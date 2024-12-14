from flask import Flask, request, jsonify
from twilio.rest import Client
import schedule
import time
from threading import Thread

# Initialize Flask app
app = Flask(__name__)

# Twilio credentials
account_sid = 'ACbd5f2536cd2dc2551e4b279d2e596383'  # Replace with your Twilio Account SID
auth_token = '99ea8f13a6bd8b4679ca9cc604c06fc1'    # Replace with your Twilio Auth Token
twilio_phone_number = '+18446260311'  # Replace with your Twilio phone number

client = Client(account_sid, auth_token)

# Background scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

Thread(target=run_scheduler, daemon=True).start()

# Function to make a call
def make_call(phone_number, text_to_say):
    try:
        call = client.calls.create(
            twiml=f'<Response><Say>{text_to_say}</Say></Response>',
            to=phone_number,
            from_=twilio_phone_number
        )
        print(f"Call initiated with SID: {call.sid}")
    except Exception as e:
        print(f"Failed to make the call: {e}")

# API Endpoint to schedule a call
@app.route('/schedule_call', methods=['POST'])
def schedule_call():
    data = request.json

    # Extract request data
    phone_number = data.get('phone_number')
    text = data.get('text')
    call_time = data.get('call_time')  # Format: 'HH:MM'

    if not phone_number or not text or not call_time:
        return jsonify({'error': 'Missing phone_number, text, or call_time'}), 400

    # Schedule the call
    schedule.every().day.at(call_time).do(make_call, phone_number, text)
    return jsonify({'message': f"Call scheduled for {phone_number} at {call_time}."})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
