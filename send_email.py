import smtplib
from email.message import EmailMessage
import os

def send_certificate_email(to_email, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = 'Your Event Certificate'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = to_email
    msg.set_content('Please find your certificate attached.')

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))

    # Replace with your SMTP credentials
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your_email@gmail.com', 'your_app_password')
        smtp.send_message(msg)
