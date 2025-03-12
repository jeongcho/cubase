import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def png_to_pdf(input_folder, output_pdf, title):
    # A4 size in points
    a4_width, a4_height = A4

    # Get list of PNG files in the input folder
    png_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]
    png_files.sort()  # Sort the files alphabetically

    # Create a PDF canvas
    c = canvas.Canvas(output_pdf, pagesize=A4)
    
    # Register a font (Malgun Gothic for Korean)
    pdfmetrics.registerFont(TTFont('MalgunGothic', 'malgun.ttf'))
    
    # Draw the title on the first page
    c.setFont('MalgunGothic', 24)
    c.drawCentredString(a4_width / 2, a4_height - 50, title)
    
    current_height = a4_height - 80  # Start drawing images below the title

    for png_file in png_files:
        # Open the PNG image
        img_path = os.path.join(input_folder, png_file)
        img = Image.open(img_path)
        
        # Resize the image to fit the width of A4, maintaining aspect ratio
        img_width, img_height = img.size
        ratio = a4_width / img_width
        img_width = a4_width
        img_height = img_height * ratio
        
        # If the image height plus current height exceeds A4 height, create a new page
        if current_height - img_height < 0:
            c.showPage()
            current_height = a4_height
        
        # Draw the image on the PDF
        c.drawImage(img_path, 0, current_height - img_height, img_width, img_height)
        current_height -= img_height

    # Save the PDF
    c.save()

# Example usage
input_folder = os.getcwd()  # Set input folder to current working directory
output_pdf = '그리워-적재.pdf'
title = '그리워-적재'
png_to_pdf(input_folder, output_pdf, title)
