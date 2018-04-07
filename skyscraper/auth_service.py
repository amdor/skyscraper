import string
from typing import Tuple

from google.oauth2 import id_token
from google.auth.transport import requests

authenticated_users = set()
CLIENT_ID = '498731538493-etubco5p4at0chs18tuqmqmm8g3ngtr1.apps.googleusercontent.com'


class AuthService:
	@staticmethod
	def validate_token(token) -> Tuple[bool, string]:
		try:
			# Specify the CLIENT_ID of the app that accesses the backend:
			idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

			# Or, if multiple clients access the backend server:
			# idinfo = id_token.verify_oauth2_token(token, requests.Request())
			# if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
			#     raise ValueError('Could not verify audience.')

			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				raise ValueError('Wrong issuer.')

			# If auth request is from a G Suite domain:
			# if idinfo['hd'] != GSUITE_DOMAIN_NAME:
			#     raise ValueError('Wrong hosted domain.')

			# ID token is valid. Get the user's Google Account ID from the decoded token.
			userid = idinfo['sub']
			authenticated_users.add(userid)
			return True, userid
		except ValueError:
			return False, ''
