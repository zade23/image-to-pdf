from io import BytesIO
import pytest
from PIL import Image

from converter import ConversionError, image_bytes_to_pdf, pdf_filename


def make_image(image_format: str, mode: str = "RGB") -> bytes:
    buffer = BytesIO()
    color = (255, 0, 0, 100) if mode == "RGBA" else (255, 0, 0)
    Image.new(mode, (24, 12), color).save(buffer, image_format)
    return buffer.getvalue()


@pytest.mark.parametrize("image_format", ["JPEG", "PNG"])
def test_converts_supported_images(image_format: str) -> None:
    result = image_bytes_to_pdf(make_image(image_format))
    assert result.startswith(b"%PDF")


def test_converts_transparent_png() -> None:
    result = image_bytes_to_pdf(make_image("PNG", "RGBA"))
    assert result.startswith(b"%PDF")


def test_rejects_invalid_file() -> None:
    with pytest.raises(ConversionError):
        image_bytes_to_pdf(b"not an image")


def test_keeps_filename_prefix() -> None:
    assert pdf_filename("holiday.photo.JPG") == "holiday.photo.pdf"
