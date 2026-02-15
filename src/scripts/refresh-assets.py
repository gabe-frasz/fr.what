from curl_cffi import requests

url = "https://www.fundamentus.com.br/resultado.php"
response = requests.get(url, impersonate="chrome110") 

if response.status_code != 200:
  print("Failed to fetch data from Fundamentus")
  print(response.text)
  exit(1)

print("Fetched data from Fundamentus")
