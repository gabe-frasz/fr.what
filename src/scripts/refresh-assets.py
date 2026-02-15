import requests
from bs4 import BeautifulSoup
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.environ["GOOGLE_SCRIPTS_WEBHOOK_URL"]
AUTH_TOKEN = os.environ["GOOGLE_SCRIPTS_AUTH_TOKEN"]

def main():
  headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
  }
  
  try:
    url = "https://www.fundamentus.com.br/resultado.php"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
      print(f"HTTP error: {response.status_code}")
      return

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "resultado"})
    
    if not table:
      print("Table not found. Blocked by the website or changed URL?")
      return

    rows = table.find_all("tr")[1:] # skip header
    assets = []

    def clean(text):
      text = text.strip()
      if text == "": return 0
      val = text.replace(".", "").replace(",", ".").replace("%", "")
      try:
        num = float(val)
        if "%" in text: num /= 100
        return num
      except:
        return text

    for row in rows:
      cols = row.find_all("td")
      assets.append({
        "ticker": cols[0].text.strip(),
        "cotacao": clean(cols[1].text),
        "p_l": clean(cols[2].text),
        "p_vp": clean(cols[3].text),
        "psr": clean(cols[4].text),
        "dy": clean(cols[5].text),
        "p_ativo": clean(cols[6].text),
        "p_capgiro": clean(cols[7].text),
        "p_ebit": clean(cols[8].text),
        "p_ativcirc": clean(cols[9].text),
        "ev_ebit": clean(cols[10].text),
        "ev_ebitda": clean(cols[11].text),
        "mrg_ebit": clean(cols[12].text),
        "mrg_liq": clean(cols[13].text),
        "liq_corr": clean(cols[14].text),
        "roic": clean(cols[15].text),
        "roe": clean(cols[16].text),
        "liq_2meses": clean(cols[17].text),
        "patrimonio_liq": clean(cols[18].text),
        "div_bruta_patr": clean(cols[19].text),
        "cresc_5a": clean(cols[20].text),
      })

    print(f"Extracted {len(assets)} assets")

    payload = { "token": AUTH_TOKEN, "assets": assets }
    r = requests.post(WEBHOOK_URL, json=payload)
    print(f"Webhook: {r.status_code} - {r.text}")

  except Exception as e:
    print(f"Fatal error: {e}")

if __name__ == "__main__":
  main()
