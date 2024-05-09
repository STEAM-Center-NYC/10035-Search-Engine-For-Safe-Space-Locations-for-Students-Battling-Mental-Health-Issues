import http.client
import requests

conn = http.client.HTTPSConnection("waze.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "SIGN-UP-FOR-KEY",
    'X-RapidAPI-Host': "waze.p.rapidapi.com"
}

conn.request("GET", "/driving-directions?source_coordinates=32.0852999%2C34.78176759999999&destination_coordinates=32.7940463%2C34.989571", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))



url = "https://waze.p.rapidapi.com/driving-directions"

querystring = {"source_coordinates":"32.0852999,34.78176759999999","destination_coordinates":"32.7940463,34.989571"}

headers = {
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "waze.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())