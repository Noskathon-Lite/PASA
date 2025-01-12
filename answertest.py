import requests
import json

url = "http://127.0.0.1:8000/answer"
headers = {'Content-Type': 'application/json'}

answers = [
    'This is answer0',
    'This is answer1',
    'This is answer2',
    'This is answer3',
    'This is answer4',
    'This is answer5',
    'This is answer6',
    'This is answer7',
    'This is answer8',
    'This is answer9',
]
ID = 7

data = {
    'answers':answers,
    'userId':ID
}

response_data = requests.post(url, json=data, headers=headers)

# response = response_data.json()

# print(f"THE RESPONSE FROM SERVER: {response}")
# print(f"THE STATUS CODE IS: {response_data.status_code}")
# print(f"logged in as: {response['userType']}")


response = response_data.json()
print(f"THE RESPONSE FROM SERVER: {response}")
print(f"THE STATUS CODE IS: {response_data.status_code}")
print("Usernames: ")
print(response['usernames'])
#print(f"logged in as: {response['userType']}")
#print(f"MSG: {response['msg']}")
#print(f"THE profId IS: {response['profId']}")
#print(f"Processed answers are: ")
#for i in response['processedAnswers']:
#    print(f"Value: {i}")