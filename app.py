from flask import Flask, request, jsonify
from generate_certificate import generate_certificate
from send_email import send_certificate_email
from pathlib import Path
import os

app = Flask(__name__)
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/send-certificates", methods=["POST"])
def send_certificates():
    data = request.json
    attendees = data["attendees"]  # List of dicts with name, email, address
    template_url = data["template_url"]
    sender_email = data["sender_email"]
    sender_password = data["sender_password"]

    template_path = Path(TEMPLATE_DIR) / "template.pptx"
    if not template_path.exists():
        return jsonify({"error": "Template not found"}), 400

    results = []
    for attendee in attendees:
        name = attendee["name"]
        email = attendee["email"]
        address = attendee["address"]

        pdf_path = generate_certificate(name, address, template_path, OUTPUT_DIR)
        send_certificate_email(
            receiver_email=email,
            subject="Your Event Certificate",
            body=f"Hi {name},\n\nFind your certificate attached.",
            pdf_path=pdf_path,
            sender_email=sender_email,
            sender_password=sender_password
        )
        results.append({"email": email, "status": "sent"})

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
