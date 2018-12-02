import requests

class MemcoinAPI(object):
    def __init__(self, api_url, token):
        self.token = token
        self.api_url = api_url
        self.headers = { 'token': token }

    def get_user(self, chat_id):
        response = requests.get(self.api_url + '/user/' + chat_id, headers=self.headers)
        return response.text

    def transfer(self, sender_id, receiver_id, amount):
        payload = {'senderId': sender_id, 'receiverId': receiver_id, 'amount': amount }
        response = requests.post(self.api_url + '/transfer', data=payload, headers=self.headers).text
        return response