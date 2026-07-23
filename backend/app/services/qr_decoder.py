import cv2
from pathlib import Path


def decode_qr(file_path: Path) -> str:
    """
    Decode QR code from an image.

    Args:
        file_path: Path of uploaded image.

    Returns:
        Decoded QR text.

    Raises:
        ValueError if QR code is not detected.
    """

    image = cv2.imread(str(file_path))

    if image is None:
        raise ValueError("Unable to read uploaded image.")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.equalizeHist(gray)

    detector = cv2.QRCodeDetector()

    data, points, _ = detector.detectAndDecode(gray)

    if not data:
        raise ValueError("No QR code detected in the uploaded image.")

    return data