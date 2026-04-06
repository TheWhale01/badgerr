import io
import requests
import logging
from io import BytesIO
from logging import Logger
from PIL import Image, ImageColor, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont
from requests.exceptions import RequestException
from badgerr.ImageConfig import ImageConfig, Position

class ImageProcess:
    def __init__(self, font_url: str, config: ImageConfig):
        self._logger: Logger = logging.getLogger("badgerr:ImageProcess")
        self._font: ImageFont.ImageFont | FreeTypeFont = ImageFont.load_default()
        self._img_width: int = 0
        self._img_height: int = 0
        self._text_width: float = 0
        self._text_height: float = 0
        self._config: ImageConfig = config
        self._get_font(font_url)

    def _reset_values(self):
        self._img_width = 0
        self._img_height = 0
        self._text_width = 0
        self._text_height = 0

    def _get_font(self, url: str):
        try:
            response: requests.Response = requests.get(url)
            response.raise_for_status()
            font_bytes: BytesIO = io.BytesIO(response.content)
            self._font = ImageFont.truetype(font_bytes, self._config.font_size)
        except RequestException as e:
            self._logger.error(f"Could not fetch font from: {url}. Falling back to default font: {e}")

    def _get_x_y_pos(self) -> tuple[int, int]:
        x: int = 0
        y: int = 0
        if self._config.position == Position.TOP:
            x = int((self._img_width - self._text_width) / 2)
            y = self._config.img_padding_y + self._config.text_padding_y
        elif self._config.position == Position.BOTTOM:
            x = int((self._img_width - self._text_width) / 2)
            y = int(self._img_height - self._text_height - self._config.img_padding_y - self._config.text_padding_y)
        elif self._config.position == Position.LEFT:
            x = self._config.img_padding_x + self._config.text_padding_x
            y = int((self._img_height - self._text_height) / 2)
        elif self._config.position == Position.RIGHT:
            x = int(self._img_width - self._text_width - self._config.img_padding_x - self._config.text_padding_x)
            y = int((self._img_height - self._text_height) / 2)
        elif self._config.position == Position.TOP_LEFT:
            x = self._config.img_padding_x + self._config.text_padding_x
            y = self._config.img_padding_y + self._config.text_padding_y
        elif self._config.position == Position.TOP_RIGHT:
            x = int(self._img_width - self._text_width - self._config.img_padding_x - self._config.img_padding_x)
            y = self._config.img_padding_y + self._config.text_padding_y
        elif self._config.position == Position.BOTTOM_LEFT:
            x = self._config.img_padding_x + self._config.text_padding_x
            y = int(self._img_height - self._text_height - self._config.img_padding_y - self._config.text_padding_y)
        elif self._config.position == Position.BOTTOM_RIGHT:
            x = int(self._img_width - self._text_width - self._config.img_padding_x - self._config.text_padding_x)
            y = int(self._img_height - self._text_height - self._config.img_padding_y - self._config.text_padding_y)
        elif self._config.position == Position.CENTER:
            x = int((self._img_width - self._text_width) / 2)
            y = int((self._img_height - self._text_height) / 2)
        return (x, y)

    def _draw_overlay(self, dest_image: Image.Image):
        overlay_layer = Image.new("RGBA", dest_image.size, (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay_layer)
        rgb = ImageColor.getcolor(self._config.background_color, "RGB")
        alpha = int(self._config.background_opacity * 255)
        color = (*rgb, alpha)
        left, top, right, bottom = draw_ov.textbbox((0, 0), self._config.text, font=self._font)
        self._text_width = right - left
        self._text_height = bottom - top
        x, y = self._get_x_y_pos()
        left, top, right, bottom = draw_ov.textbbox((x, y), self._config.text, font=self._font)
        coords = [
            0, 0,
            self._img_width, self._img_height
        ]
        draw_ov.rectangle(coords, fill=color)
        draw_ov.rectangle(
            xy=(
                left - self._config.text_padding_x,
                top - self._config.text_padding_y,
                right + self._config.text_padding_x,
                bottom + self._config.text_padding_y
            ),
            fill=(ImageColor.getcolor(self._config.text_background_color, "RGB"))
        )
        draw_ov.text((x, y), self._config.text, font=self._font, fill=self._config.text_color)
        return Image.alpha_composite(dest_image, overlay_layer)

    def apply_overlay(self, src_image: bytes) -> bytes:
        dest_image: Image.Image = Image.open(io.BytesIO(src_image)).convert("RGBA")
        self._img_width, self._img_height = dest_image.size
        dest_image = self._draw_overlay(dest_image)
        output_buffer = io.BytesIO()
        dest_image.convert("RGB").save(output_buffer, format="PNG", quality=100)
        self._reset_values()
        return output_buffer.getvalue()
