"""Image-to-PDF conversion helpers."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class ConversionError(ValueError):
    """Raised when an uploaded file cannot be converted."""


def image_bytes_to_pdf(data: bytes) -> bytes:
    """Convert JPG/PNG bytes to a one-page PDF."""
    try:
        with Image.open(BytesIO(data)) as image:
            source_format = image.format
            if source_format not in {"JPEG", "PNG"}:
                raise ConversionError("仅支持 JPG 和 PNG 格式")
            image = ImageOps.exif_transpose(image)

            if image.mode in {"RGBA", "LA"} or (
                image.mode == "P" and "transparency" in image.info
            ):
                rgba = image.convert("RGBA")
                background = Image.new("RGBA", rgba.size, "white")
                background.alpha_composite(rgba)
                pdf_image = background.convert("RGB")
            else:
                pdf_image = image.convert("RGB")

            output = BytesIO()
            pdf_image.save(output, "PDF", resolution=100.0)
            pdf_image.close()
            return output.getvalue()
    except ConversionError:
        raise
    except (OSError, UnidentifiedImageError, ValueError) as exc:
        raise ConversionError("图片损坏或格式无法识别") from exc


def pdf_filename(image_filename: str) -> str:
    """Keep the original filename prefix and replace its extension with .pdf."""
    return f"{Path(image_filename).stem}.pdf"


def safe_output_path(directory: Path, filename: str) -> Path:
    """Return a path contained directly inside the selected output directory."""
    return directory / Path(filename).name
