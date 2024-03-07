from flask import Flask, request
import africastalking
import os

app = Flask(__name__)
username = "Breeze"
api_key = "f7cd00a06e12433f0b78a8bc5454ba4782fe0eccb53dcf1078bc074ec027559c"
africastalking.initialize(username, api_key)

# Initialize Africastalking SMS
sms = africastalking.SMS

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    print(phone_number)
    print("I'm executed!")
    text = request.values.get("text", "default")
    sms_phone_number = [phone_number]
    print("I'm executed")

    if service_code == "*245#":
        if text == "":
            response = "Breeze What would you like to do?\n"
            response += "1. Check account details\n"
            response += "2. Check phone number\n"
            response += "3. Send me a message"

        elif text == "1":
            response = "Breeze What would you like to check on your account?\n"
            response += "1. Account Balance\n"
            response += "2. Account Number"

        elif text == "2":
            response = "END Your phone number is {}".format(phone_number)

        elif text == "3":
            try:
                sms_response = sms.send("Thank you for your response", sms_phone_number)
                print(sms_response)
                response = "END Message sent successfully"
            except Exception as e:
                print(f"We have a problem: {e}")
                response = "END Failed to send message"

        elif text == "1*1":
            account_number = "1243324376742"
            response = "END Your account number is {}".format(account_number)

        elif text == "1*2":
            account_balance = "100,000"
            response = "END Your account balance is KES {}".format(account_balance)
        
        else:
            response = "END Invalid input. Try again."
    else:
        response = "END Invalid service code. Please dial *245# to access this service."

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))
