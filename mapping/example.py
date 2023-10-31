import requests

url = "https://graphhopper.com/api/1/route"

query = {
    "key" : "5a3759fd-c16e-4523-9991-c7fd834de72b"
}

def coords_to_decimal(degrees, minutes, seconds):
    return degrees + minutes / 60.0 + seconds / 3600.0


payload = {
    "points" : [
        [
            coords_to_decimal(71, 20, 2),
            coords_to_decimal(42, 22, 32), #my address
        ],
        [
            coords_to_decimal(71, 20, 41),
            coords_to_decimal(42, 22, 23), #claypit hill school
        ]
    ],
    "vehicle" : "foot",
    "locale" : "en",
    "elevation" : True,
    "instructions" : True, #just to confirm it works
    "calc_points" : True,
    "points_encoded" : False
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers, params=query)

data = response.json()
print(data)