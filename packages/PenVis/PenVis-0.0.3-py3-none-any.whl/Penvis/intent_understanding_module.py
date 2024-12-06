# intent_understanding_module.py

import requests
import json
from PenVis.config import Config

class IntentUnderstandingModule:
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

    def __init__(self, intent_prompt_prefix):
        self.intent_prompt_prefix = intent_prompt_prefix

    def understand_intent(self, user_need):
        """ 理解用户意图并获取API响应 """
        full_prompt = self.intent_prompt_prefix + user_need
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