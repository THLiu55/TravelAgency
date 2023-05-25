import requests
import random
import json


API_KEY = "w22DiAAmDvd1aUotmZCCTFjY"
SECRET_KEY = "cmdgasS2vG4wgcpXyv00wGCtG10GrRad"


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


token=get_access_token()

# q: sentence in original language; from_lang: current language; dst_lang:  target language; # Return:translated sentences
def translator(q, from_lang, to_lang):
    if q == "":
        return ""
    url = 'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=' + token

    headers = {'Content-Type': 'application/json'}
    payload = {'q': q, 'from': from_lang, 'to': to_lang, 'termIds': ''}

    result = requests.post(url, params=payload, headers=headers).json()
    return result.get('result').get('trans_result')[0].get('dst')



def fill_translations(file_path, from_language, destination_language, translator):
    """
    Fills in the translations in the specified language file using the translator function.

    Args:
        file_path (str): The path to the language file.
        from_language (str): The language code of the original language.
        destination_language (str): The language code of the destination language.
        translator (function): The translator function to use.

    Returns:
        None
    """
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('msgid'):
                msgid = line.split('"')[1]
                msgstr = lines[i+1].split('"')[1]
                if not msgstr:
                    translation = translator(msgid, from_language, destination_language)
                    lines[i+1] = f'msgstr "{translation}"'
        f.seek(0)
        f.write('\n'.join(lines))
        f.truncate()



if __name__ == "__main__":
    # fill_translations('./zh/LC_MESSAGES/messages.po', 'en', 'zh', translator)
    print(translator("here", "en", "zh"))

