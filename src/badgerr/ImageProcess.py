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
    def __init__(self):
        self._logger: Logger = logging.getLogger("badgerr:ImageProcess")
        self._font: ImageFont.ImageFont | FreeTypeFont = ImageFont.load_default()
        self._img_width: int = 0
        self._img_height: int = 0
        self._text_width: float = 0
        self._text_height: float = 0

    def _reset_values(self):
        self._img_width = 0
        self._img_height = 0
        self._text_width = 0
        self._text_height = 0

    def get_font(self, url: str, config: ImageConfig):
        try:
            response: requests.Response = requests.get(url)
            response.raise_for_status()
            font_bytes: BytesIO = io.BytesIO(response.content)
            self._font = ImageFont.truetype(font_bytes, config.font_size)
        except RequestException as e:
            self._logger.error(f"Could not fetch font from: {url}. Falling back to default font: {e}")

    def _get_x_y_pos(self, config: ImageConfig) -> tuple[int, int]:
        x: int = 0
        y: int = 0
        if config.position == Position.TOP:
            x = int((self._img_width - self._text_width) / 2)
            y = config.img_padding_y + config.text_padding_y
        elif config.position == Position.BOTTOM:
            x = int((self._img_width - self._text_width) / 2)
            y = int(self._img_height - self._text_height - config.img_padding_y - config.text_padding_y)
        elif config.position == Position.LEFT:
            x = config.img_padding_x + config.text_padding_x
            y = int((self._img_height - self._text_height) / 2)
        elif config.position == Position.RIGHT:
            x = int(self._img_width - self._text_width - config.img_padding_x - config.text_padding_x)
            y = int((self._img_height - self._text_height) / 2)
        elif config.position == Position.TOP_LEFT:
            x = config.img_padding_x + config.text_padding_x
            y = config.img_padding_y + config.text_padding_y
        elif config.position == Position.TOP_RIGHT:
            x = int(self._img_width - self._text_width - config.img_padding_x - config.img_padding_x)
            y = config.img_padding_y + config.text_padding_y
        elif config.position == Position.BOTTOM_LEFT:
            x = config.img_padding_x + config.text_padding_x
            y = int(self._img_height - self._text_height - config.img_padding_y - config.text_padding_y)
        elif config.position == Position.BOTTOM_RIGHT:
            x = int(self._img_width - self._text_width - config.img_padding_x - config.text_padding_x)
            y = int(self._img_height - self._text_height - config.img_padding_y - config.text_padding_y)
        elif config.position == Position.CENTER:
            x = int((self._img_width - self._text_width) / 2)
            y = int((self._img_height - self._text_height) / 2)
        return (x, y)

    def _draw_overlay(self, dest_image: Image.Image, config: ImageConfig):
        overlay_layer = Image.new("RGBA", dest_image.size, (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay_layer)
        rgb = ImageColor.getcolor(config.background_color, "RGB")
        alpha = int(config.background_opacity * 255)
        color = (*rgb, alpha)
        left, top, right, bottom = draw_ov.textbbox((0, 0), config.text, font=self._font)
        self._text_width = right - left
        self._text_height = bottom - top
        x, y = self._get_x_y_pos(config)
        left, top, right, bottom = draw_ov.textbbox((x, y), config.text, font=self._font)
        coords = [
            0, 0,
            self._img_width, self._img_height
        ]
        draw_ov.rectangle(coords, fill=color)
        draw_ov.rectangle(
            xy=(
                left - config.text_padding_x,
                top - config.text_padding_y,
                right + config.text_padding_x,
                bottom + config.text_padding_y
            ),
            fill=(ImageColor.getcolor(config.text_background_color, "RGB"))
        )
        draw_ov.text((x, y), config.text, font=self._font, fill=config.text_color)
        return Image.alpha_composite(dest_image, overlay_layer)

    def apply_overlay(self, src_image: bytes, config: ImageConfig) -> bytes:
        dest_image: Image.Image = Image.open(io.BytesIO(src_image)).convert("RGBA")
        self._img_width, self._img_height = dest_image.size
        dest_image = self._draw_overlay(dest_image, config)
        ImageDraw.Draw(dest_image)
        output_buffer = io.BytesIO()
        dest_image.convert("RGB").save(output_buffer, format="PNG", quality=100)
        self._reset_values()
        return output_buffer.getvalue()

    # TEST
    def write_img_file(self, img: bytes, filename: str):
        with open(filename, 'wb') as file:
            file.write(img)
