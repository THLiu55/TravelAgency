import base64
import urllib
import requests

API_KEY = "4aXwaMWTIIV6kWj8SVEpLsG8"
SECRET_KEY = "0x4q77up034G8ed2prWVyfrg8YKy0Fb0"


def main(file):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token=" + get_access_token()

    payload = get_file_content_as_base64(file, True)
    payload = "image=" + payload
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def get_file_content_as_base64(file, urlencoded=False):
    """
    获取文件base64编码
    :param file: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    content = base64.b64encode(file.read()).decode("utf8")
    if urlencoded:
        content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
