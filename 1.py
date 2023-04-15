import requests as req

address = "Beijing University OF Technology Beijing China"
url = 'https://nominatim.openstreetmap.org/search?q={}&format=json'.format(address)
response = req.get(url).json()
if len(response) > 0:
    print(response)
else:
    print(response)
