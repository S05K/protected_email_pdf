from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import os

def create_pdf(user_password, user_email):
    # Create a simple PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hello, Welcome!", ln=True, align='C')
    
    # Save the PDF to file
    file_path = f"{user_email}_welcome.pdf"
    pdf.output(file_path)
    
    # Apply password protection
    with open(file_path, "rb") as original_pdf:
        reader = PdfReader(original_pdf)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # Add user password
        writer.encrypt(user_password)
        
        # Save the protected PDF
        protected_pdf_path = f"{user_email}_welcome.pdf"
        with open(protected_pdf_path, "wb") as protected_pdf:
            writer.write(protected_pdf)
    
    return protected_pdf_path
