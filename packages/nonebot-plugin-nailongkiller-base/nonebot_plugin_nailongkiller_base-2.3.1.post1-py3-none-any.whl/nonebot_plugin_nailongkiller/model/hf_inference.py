from gradio_client import Client, handle_file
from typing import Union, Dict
import os
from pathlib import Path

class HFInference:
    def __init__(self):
        self.client = Client("Hakureirm/NailongKiller")
    
    async def predict(self, image_path: Union[str, Path]) -> Dict:
        """
        使用 Hugging Face API 进行推理
        
        Args:
            image_path: 图片路径，可以是本地路径或URL
            
        Returns:
            Dict: 推理结果
        """
        try:
            # 判断是否为URL
            if image_path.startswith(('http://', 'https://')):
                result = self.client.predict(
                    img=handle_file(image_path),
                    api_name="/predict"
                )
            else:
                # 本地文件
                result = self.client.predict(
                    img=handle_file(str(Path(image_path).absolute())),
                    api_name="/predict"
                )
            
            return result
        except Exception as e:
            raise Exception(f"HF API inference failed: {str(e)}")