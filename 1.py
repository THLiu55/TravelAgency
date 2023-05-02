import requests as req

address = "??????"
url = 'https://nominatim.openstreetmap.org/search?q={}&format=json'.format(address.encode("utf-8"))
response = req.get(url).json()
if len(response) > 0:
    print(response)
else:
    print(response)
