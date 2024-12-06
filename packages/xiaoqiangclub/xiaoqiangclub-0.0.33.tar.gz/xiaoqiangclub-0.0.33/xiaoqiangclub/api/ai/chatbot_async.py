# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/23 12:25
# 文件名称： chatbot.py
# 项目描述： 微信对话开发平台API
# 开发工具： PyCharm
import inspect
import time
import json
import uuid
import hashlib
from typing import Optional, Union, Dict, List
import asyncio
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.utils.network_utils import get_response_async  # 导入异步请求工具


class WeChatBotAPIAsync:
    def __init__(self, app_id: str, token: str, encoding_aes_key: str, user_id: str):
        """
        微信对话开发平台API（异步版）
        接入之前，需要先在对话平台官网创建机器人，并在应用绑定中申请开放 API 的接入参数。

        :param app_id: 微信对话开放平台：管理 > 应用绑定 > 开放API 获取
        :param token:
        :param encoding_aes_key:
        :param user_id: 微信对话开放平台：管理 > 基础设置 > 成员权限 > 用户ID 获取
        """
        self.app_id = app_id
        self.token = token
        self.aes_key = encoding_aes_key
        self.user_id = user_id
        self.nonce = 'XiaoqiangClub'
        self.access_token = None
        print('请使用 async with 或调用 initialize 方法初始化 API...')

    async def initialize(self):
        """异步初始化，获取 access_token"""
        await self._get_access_token()

    def __generate_signature(self, unix_timestamp: str, body: Optional[str] = "") -> str:
        """
        生成请求签名的函数（保持同步）
        """
        s = self.token + str(unix_timestamp) + self.nonce + hashlib.md5(body.encode()).hexdigest()
        sign = hashlib.md5(s.encode()).hexdigest()
        log.debug(f"生成签名：{sign}")
        return sign

    def __get_headers(self, body, get_access_token: bool = False) -> dict:
        """
        生成请求头（保持同步）
        """
        timestamp = str(int(time.time()))
        if get_access_token:
            headers = {
                'X-APPID': self.app_id,
                'content-type': 'application/json',
                'request_id': str(uuid.uuid4()),
                'timestamp': timestamp,
                'nonce': self.nonce,
                'sign': self.__generate_signature(timestamp, json.dumps(body))
            }
        else:
            if not self.access_token:
                asyncio.run(self._get_access_token())  # 异步获取 access_token

            headers = {
                'X-OPENAI-TOKEN': self.access_token,
                'content-type': 'application/json',
                'request_id': str(uuid.uuid4()),
                'timestamp': timestamp,
                'nonce': self.nonce,
                'sign': self.__generate_signature(timestamp, json.dumps(body))
            }

        return headers

    async def _get_response(self, url: str, body: dict = None, get_access_token: bool = False,
                            return_json: bool = True, post: bool = False) -> Optional[Union[Dict, str]]:
        """
        异步获取响应
        """
        try:
            caller = inspect.currentframe().f_back.f_code.co_name
            headers = self.__get_headers(body, get_access_token)
            if body or post:
                response = await get_response_async(url, headers=headers, json=body)
            else:
                response = await get_response_async(url, headers=headers)

            log.debug(
                f'[{caller}] 请求方式：{response.request.method}，响应状态码: {response.status_code}，响应内容:{response.text}')

            if response.status_code == 200:
                return response.json() if return_json else response.text

            log.error(f"请求失败，状态码：{response.status_code}，响应内容：{response.text}")
            return None

        except Exception as e:
            log.error(f"网络请求发生错误: {e}")
            return None

    @staticmethod
    def _get_data(get_key: str, json_data: dict, return_raw_data: bool = False) -> Optional[Union[str, int]]:
        """
        从响应中获取数据（保持同步）
        """
        if return_raw_data:
            return json_data

        if not json_data:
            log.error(f"获取 {get_key} 失败：{json_data}")
            return None

        value = json_data.get('data', {}).get(get_key)
        if value:
            log.debug(f"获取到{get_key}：{value}")
            return value
        else:
            log.error(f"获取 {get_key} 失败：{json_data.get('msg')}")
            return None

    async def _get_access_token(self) -> Optional[str]:
        """异步获取access_token"""
        body = {"account": self.user_id}
        json_data = await self._get_response('https://openaiapi.weixin.qq.com/v2/token', body, True)
        self.access_token = self._get_data('access_token', json_data)
        return self.access_token

    async def keywords_exists(self, keywords: str) -> bool:
        """
        判断关键词是否已经存在
        :param keywords: 关键词
        :return:
        """
        reply = await self.get_answer(keywords)
        if reply != '请问你是想了解以下问题吗？' and reply:  # 说明不存在
            return True

        return False

    async def add_question(self, question: str, answers: Union[str, List[str]], question_class: str = '关键字',
                           similar_questions: List[str] = None, disable: bool = False, mode: int = 0,
                           threshold: str = '0.9', return_raw_data: bool = False) -> Optional[str]:
        """
        插入知识问答（异步）
        """
        exist = await self.keywords_exists(question)
        if exist and mode == 2:
            log.info(f"关键词 {question} 已存在，跳过")
            return None

        if not exist and mode == 2:
            mode = 0

        data = {
            "mode": mode,
            "data": [
                {
                    "skill": question_class,
                    "intent": question,
                    "threshold": threshold,
                    "disable": disable,
                    "questions": similar_questions,
                    "answers": [answers] if isinstance(answers, str) else answers
                }
            ]
        }
        json_data = await self._get_response('https://openaiapi.weixin.qq.com/v2/bot/import/json', data)
        return self._get_data('task_id', json_data, return_raw_data)

    async def publish_bot(self, return_raw_data: bool = False) -> Optional[str]:
        """异步发布机器人"""
        json_data = await self._get_response("https://openaiapi.weixin.qq.com/v2/bot/publish", body={}, post=True)
        task_id = self._get_data('task_id', json_data, return_raw_data)
        if task_id:
            log.info(f"发布成功，任务ID：{task_id}")
        else:
            log.error(f"发布失败，{json_data}")
        return task_id

    async def get_task_info(self, task_id: str) -> Optional[dict]:
        """查询异步请求详情"""
        data = {'task_id': task_id}
        return await self._get_response('https://openaiapi.weixin.qq.com/v2/async/fetch', data)

    async def get_publish_progress(self, return_raw_data: bool = False) -> Optional[Union[dict, int]]:
        """获取机器人发布进度"""
        data = {"env": "online"}
        json_data = await self._get_response("https://openaiapi.weixin.qq.com/v2/bot/effective_progress", data)
        return self._get_data('progress', json_data, return_raw_data)

    async def __get_query_signature(self) -> Optional[str]:
        """获取调用签名"""
        try:
            data = {'userid': self.user_id}
            url = f'https://chatbot.weixin.qq.com/openapi/sign/{self.token}'
            response = await get_response_async(url, data=data)
            if response.status_code == 200:
                json_data = response.json()
                signature = json_data.get('signature')
                log.debug(f'获取 signature: {signature}')
                return signature

        except Exception as e:
            log.error(f"获取 signature 失败：{e}")
            return None

    async def get_answer(self, query: str, return_node_name: bool = False,
                         return_raw_data: bool = False) -> Optional[Union[dict, tuple, str]]:
        """获取机器人智能对话答案"""
        try:
            signature = await self.__get_query_signature()
            if not signature:
                return None

            params = {'signature': signature, 'query': query}
            url = f'https://chatbot.weixin.qq.com/openapi/aibot/{self.token}'
            response = await get_response_async(url, data=params)
            if response.status_code == 200:
                json_data = response.json()
                if return_raw_data:
                    return json_data

                if return_node_name:
                    return json_data.get('node_name')

                return json_data.get('answer')
        except Exception as e:
            log.error(f"获取智能对话失败: {e}")
            return None

    async def __aenter__(self):
        """进入上下文管理器时获取 access_token"""
        await self._get_access_token()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        pass
