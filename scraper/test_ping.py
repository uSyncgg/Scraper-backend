import requests
import time

# url = 'https://website-backend-5m32.onrender.com/usyncapp/tournaments'

# try:
#     response = requests.get(url)
#     print(f"Pinged {url} - Status code: {response.status_code}")
# except Exception as e:
#     print(f"Error pinging {url}: {e}")

flask_url = 'http://127.0.0.1:5000'

response = requests.post(flask_url + '/start-long-task')
print("Status Code:", response.status_code)
print("Response JSON:", response.json())


for i in range(0, 20):
    response2 = requests.get(flask_url + '/quick-task')

    print("Status Code 2:", response2.status_code)
    print("Response JSON 2:", response2.json())

    time.sleep(5)

