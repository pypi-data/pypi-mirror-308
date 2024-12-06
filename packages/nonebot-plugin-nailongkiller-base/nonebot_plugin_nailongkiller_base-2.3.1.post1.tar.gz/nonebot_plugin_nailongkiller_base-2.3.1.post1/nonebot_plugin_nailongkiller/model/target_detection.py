import asyncio
from dataclasses import dataclass
from typing import Optional
from typing_extensions import override

from ultralytics import YOLO
import numpy as np
from cookit import with_semaphore
from nonebot.utils import run_sync

from ..config import config
from ..frame_source import FrameSource, repack_save
from .utils.common import CheckResult, CheckSingleResult, race_check
from .utils.update import GitHubLatestReleaseModelUpdater, ModelInfo, UpdaterGroup

model_filename = "NailongKiller.yolo11n.pt"

class ModelUpdater(GitHubLatestReleaseModelUpdater):
    @override
    def get_info(self) -> ModelInfo[None]:
        info = super().get_info()
        info.filename = model_filename
        return info

# 更新 GitHub 仓库信息
OWNER = "Hakureirm"
REPO = "NailongKiller"

model_path, labels_path = UpdaterGroup(
    ModelUpdater(
        OWNER,
        REPO,
        lambda x: x == model_filename,
    ),
    GitHubLatestReleaseModelUpdater(
        OWNER,
        REPO,
        lambda x: x == "labels.txt",
    ),
).get()

# 加载模型
model = YOLO(model_path)

@dataclass
class Detections:
    boxes: np.ndarray
    scores: np.ndarray
    ids: np.ndarray

@dataclass
class FrameInfo:
    frame: np.ndarray
    detections: Optional[Detections] = None

    def vis(self) -> np.ndarray:
        if not self.detections:
            return self.frame
        
        # 使用 YOLO 的可视化功能
        results = model.predict(self.frame, conf=0.3, show=False)[0]
        return results.plot()

@run_sync
def _check_single(frame: np.ndarray) -> CheckSingleResult[Optional[Detections]]:
    # 使用 YOLO 进行预测
    results = model.predict(frame, conf=0.1)[0]
    
    if len(results.boxes) == 0:
        return CheckSingleResult.not_ok(None)

    boxes = results.boxes.xyxy.cpu().numpy()
    scores = results.boxes.conf.cpu().numpy()
    cls_ids = results.boxes.cls.cpu().numpy()

    for c, s in zip(cls_ids, scores):
        label = results.names[int(c)]
        expected = config.nailong_model1_score.get(label)
        if (expected is not None) and s >= expected:
            return CheckSingleResult(
                ok=True,
                label=label,
                extra=Detections(boxes, scores, cls_ids),
            )
    return CheckSingleResult.not_ok(None)

async def check_single(frame: np.ndarray) -> CheckSingleResult[FrameInfo]:
    res = await _check_single(frame)
    return CheckSingleResult(
        ok=res.ok,
        label=res.label,
        extra=FrameInfo(frame, res.extra),
    )

async def check(source: FrameSource) -> CheckResult:
    label = None
    extra_vars = {}
    if config.nailong_check_all_frames:
        sem = asyncio.Semaphore(config.nailong_concurrency)
        results = await asyncio.gather(
            *(with_semaphore(sem)(check_single)(frame) for frame in source),
        )
        ok = any(r.ok for r in results)
        if ok:
            all_labels = {r.label for r in results if r.label}
            label = next(
                (x for x in config.nailong_model1_score if x in all_labels),
                None,
            )
            extra_vars["$checked_result"] = await repack_save(
                source,
                (r.extra.vis() for r in results),
            )
    else:
        res = await race_check(check_single, source)
        ok = bool(res)
        if res:
            label = res.label
            extra_vars["$checked_result"] = await repack_save(
                source,
                iter((res.extra.vis(),)),
            )
    return CheckResult(ok, label, extra_vars)