import smtplib
from email.message import EmailMessage

def send_email(receiver_email, pdf_path):
    msg = EmailMessage()
    msg["Subject"] = "Your Participation certificate"
    msg["From"] = "ditchrabbitsega@gmail.com"
    msg["To"] = receiver_email
    #msg.set_content(body)

    # Attach PDF
    with open(pdf_path, "rb") as f:
        file_data = f.read()
        file_name = pdf_path.name
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # Send email via Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("ditchrabbitsega@gmail.com", "cokr vzrf xiaj emmb")
        smtp.send_message(msg)
