import requests


class ClientAuth(requests.auth.AuthBase):

    def __init__(self, access_token=None):
        if access_token:
            if requests.get('https://api.typeform.com/forms', headers={'authorization': 'bearer '+access_token}).status_code==200:
                self.access_token = access_token
                print('Ok, token valid')
            else:
                print('Invalid Token')
        else:
            print("You must provide an access_token ")

    def __call__(self):#, r):
        return (self.access_token)
        