from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    
    # Extract caller ID from the webhook
    caller_id = data.get("from_number", "unknown")
    
    # Format the number for better readability (optional)
    formatted_number = format_phone_number(caller_id)
    
    response = {
        "response_id": data.get("response_id"),
        "state": [
            {
                "key": "caller_id_number", 
                "value": formatted_number
            }
        ],
        "transcript": [
            {
                "role": "system",
                "content": f"I see you're calling from {formatted_number}. Is this the best number to reach you?"
            }
        ]
    }
    
    return jsonify(response)

def format_phone_number(phone_number):
    """Format phone number to (XXX) XXX-XXXX format"""
    if phone_number == "unknown":
        return "unknown number"
    if len(phone_number) == 10:
        return f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
    elif len(phone_number) == 11 and phone_number.startswith('1'):
        return f"({phone_number[1:4]}) {phone_number[4:7]}-{phone_number[7:]}"
    return phone_number

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
