import requests

def send_test():
    url = "http://127.0.0.1:8000/types/add"
    data = {
        "id": 15,
        "name": "Drinking",
        "desc": "A lot of beer will be had"
    }

    # Use the 'json' parameter so requests automatically handles headers and serialization
    response = requests.post(url, json=data)
    print(response.json())
