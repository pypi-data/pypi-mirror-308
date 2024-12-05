import requests
from .parser import ResponseParser


def build_api_url(action, hostname=None, ipv6=None, mail=None, key=None):
    ipv6 = ipv6 or ""
    mail = mail or ""
    base_url = f"https://ddnsapi-v6.open.ad.jp/api/{action}/"

    if action == "new" and hostname:
        return f"{base_url}?{hostname}={ipv6},{mail}"
    elif action == "renew" and key:
        return f"{base_url}?{key}={ipv6},{mail}"
    else:
        raise ValueError("Invalid parameters for the specified action.")


def make_api_request(action, hostname=None, ipv6=None, mail=None, key=None):
    url = build_api_url(action, hostname, ipv6, mail, key)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")


def new(hostname, ipv6=None, mail=None):
    raw_response = make_api_request("new", hostname, ipv6, mail)
    parser = ResponseParser(raw_response)
    result = parser.get_result()

    if result["status"] == "OK":
        return parser.parsed_data
    else:
        error_message = f"Error: {result['message_ja']} ({result['message_en']})"
        raise RuntimeError(error_message)


def renew(key, ipv6=None, mail=None):
    raw_response = make_api_request("renew", None, ipv6, mail, key)
    parser = ResponseParser(raw_response)
    result = parser.get_result()

    if result["status"] == "OK":
        return parser.parsed_data
    else:
        error_message = f"Error: {result['message_ja']} ({result['message_en']})"
        raise RuntimeError(error_message)
