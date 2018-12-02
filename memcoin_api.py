import requests

class ApiResponse:
    def __init__(self, response):
        self.__response = response
        self.json = response.json()
        self.success = response.status_code == 200
        self.error = self.json['type'] if not self.success else 'no error'

    def __str__(self):
        return str(self.json)

class MemcoinAPI(object):
    def __init__(self, api_url, token):
        self.__token = token
        self.__api_url = api_url
        self.__headers = { 'token': token }

    def get_user(self, chat_id):
        response = requests.get(self.__api_url + '/user/' + chat_id, headers=self.__headers)
        return ApiResponse(response) 

    def transfer(self, sender_id, receiver_id, amount):
        payload = {'senderId': sender_id, 'receiverId': receiver_id, 'amount': amount }
        response = requests.post(self.__api_url + '/transfer', data=payload, headers=self.__headers)
        return ApiResponse(response)