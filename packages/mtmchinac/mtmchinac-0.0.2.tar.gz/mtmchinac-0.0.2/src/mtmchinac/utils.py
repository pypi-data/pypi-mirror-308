import base64
import hashlib
import hmac
import time
import urllib.parse
import urllib.request

from typing import Tuple, Dict, Mapping


def request(request_url, headers: dict = None, body: bytes = None, method='GET') -> Tuple[int, str]:
    """
    发送请求
    :param request_url:  请求地址
    :param headers: 请求头
    :param body: 请求体
    :param method: 请求方法
    :return: 状态码，响应体
    """
    req = urllib.request.Request(
        request_url,
        data=body,
        headers=headers or {},
        method=method,
    )
    res = urllib.request.urlopen(req)
    return res.getcode(), res.read().decode('utf-8')


def sha_hmac256_signature(key: str, msg: str) -> str:
    """
    base64 hmac256加密
    :param key: 密钥
    :param msg: 消息
    :return: 加密后的字符串
    """
    h = hmac.new(bytearray(key, 'utf-8'), bytearray(msg, 'utf-8'), hashlib.sha256)
    return str(base64.encodebytes(h.digest()).strip(), 'utf-8')


def generate_headers() -> Dict[str, str]:
    """
    生成请求头
    :return: 请求头字典
    """
    return {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept-Encoding': '*',
        'Date': time.strftime("%Y-%m-%dT%H:%M:%S +0800", time.localtime())
    }


def _percent_encode(url_string: str) -> str:
    """
    转成url通信标准RFC 3986
    :param url_string: 原始url
    :return: 转换后的url
    """
    check_dict = {'+': '%20', '*': '%2A', '~': '%7E'}
    for k, v in check_dict.items():
        url_string = url_string.replace(k, v)
    return url_string


def percent_url_encode_params(params: Mapping) -> str:
    """
    encodeurl参数
    :param params: 参数
    :return: 转换后的参数
    """
    url_string = urllib.parse.urlencode(params)
    return _percent_encode(url_string)


def percent_url_encode_str(url_string: str) -> str:
    """
    encodeurl字符串
    :param url_string: 字符串
    :return: 转换后的字符串
    """
    url_string = urllib.parse.quote(url_string)
    return _percent_encode(url_string)


def camel_key_to_snake(ori_dict: dict) -> dict:
    """将字典键名的驼峰命名转换为下划线命名"""
    import re
    result = {}
    for k, v in ori_dict.items():
        new_key = re.sub(r'([a-z])([A-Z])', r'\1_\2', k).lower()
        if isinstance(v, dict):
            result[new_key] = camel_key_to_snake(v)
        elif isinstance(v, list):
            result[new_key] = [camel_key_to_snake(i) if isinstance(i, dict) else i for i in v]
        else:
            result[new_key] = v
    return result