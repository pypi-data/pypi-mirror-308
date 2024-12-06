# data_format_converter.py

import requests
import json
from AI_agent.config import Config

class DataFormatConverter:
    @classmethod
    def get_access_token(cls):
        """ 使用API Key，Secret Key 获取access_token """
        params = {
            'grant_type': 'client_credentials',
            'client_id': Config.CLIENT_ID,
            'client_secret': Config.CLIENT_SECRET
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(Config.TOKEN_URL, params=params, headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError异常
        return response.json().get("access_token")

    def __init__(self, convert_prompt_prefix):
        self.convert_prompt_prefix = convert_prompt_prefix

    def convert_to_json_format(self, orchestration_result):
        """
        将function_plan_result转换为JSON格式，并通过大模型进行格式转换。
        :param orchestration_result: 待转换的数据
        :return: 转换后的JSON格式数据或None（如果请求失败）
        """
        if orchestration_result is None:
            return None
        full_prompt = self.convert_prompt_prefix + orchestration_result
        access_token = self.get_access_token()
        url = f"{Config.API_URL}?access_token={access_token}"
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # 检查请求是否成功
            response_data = response.json()
            reply = response_data.get('result', {})
            return reply
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None