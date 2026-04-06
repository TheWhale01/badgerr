from enum import Enum
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
