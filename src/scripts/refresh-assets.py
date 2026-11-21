import requests
from bs4 import BeautifulSoup
import json
import time
import os
import sys
import unicodedata
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.environ["GOOGLE_SCRIPTS_WEBHOOK_URL"]
AUTH_TOKEN = os.environ["GOOGLE_SCRIPTS_AUTH_TOKEN"]

# Output key -> accepted Fundamentus headers (normalized). Key order = DB tab columns.
COLUMNS = {
  "ticker": ["papel"],
  "cotacao": ["cotacao"],
  "p_l": ["pl"],
  "p_vp": ["pvp"],
  "psr": ["psr"],
  "dy": ["divyield"],
  "p_ativo": ["pativo"],
  "p_capgiro": ["pcapgiro"],
  "p_ebit": ["pebit"],
  "p_ativcirc": ["pativcircliq"],
  "ev_ebit": ["evebit"],
  "ev_ebitda": ["evebitda"],
  "mrg_ebit": ["mrgebit"],
  "mrg_liq": ["mrgliq"],
  "liq_corr": ["liqcorr"],
  "roic": ["roic"],
  "roe": ["roe"],
  "liq_2meses": ["liq2meses"],
  "patrimonio_liq": ["patrimliq"],
  "div_bruta_patr": ["divbrutpatrim", "divliqpatrim"],  # Fundamentus now shows net debt
  "cresc_5a": ["crescrec5a"],
}

def normalize(text):
  text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
  return "".join(ch for ch in text.lower() if ch.isalnum())

def map_headers(table):
  headers = [normalize(th.get_text()) for th in table.find_all("th")]
  index, missing = {}, []
  for key, names in COLUMNS.items():
    found = next((headers.index(n) for n in names if n in headers), None)
    if found is None: missing.append(key)
    else: index[key] = found
  if missing:
    raise RuntimeError(f"Fundamentus headers changed, missing: {missing}. Got: {headers}")
  extra = set(range(len(headers))) - set(index.values())
  if extra:
    print(f"Warning: unmapped Fundamentus columns: {[headers[i] for i in sorted(extra)]}")
  return index, len(headers)

def main():
  headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
  }
  
  try:
    url = "https://www.fundamentus.com.br/resultado.php"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
      raise RuntimeError(f"HTTP error: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "resultado"})
    
    if not table:
      raise RuntimeError("Table not found. Blocked by the website or changed URL?")

    index, n_cols = map_headers(table)
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
      if len(cols) != n_cols:
        raise RuntimeError(f"Row has {len(cols)} cells, header has {n_cols}")
      asset = {key: clean(cols[i].text) for key, i in index.items()}
      asset["ticker"] = cols[index["ticker"]].text.strip()
      assets.append(asset)

    print(f"Extracted {len(assets)} assets")

    payload = { "token": AUTH_TOKEN, "assets": assets }
    r = requests.post(WEBHOOK_URL, json=payload)
    print(f"Webhook: {r.status_code} - {r.text}")
    if r.status_code != 200:
      raise RuntimeError("Webhook failed")

  except Exception as e:
    print(f"Fatal error: {e}")
    sys.exit(1)

if __name__ == "__main__":
  main()
