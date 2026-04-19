from enum import Enum
from argparse import Namespace
from dataclasses import dataclass

class Position(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"

@dataclass
class ImageConfig:
    text: str
    position: Position
    text_padding_x: int
    text_padding_y: int
    text_background_color: str
    img_padding_x: int
    img_padding_y: int
    font_size: int = 50
    text_color: str = "#FFFFFF"
    background_opacity: float = 0.0
    background_color: str = "#000000"

    @classmethod
    def loadyaml(cls, config: Namespace):
        text_block = config.get('text') or {}
        image_block = config.get('image') or {}
        return cls(
            text=text_block.get('value') or "",
            position=Position(config.get('position')),
            text_padding_x=int(text_block.get('padding_x') or 0),
            text_padding_y=int(text_block.get('padding_y') or 0),
            text_background_color=text_block.get('background_color') or "#000000",
            img_padding_x=int(image_block.get('padding_x') or 0),
            img_padding_y=int(image_block.get('padding_y') or 0),
            font_size=int(text_block.get('font_size') or 50),
            text_color=text_block.get('color') or "#FFFFFF",
            background_opacity=float(image_block.get('background_opacity') or 0.0),
            background_color=image_block.get('background_color') or "#000000",
        )
