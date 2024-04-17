from instamojo_wrapper import Instamojo
API_KEY = 'test_dd284029d221d9e3cca0b703679'
AUTH_TOKEN = 'test_8e5c4ab3cd24a28e883247b4ae7'

api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

# Create a new Payment Request
response = api.payment_request_create(
    amount='11',
    purpose='Testing',
    send_email=True,
    email="lovehate9899@gmail.com.com",
    redirect_url="http://localhost:8000/handle_redirect"
    )
# print the long URL of the payment request.
print(response['payment_request']['longurl'])