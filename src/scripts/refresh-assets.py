import requests
from bs4 import BeautifulSoup
import json
import time

WEBHOOK_URL = ""
AUTH_TOKEN = ""

def main():
  headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
  } 

  url = "https://www.fundamentus.com.br/resultado.php"
  response = requests.get(url, headers=headers)
  
  if response.status_code != 200:
    print(f"HTTP error: {response.status_code}")

  print("Parsing HTML...")

if __name__ == "__main__":
  main()
