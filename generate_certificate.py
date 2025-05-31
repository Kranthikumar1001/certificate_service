from pptx import Presentation
from pathlib import Path
import subprocess
import os

def generate_certificate(name, address, template_path, output_dir):
    output_pptx = Path(output_dir) / f"{name.replace(' ', '_')}.pptx"
    output_pdf = Path(output_dir) / f"{name.replace(' ', '_')}.pdf"

    # Load template
    prs = Presentation(template_path)

    # Replace placeholders
    replacements = {
        "{{Name}}": name,
        "{{Address}}": address
    }

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        for key, val in replacements.items():
                            if key in run.text:
                                run.text = run.text.replace(key, val)

    # Save modified PPTX
    prs.save(output_pptx)

    # Convert PPTX to PDF using LibreOffice
    # subprocess.run([
    #     "libreoffice", "--headless", "--convert-to", "pdf", str(output_pptx),
    #     "--outdir", str(output_dir)
    # ])

    return output_pptx
