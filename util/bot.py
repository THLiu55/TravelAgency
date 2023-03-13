import os, json, requests

bot_choices = ["WXBOT", "CHATGPT", "FALLBACK"]
WXBOT_TOKEN = os.environ.get("WXBOT_TOKEN")
WXBOT_GET_SIGNATURE_URL_PREFIX = os.environ.get("WXBOT_GET_SIGNATURE_URL_PREFIX")
WXBOT_GET_RESPONSE_URL_PREFIX = os.environ.get("WXBOT_GET_RESPONSE_URL_PREFIX")


# core function


def get_wxbot_signature(userid):
    url = WXBOT_GET_SIGNATURE_URL_PREFIX + WXBOT_TOKEN
    response = requests.post(url, json={"userid": userid}, timeout=5)
    signature = json.loads(response.text)["signature"]
    return signature


def get_wxbot_answer(message, signature):
    url = WXBOT_GET_RESPONSE_URL_PREFIX + WXBOT_TOKEN
    response = requests.post(
        url, json={"signature": signature, "query": message}, timeout=5
    )
    answer = json.loads(response.text)["answer"]
    return answer
