from imgurpython import ImgurClient
from dotenv import load_dotenv
import os
load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

client = ImgurClient(client_id, client_secret)

# Authorization flow, pin example (see docs for other auth types)
authorization_url = client.get_auth_url('pin')

# ... redirect user to `authorization_url`, obtain pin (or code or token) ...

credentials = client.authorize('PIN OBTAINED FROM AUTHORIZATION', 'pin')
client.set_user_auth(credentials['access_token'], credentials['refresh_token'])