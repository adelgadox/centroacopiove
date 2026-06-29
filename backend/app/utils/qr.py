"""QR code generation utilities.

Generates QR codes that point to the public box ficha URL (/b/{code}).
The QR is returned as raw PNG bytes — callers decide how to embed it.
"""

import io

import qrcode
from qrcode.image.pil import PilImage


def box_qr_png(code: str, base_url: str, size: int = 10) -> bytes:
    """Return PNG bytes for a QR code pointing to /b/{code}."""
    url = f"{base_url.rstrip('/')}/b/{code}"
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
