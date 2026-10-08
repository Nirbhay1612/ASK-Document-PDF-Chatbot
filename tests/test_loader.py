import pytest
from pathlib import Path
from reportlab.pdfgen import canvas


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    """Create a valid readable PDF for testing."""

    pdf_path = tmp_path / "sample.pdf"

    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, "This is a sample PDF document.")
    c.drawString(100, 730, "Testing PDF loading functionality.")
    c.save()

    return pdf_path