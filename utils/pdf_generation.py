# utils/pdf_generation.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_case_pdf(summary=None, chat_history=None):
    """Generate a PDF with document summary and chat history."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    y = 750  # Starting y-position
    line_height = 15
    max_width = 400  # Maximum width for text (in points)

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "Case Summary")
    y -= 30

    # Add Summary (if provided)
    if summary:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, "Document Summary:")
        y -= 20
        c.setFont("Helvetica", 10)
        for line in summary.split('\n'):
            words = line.split()
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                if c.stringWidth(test_line, "Helvetica", 10) > max_width:
                    c.drawString(100, y, current_line)
                    y -= line_height
                    if y < 50:
                        c.showPage()
                        y = 750
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                c.drawString(100, y, current_line)
                y -= line_height
        y -= 10

    # Add Chat History (if provided)
    if chat_history:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, "Chat Conversation:")
        y -= 20
        c.setFont("Helvetica", 10)
        for entry in chat_history:
            user_text = f"User: {entry['user']}"
            bot_text = f"Bot: {entry['bot']}"
            for text in [user_text, bot_text]:
                words = text.split()
                current_line = ""
                for word in words:
                    test_line = f"{current_line} {word}".strip()
                    if c.stringWidth(test_line, "Helvetica", 10) > max_width:
                        c.drawString(100, y, current_line)
                        y -= line_height
                        if y < 50:
                            c.showPage()
                            y = 750
                        current_line = word
                    else:
                        current_line = test_line
                if current_line:
                    c.drawString(100, y, current_line)
                    y -= line_height
            y -= 5  # Extra spacing between entries

    c.save()
    buffer.seek(0)
    return buffer.getvalue()