from io import BytesIO
from pathlib import Path

import pytest
from pypdf import PdfReader
from reportlab.pdfgen import canvas


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    """Create a valid sample PDF for testing."""

    pdf_path = tmp_path / "sample.pdf"

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, "This is a test PDF document.")
    pdf.drawString(100, 730, "It contains readable text for testing.")
    pdf.save()

    pdf_path.write_bytes(buffer.getvalue())

    # Verify that the generated PDF is actually valid.
    reader = PdfReader(str(pdf_path))

    assert len(reader.pages) > 0

    return pdf_path