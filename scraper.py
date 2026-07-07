import requests
from bs4 import BeautifulSoup
import json

def fetch_antutu_live():
    url = "https://antutu.com/web/ranking"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        phones_list = []
        
        # Searching for the structural rank items from the live web view
        items = soup.select('.rank-list li, .ranking-list li, tr')
        
        for item in items:
            try:
                name_el = item.select_one('.name, .title') or item.find('td', class_='name')
                score_el = item.select_one('.score, .total-score') or item.find('td', class_='score')
                
                if name_el and score_el:
                    name = name_el.text.strip()
                    score = score_el.text.strip()
                    
                    if name and score:
                        phones_list.append({
                            "rank": str(len(phones_list) + 1),
                            "name": name,
                            "score": score
                        })
            except:
                continue
                
        return phones_list if len(phones_list) > 0 else None
    except:
        return None

if __name__ == "__main__":
    live_data = fetch_antutu_live()
    if live_data:
        output = {"2026": live_data}
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
