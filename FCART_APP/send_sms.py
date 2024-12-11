from twilio.rest import Client
import os
# with call
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
FROM_PHONE = os.getenv('TWILIO_PHONE_NUMBER')
whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')


def send_otp_call(phone_number, otp):
    client = Client(account_sid, auth_token)
    try:
        call = client.calls.create(
            to="+917719596737",
            from_="+16413268611",
            twiml=f'<Response><Say>Your OTP is {otp}</Say></Response>'
        )
    except Exception as e:
        print("Fail Call", str(e))
    return call.sid



# with text sms
def sendsms(phone_number, otp):
    client = Client(account_sid, auth_token)
    message_body = f"OTP for registration is {otp}."

    try:
        sent_message = client.messages.create(
            to="+917719596737",
            from_="+16413268611",
            body=message_body
        )
        print("SMS sent:", sent_message.sid)
    except Exception as e:
        print("Fail send SMS:", str(e))
    return otp
# print(sendsms('7719596737', "88999"))
