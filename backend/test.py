from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import hashlib
import random

app = Flask(__name__)
CORS(app)


# --------------------------------------------------------
# PRICE SCRAPER: tries to detect price-like values in HTML
# --------------------------------------------------------
def try_scrape_price(html):
    """
    Very loose price detector.
    Looks for patterns like:
        '12 TON', '3.5 TH', 'Price: 10', '1500⭐', '125 Stars'
    Returns float or None.
    """

    text = " ".join(html.split())  # Normalize spacing

    patterns = [
        r"(\d+\.?\d*)\s*TON",
        r"TON\s*(\d+\.?\d*)",
        r"(\d+\.?\d*)\s*Stars",
        r"Stars\s*(\d+\.?\d*)",
        r"Price[:\s]+(\d+\.?\d*)",
        r"(\d+\.?\d*)\s*\$",
    ]

    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except:
                pass

    return None


# --------------------------------------------------------
# FALLBACK: deterministic fake price
# --------------------------------------------------------
def generate_fake_price(nft_id: str | None):
    if not nft_id:
        nft_id = str(random.random())

    h = hashlib.sha256(nft_id.encode()).hexdigest()
    seed = int(h[:8], 16)
    random.seed(seed)

    return round(random.uniform(0.3, 35.0), 2)  # TON-like price


# --------------------------------------------------------
# MAIN ENDPOINT
# --------------------------------------------------------
@app.route("/api/nft")
def nft():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "missing ?url="}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        # --- Meta extraction ---
        title_meta = soup.find("meta", property="og:title")
        description_meta = soup.find("meta", property="og:description")
        image_meta = soup.find("meta", property="og:image")

        title_text = title_meta["content"] if title_meta else ""
        if "#" in title_text:
            name, nft_id = title_text.split("#", 1)
            name = name.strip()
            nft_id = nft_id.strip()
        else:
            name = title_text
            nft_id = None

        # --- Table extraction ---
        table_data = {}
        table = soup.find("table", class_="tgme_gift_table")
        if table:
            for row in table.find_all("tr"):
                cols = row.find_all(["th", "td"])
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    val = cols[1].get_text(strip=True)
                    table_data[key] = val

        # --- PRICE SCRAPER ---
        scraped_price = try_scrape_price(r.text)

        # --- PRICE FALLBACK ---
        if scraped_price is None:
            scraped_price = generate_fake_price(nft_id)
            price_found = False
        else:
            price_found = True

        return jsonify({
            "id": nft_id,
            "name": name,
            "description": description_meta["content"] if description_meta else None,
            "image": image_meta["content"] if image_meta else None,
            "table": table_data,
            "price": scraped_price,
            "price_found": price_found,
            "url": url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
