from flask import Flask, request, jsonify
from generate_certificate import generate_certificate
from send_email import send_certificate_email

app = Flask(__name__)

@app.route('/send-certificates', methods=['POST'])
def send_certificates():
    data = request.get_json()
    attendees = data.get('attendees', [])
    template_url = data.get('template_url')
    event_location = data.get('event_location')

    results = []

    for attendee in attendees:
        name = attendee['name']
        email = attendee['email']
        pptx_path, pdf_path = generate_certificate(name, event_location, template_url)
        send_certificate_email(email, pdf_path)
        results.append({'name': name, 'email': email, 'status': 'sent'})

    return jsonify({'status': 'success', 'results': results})

if __name__ == '__main__':
    app.run(debug=True)
