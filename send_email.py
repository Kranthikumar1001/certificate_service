import smtplib
from email.message import EmailMessage

def send_certificate_email(receiver_email, subject, body, pdf_path, sender_email, sender_password):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    # Attach PDF
    with open(pdf_path, "rb") as f:
        file_data = f.read()
        file_name = pdf_path.name
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # Send email via Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
