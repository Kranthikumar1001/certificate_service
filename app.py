from flask import Flask, request, jsonify
from generate_certificate import generate_certificate
from send_email import send_email
import os
import requests

app = Flask(__name__)

# Directory to save generated files
OUTPUT_DIR = "generated_certificates"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_template(template_url, filename='template.pptx'):
    try:
        response = requests.get(template_url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        else:
            raise Exception(f"Failed to download template. Status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error downloading template: {str(e)}")

@app.route("/send-certificates", methods=["POST"])
def send_certificates():
    data = request.get_json()

    attendees = data.get("attendees", [])
    template_url = data.get("template_url")
    event_location = data.get("location")

    if not template_url or not attendees or not event_location:
        return jsonify({"error": "Missing required data"}), 400

    try:
        downloaded_template = download_template(template_url)

        for attendee in attendees:
            name = attendee.get("name")
            email = attendee.get("email")

            if not name or not email:
                continue  # Skip invalid entries

            # Generate the certificate
            pdf_path = generate_certificate(name, event_location, downloaded_template, OUTPUT_DIR)

            # Send email
            send_email(email, pdf_path)

        return jsonify({"message": "Certificates generated and sent successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
