import requests

response = requests.get(
    "https://raw.githubusercontent.com/lbreede/sidefx-versions/main/json/builds.json"
)
data = response.json()
print(data["Houdini_19_5"]["Production_Builds"][0])
