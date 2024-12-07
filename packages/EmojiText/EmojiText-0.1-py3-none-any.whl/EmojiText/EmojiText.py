# custom_emoji.py 내 EmojiHandler 클래스 수정

from PIL import Image, ImageSequence
import re
from typing import List, Union

class EmojiHandler:
    def __init__(self, emoji_folder: str = "emojis"):
        self.emoji_folder = emoji_folder
        self.emoji_map = {
            "coffee": f"{self.emoji_folder}/293ab0f0-d19d-480f-8b01-c9f2197d44cc-8.png",
        }

    def get_emoji_image(self, emoji_name: str):
        path = self.emoji_map.get(emoji_name)
        if not path:
            return None

        # GIF 파일 여부 확인
        if path.endswith('.gif'):
            image = Image.open(path)
            # 첫 번째 프레임만 반환하거나 여러 프레임으로 사용할 수 있도록 조정 가능
            frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
            return frames[0]  # 첫 번째 프레임 반환, 또는 frames 전체를 반환하여 애니메이션으로 다룰 수 있음
        else:
            return Image.open(path)

    def parse_text(self, text: str) -> List[Union[str, Image.Image]]:
        result = []
        tokens = re.split(r"(\(\w+\))", text)

        for token in tokens:
            if token.startswith("(") and token.endswith(")"):
                emoji_name = token[1:-1]
                emoji_image = self.get_emoji_image(emoji_name)
                if emoji_image:
                    result.append(emoji_image)  # 이미지 추가
                else:
                    result.append(token)  # 매칭되는 이모지가 없으면 원래 텍스트 유지
            else:
                result.append(token)  # 일반 텍스트

        return result
