import requests

response = requests.get(
    "https://raw.githubusercontent.com/lbreede/sidefx-versions/main/json/builds.json"
)

# print(dir(response))
data = response.json()

print(data["Houdini_19_5"]["Production_Builds"])
