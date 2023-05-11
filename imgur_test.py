from imgurpython import ImgurClient
from dotenv import load_dotenv
import os
load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")


def get_input(string):
    return input(string)


def authenticate():
    # Get client ID and secret from config.py
    client = ImgurClient(client_id, client_secret)

    # Authorization flow, pin example (see docs for other auth types)
    authorization_url = client.get_auth_url('pin')

    print(f"Go to the following URL: {authorization_url}")

    # Read in the pin, handle Python 2 or 3 here.
    pin = get_input("Enter pin code: ")

    # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    print("Authentication successful! Here are the details:")
    print(f"   Access token:  {credentials['access_token']}")
    print(f"   Refresh token: {credentials['refresh_token']}")
    auth_tokens = {" Access token": credentials['access_token'],
                   " Refresh token": credentials['refresh_token']}

    return client, auth_tokens


# If you want to run this as a standalone script, so be it!
if __name__ == "__main__":
     client , auth_token = authenticate()
     access_token = auth_token[" Access token"]
     refresh_token = auth_token[" Refresh token"]
