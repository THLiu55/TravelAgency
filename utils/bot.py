import os, json, requests

# bot_choices = ["WXBOT", "CHATGPT", "FALLBACK"]
BOT_CHOICE = os.environ.get("BOT_CHOICE")
WXBOT_TOKEN = os.environ.get("WXBOT_TOKEN")
WXBOT_GET_SIGNATURE_URL_PREFIX = os.environ.get("WXBOT_GET_SIGNATURE_URL_PREFIX")
WXBOT_GET_RESPONSE_URL_PREFIX = os.environ.get("WXBOT_GET_RESPONSE_URL_PREFIX")

BOT_CMD_RESP_DICT = json.loads(os.environ.get("BOT_CMD_RESP_DICT"))

TRANSLATE_PROVIDER = os.environ.get("TRANSLATE_PROVIDER")
LIBRETRANSLATE_URL = os.environ.get("LIBRETRANSLATE_URL")
BAIDUBCE_TRANSLATE_URL = os.environ.get("BAIDUBCE_TRANSLATE_URL")
BAIDUBCE_TRANSLATE_TOKEN = os.environ.get("BAIDUBCE_TRANSLATE_TOKEN")
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

def translate_message(message, source_lang, target_lang):
    if TRANSLATE_PROVIDER == "BAIDU":
        if message == "":
            return ""
        token = BAIDUBCE_TRANSLATE_TOKEN
        url = BAIDUBCE_TRANSLATE_URL + token

        headers = {'Content-Type': 'application/json'}
        payload = {'q': message, 'from': source_lang, 'to': target_lang, 'termIds': ''}

        result = requests.post(url, params=payload, headers=headers).json()
        return result.get('result').get('trans_result')[0].get('dst')
    elif TRANSLATE_PROVIDER == "LIBRETRANSLATE":
        url = LIBRETRANSLATE_URL
        response = requests.post(
            url, json={"q": message, "source": source_lang, "target": target_lang}, timeout=5
        )
        answer = json.loads(response.text)["translatedText"]
        return answer