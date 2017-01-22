from oauth2client import client, crypt

class Auth():

    # def __init__(self):
    #     pass

    def validate_token(self, token, client_id, domain):
        # (Receive token by HTTPS POST)
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)

            # Or, if multiple clients access the backend server:
            #idinfo = client.verify_id_token(token, None)
            #if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #    raise crypt.AppIdentityError("Unrecognized client.")

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")

            # If auth request is from a G Suite domain:
            if idinfo['hd'] != domain:
               raise crypt.AppIdentityError("Wrong hosted domain.")
        except crypt.AppIdentityError:
            # Invalid token
            raise crypt.AppIdentityError("Invalid token.")
        userid = idinfo['sub']
        return userid

    # def check_aud(client_id, app_client_id):
    #     if user_id['hd'] == app_client_id
