from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
import re
from typing import List, Union


class EmojiHandler:
    def __init__(self, emoji_folder: str = "emojis"):
        self.emoji_folder = emoji_folder
        self.emoji_map = {
            "coffee": f"{self.emoji_folder}/293ab0f0-d19d-480f-8b01-c9f2197d44cc-8.png",
        }
        self.emoji_size = (64, 64)  # 항상 64x64 픽셀로 고정

    def get_emoji_image(self, emoji_name: str):
        path = self.emoji_map.get(emoji_name)
        if not path:
            return None

        if path.endswith('.gif'):
            image = Image.open(path)
            frames = [frame.copy().resize(self.emoji_size, Image.ANTIALIAS) for frame in ImageSequence.Iterator(image)]
            return ImageTk.PhotoImage(frames[0])  # 첫 번째 프레임 변환
        else:
            image = Image.open(path)
            image = image.resize(self.emoji_size, Image.ANTIALIAS)  # PNG, JPG 리사이즈
            return ImageTk.PhotoImage(image)

    def parse_text(self, text: str) -> List[Union[str, ImageTk.PhotoImage]]:
        result = []
        tokens = re.split(r"(;[a-zA-Z0-9_]+;)", text)  # 이모지 형식을 ;emoji_name;로 변경

        for token in tokens:
            if token.startswith(";") and token.endswith(";"):
                emoji_name = token[1:-1]  # 앞뒤의 ; 제거
                emoji_image = self.get_emoji_image(emoji_name)
                if emoji_image:
                    result.append(emoji_image)
                else:
                    result.append(token)
            else:
                result.append(token)

        return result

    def create_labels(self, parent: tk.Widget, text: str) -> List[tk.Label]:
        labels = []
        parsed_result = self.parse_text(text)

        for item in parsed_result:
            label = tk.Label(
                parent,
                image=item if isinstance(item, ImageTk.PhotoImage) else None,
                text=None if isinstance(item, ImageTk.PhotoImage) else item,
            )
            if isinstance(item, ImageTk.PhotoImage):
                label.image = item  # 참조 유지
            label.pack()
            labels.append(label)

        return labels
