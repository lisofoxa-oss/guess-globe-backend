from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
import hmac
import hashlib
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = "8164563339:AAGz6nMXwaXkBSNdCF0-UwtuBVvZd1-ApLA"

FLAGS = [
    {"id": 1, "country": "Russia", "image_url": "https://upload.wikimedia.org/wikipedia/en/f/f3/Flag_of_Russia.svg"},
    {"id": 2, "country": "United States", "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg"},
    {"id": 3, "country": "France", "image_url": "https://upload.wikimedia.org/wikipedia/en/c/c3/Flag_of_France.svg"},
    {"id": 4, "country": "Germany", "image_url": "https://upload.wikimedia.org/wikipedia/en/b/ba/Flag_of_Germany.svg"},
    {"id": 5, "country": "Japan", "image_url": "https://upload.wikimedia.org/wikipedia/en/9/9e/Flag_of_Japan.svg"},
    {"id": 6, "country": "Brazil", "image_url": "https://upload.wikimedia.org/wikipedia/en/0/05/Flag_of_Brazil.svg"},
    {"id": 7, "country": "Canada", "image_url": "https://upload.wikimedia.org/wikipedia/en/c/cf/Flag_of_Canada.svg"},
    {"id": 8, "country": "Australia", "image_url": "https://upload.wikimedia.org/wikipedia/en/8/88/Flag_of_Australia.svg"},
    {"id": 9, "country": "China", "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg"},
    {"id": 10, "country": "India", "image_url": "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg"},
]

def parse_telegram_data(init_data):
    if not init_data or init_data == "undefined":
        raise HTTPException(status_code=400, detail="Missing init data")
    try:
        pairs = init_data.split("&")
        params = {}
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                import urllib.parse
                params[key] = urllib.parse.unquote(value)
        if "hash" not in params:
            raise HTTPException(status_code=400, detail="Missing hash")
        hash_val = params.pop("hash")
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(params.items()))
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        if computed_hash != hash_val:
            raise HTTPException(status_code=403, detail="Invalid hash")
        if "user" not in params:
            raise HTTPException(status_code=400, detail="Missing user data")
        user = json.loads(params["user"])
        return user["id"]
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid init data")

@app.get("/api/question")
def get_question(authorization: str = Header(...)):
    user_id = parse_telegram_data(authorization)
    flag = random.choice(FLAGS)
    other = [f["country"] for f in FLAGS if f["country"] != flag["country"]]
    options = [flag["country"]] + random.sample(other, 3)
    random.shuffle(options)
    return {
        "question_id": flag["id"],
        "image_url": flag["image_url"],
        "options": options,
        "correct_answer": flag["country"]
    }

@app.post("/api/answer")
def answer():
    return {"correct": True}  # Для MVP — всегда "верно" (можно улучшить позже)