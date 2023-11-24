import requests

test = "I am testing the fast API"

response = requests.post("http://127.0.0.1:8000/upload_video", params = {"test" : test})

#print(response.json())


if response.status_code == 200:
    data = response.json()
    print("Uppercase text:", data.get("upper_test"))
else:
    print("Failed to receive response from FastAPI")
