from enum import Enum
from typing import Any
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
    def loadyaml(cls, config: Any):
        return cls(
            text = config.get('text').get('value'),
            position = config.get('position'),
            text_padding_x = config.get('text').get('padding_x'),
            text_padding_y = config.get('text').get('padding_y'),
            text_background_color = config.get('text').get('background_color'),
            img_padding_x = config.get('image').get('padding_x'),
            img_padding_y = config.get('image').get('padding_y'),
            font_size = config.get('text').get('font_size'),
            text_color = config.get('text').get('color'),
            background_opacity = config.get('image').get('background_opacity'),
            background_color = config.get('image').get('background_color'),
        )
