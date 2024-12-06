import requests
import json
import os
import logging
import re
import pymysql
from contextlib import contextmanager

# 设置日志记录
logging.basicConfig(level=logging.INFO)

# 连接到数据库的函数，作为上下文管理器
@contextmanager
def connect_db(config):
    connection = pymysql.connect(**config)
    try:
        yield connection
    finally:
        connection.close()

# 数据库连接配置
db_config = {
    'host': '116.204.70.1',
    'port': 3306,
    'user': 'root',
    'password': 'VisPen1109*_hz_qwer',
    'database': 'pen_vis_test',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 连接到数据库
def connect_db():
    return pymysql.connect(**db_config)

class MemoryModule:
    def __init__(self, task_id, db_config):
        # 初始化一个空的字典来存储记忆
        self.memory = {}
        self.task_id = task_id
        self.db_config = db_config
        # 连接到数据库
        self.connection = pymysql.connect(**self.db_config)

    def __del__(self):
        # 对象销毁时关闭数据库连接
        self.connection.close()

    def record(self, module_name, result):
        """
        记录并更新指定模块的输出结果，并存储到数据库中。

        参数:
        module_name (str): 模块的名称，作为字典的键和数据库表的列名。
        result (any): 模块的输出结果，需要是可以转换为字符串的数据类型。
        """
        # 将结果存储在字典中，键为模块名称
        self.memory[module_name] = result
        print(f"Recorded result for module '{module_name}': {result}")

        # 存储到数据库
        self.store_to_db(module_name, result)

    def store_to_db(self, module_name, result):
        """
        将指定模块的结果更新到数据库中。

        参数:
        module_name (str): 模块的名称，作为数据库表的列名。
        result (any): 模块的输出结果。
        """
        try:
            with self.connection.cursor() as cursor:
                # 构建 SQL 更新语句
                # 假设表名为 pen_agent_memory，且有一个 task_id 字段用于标识记录
                sql = f"UPDATE pen_agent_memory SET {module_name} = %s WHERE task_id = %s"

                # 执行更新操作
                cursor.execute(sql, (result, self.task_id))

            # 提交事务
            self.connection.commit()
            print(f"'{module_name}' 已保持至记忆模块.")
        except Exception as e:
            # 如果出现异常，回滚事务并打印错误
            self.connection.rollback()
            print(f"An error occurred while updating the result for module '{module_name}': {e}")

    def get_memory(self):
        """
        获取所有已记录的记忆。

        返回:
        dict: 包含所有模块名称及其对应结果的字典。
        """
        return self.memory

class IntentUnderstandingModule:
    API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-turbo-8k"
    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
    CLIENT_ID = "uFVD6G313UrqawNHbCXuK6jj"
    CLIENT_SECRET = "SSzm3rixotMM5iVdaUcqC8ei4fJmzMRq"

    @classmethod
    def get_access_token(cls):
        """ 使用API Key，Secret Key 获取access_token """
        params = {
            'grant_type': 'client_credentials',
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(cls.TOKEN_URL, params=params, headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError异常
        return response.json().get("access_token")

    def __init__(self, intent_prompt_prefix):
        self.intent_prompt_prefix = intent_prompt_prefix

    def understand_intent(self, user_need):
        """ 理解用户意图并获取API响应 """
        full_prompt = self.intent_prompt_prefix + user_need
        access_token = self.get_access_token()
        url = f"{self.API_URL}?access_token={access_token}"

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
            # 假设返回的JSON中有一个'result'键，其值是一个包含回复的字典或列表
            reply = response_data.get('result', {})
            # 根据实际API返回的结构，可能需要进一步处理reply以获取最终的文本内容
            return reply
        except requests.RequestException as e:
            # 如果请求失败，打印错误信息并返回None或适当的默认值
            print(f"请求失败: {e}")
            return None


class FunctionPlanningModule:
    API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-turbo-8k"
    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
    CLIENT_ID = "uFVD6G313UrqawNHbCXuK6jj"
    CLIENT_SECRET = "SSzm3rixotMM5iVdaUcqC8ei4fJmzMRq"

    @classmethod
    def get_access_token(cls):
        """ 使用API Key，Secret Key 获取access_token """
        params = {
            'grant_type': 'client_credentials',
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(cls.TOKEN_URL, params=params, headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError异常
        return response.json().get("access_token")

    def __init__(self, plan_function_prompt_prefix):
        self.plan_function_prompt_prefix = plan_function_prompt_prefix

    def plan_function(self, intent_result):
        """ 根据用户意图进行功能规划并获取API响应 """
        full_prompt = self.plan_function_prompt_prefix + intent_result
        access_token = self.get_access_token()
        url = f"{self.API_URL}?access_token={access_token}"

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
            # 假设返回的JSON中有一个'result'键，其值是一个包含回复的字典或列表
            # reply = response_data.get('result', {})
            reply = response_data.get('result', '')
            # 检查回复结果
            if reply == "无适配方案":
                print("无适配方案")
                return None  # 终止后续程序
            # 根据实际API返回的结构，可能需要进一步处理reply以获取最终的文本内容
            return reply
        except requests.RequestException as e:
            # 如果请求失败，打印错误信息并返回None或适当的默认值
            print(f"请求失败: {e}")
            return None


class FunctionOrchestrationModule:
    API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-turbo-8k"
    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
    CLIENT_ID = "uFVD6G313UrqawNHbCXuK6jj"
    CLIENT_SECRET = "SSzm3rixotMM5iVdaUcqC8ei4fJmzMRq"

    @classmethod
    def get_access_token(cls):
        """ 使用API Key，Secret Key 获取access_token """
        params = {
            'grant_type': 'client_credentials',
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(cls.TOKEN_URL, params=params, headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError异常
        return response.json().get("access_token")

    def __init__(self, orchestration_prompt_prefix):
        self.orchestration_prompt_prefix = orchestration_prompt_prefix

    def plan_orchestration(self, function_plan_result):
        """ 检索功能池并获取API响应 """
        if function_plan_result is None:
            # 如果function_plan_result为None，则直接返回，不再继续执行
            return

        full_prompt = self.orchestration_prompt_prefix + function_plan_result
        access_token = self.get_access_token()
        url = f"{self.API_URL}?access_token={access_token}"

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
            # 假设返回的JSON中有一个'result'键，其值是一个包含回复的字典或列表
            reply = response_data.get('result', {})
            # 根据实际API返回的结构，可能需要进一步处理reply以获取最终的文本内容
            return reply
        except requests.RequestException as e:
            # 如果请求失败，打印错误信息并返回None或适当的默认值
            print(f"请求失败: {e}")
            return None


class DataFormatConverter:
    API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-4.0-turbo-8k"
    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
    CLIENT_ID = "uFVD6G313UrqawNHbCXuK6jj"
    CLIENT_SECRET = "SSzm3rixotMM5iVdaUcqC8ei4fJmzMRq"

    @classmethod
    def get_access_token(cls):
        """ 使用API Key，Secret Key 获取access_token """
        params = {
            'grant_type': 'client_credentials',
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post(cls.TOKEN_URL, params=params, headers=headers)
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
            # 如果function_plan_result为None，则直接返回None
            return None

        # 拼接提示词模板和function_plan_result
        full_prompt = self.convert_prompt_prefix + orchestration_result

        # 获取access_token
        access_token = self.get_access_token()
        url = f"{self.API_URL}?access_token={access_token}"

        # 构建请求体
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
            # 发送请求
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # 检查请求是否成功
            response_data = response.json()

            # 假设返回的JSON中有一个'result'键，其值是我们需要的转换结果
            reply = response_data.get('result', {})

            # 返回转换后的结果
            return reply
        except requests.RequestException as e:
            # 如果请求失败，打印错误信息并返回None
            print(f"请求失败: {e}")
            return None
# 示例使用
if __name__ == "__main__":
    task_id = 222
    memory_module = MemoryModule(task_id, db_config)

    # 初始化意图理解模块，并设置提示词前缀
    intent_understanding = IntentUnderstandingModule("请你扮演一位数据处理解决访问大师，你的任务是根据用户提出的有关数据处理的需求，进行合理的意图理解分析。然后参考下方示例进行输出。务必保证输出结果的结构化。\n示例需求：\n我有一篇3000字的论文，到时候不满意，让我进行文本优化并增添些数据分析，让我下周就交付。\n示例如下：\n期望目标：文本优化、增加数据分析；情感：急迫；约束条件：3000字结果仅输出期望目标、情感、约束条件，无其他内容。\n待意图理解的用户需求如下：\n")

    # 用户需求
    user_need = "我的论文被导师打回来了，他说我的论文里有脏数据，同时缺失数据的统一以及可视化，他要求我下周一交付一版优化后的稿子。"

    # 理解用户意图并获取结果
    intent_result = intent_understanding.understand_intent(user_need)

    memory_module.record("intent_result", intent_result)


    # 动态设置的功能池描述
    function_pool = "数据清洗、数据转换、数据合并与连接、数据聚合与分组、数据排序与筛选、数据去重、数据透视表、数据归一化与标准化、数据可视化"

    memory_module.record("function_pool", function_pool)

    # 初始化功能规划模块，并设置提示词模板和功能池知识库
    function_pool_knowledge = "数据清洗：识别和纠正数据中的错误、异常或缺失值，确保数据质量。数据转换：将数据从一种格式或类型转换为另一种，以便进行后续分析。数据合并与连接：将多个数据集根据某个或多个键合并成一个数据集。数据聚合与分组：按照某个或多个列对数据进行分组，并对每组数据进行聚合计算。数据排序与筛选：根据特定条件对数据进行排序或筛选，以获取所需的数据子集。数据去重：识别并删除数据集中的重复记录，保持数据的唯一性。数据透视表：根据数据集中的特定列生成透视表，用于数据汇总和分析。数据归一化与标准化：将数据缩放到特定范围或分布，以便进行机器学习或统计分析。时间序列分析：对时间序列数据进行处理和分析，如时间戳转换、时间序列的平滑、趋势分析等。数据可视化：将数据以图表形式展示，以便更直观地理解和分析数据。"

    # 构建动态提示词前缀
    dynamic_prompt_prefix = f"作为功能规划领域的专家，您的首要职责是深入理解用户需求，并从我们广泛而全面的功能库中查看是否有能够满足用户需求的功能，若有能更满足用户需求的功能，则将能够满足用户需求的功能池清单挑出来。\n注意事项：\n功能选择局限于功能库。请尽量遵循“少即是多”的原则。\n避免强行匹配功能。\n在满足用户需求的前提下，优先考虑使用最少的功能数量。每个增加的功能都应确保其对解决用户问题有直接且显著的贡献。这里举一个反例。\n反例展示：\n用户需求：请为我执行关键词提取任务。\n功能池清单（错误示例）：\n文本分词功能\n停用词去除功能\n关键词提取功能\n正确的功能池应仅包含：\n关键词提取功能\n示例功能如下：\n功能池清单：文本分词功能，去除停用词功能\n输出结果要求如下：\n若存在匹配的功能，则仅呈现功能池清单，无其他内容；若不存在匹配功能，则仅输出“无适配方案”，无其他内容。\n功能池如下：{function_pool}。\n用户需求的意图理解分析如下："

    # 初始化功能规划模块，并将动态提示词前缀作为参数传递
    function_planning = FunctionPlanningModule(dynamic_prompt_prefix)

    # 进行功能规划并获取结果
    function_plan_result = function_planning.plan_function(intent_result if intent_result else "未能获取意图理解结果")

    memory_module.record("function_plan_result", function_plan_result)

    # 初始化功能编排模块，并设置提示词前缀
    orchestration_prompt_prefix = f"作为任务编排专家，你的任务是根据我提供的用户需求和上传的功能池，参考示例编排方案的格式，精心设计一份高效且合理的编排方案，旨在实现复杂任务的自动化处理。编排方案包括具体节点和编排分析。本编排方案方案采用单向传播式的工作流架构，确保任务执行的高效性与准确性。\n工作流架构特点\n单向传播：每个节点的输出直接作为下一个节点的输入，形成无缝衔接的工作流。\n数据类型一致性：严格保证相邻节点间数据类型的匹配，避免数据转换错误或丢失。\n高效执行顺序：基于功能间的逻辑依赖关系，精心编排节点执行顺序，提升工作流整体效率。\n注意事项\n数据类型匹配：已严格验证并确保所有相邻节点间的数据类型完全匹配，以消除数据转换过程中的潜在问题。\n执行顺序优化：根据功能间的逻辑依赖，对节点执行顺序进行了精心调整，以最大化工作流的整体效率。\n编排分析请用一个自然段进行表示。节点后面只出现功能的名称。\n编排节点的范围仅包括功能池的所有内容。请不要额外增添其他功能\n示例编排方案如下：\n节点一：数据收集功能\n节点二：数据分析功能\n节点三：数据预测功能\n编排分析：本流程首先会从指定来源细致地收集原始文章数据，随后会严谨地进行数据的清洗、格式化与标准化处理，以确保数据的品质卓越。在此基础之上，我们会深入分析数据，精心识别出文章中需要润色的部分。紧接着，我们将依托丰富的历史数据与先进的模型，为您提供智能化的润色建议，甚至实现自动润色。最终，我们将为您自动生成一份详尽的报告，其中既包含了我们专业的改进建议，也呈现了经过精心润色后的文章成果。\n结果仅输出具体节点、编排分析，无其他内容。\n用户需求的意图理解分析如下：{intent_result}\n功能池如下："
    function_orchestration = FunctionOrchestrationModule(orchestration_prompt_prefix)

    # 进行功能编排并获取结果
    orchestration_result = function_orchestration.plan_orchestration(function_plan_result)

    memory_module.record("orchestration_result", orchestration_result)

    print(orchestration_result)

    text = orchestration_result
    # 使用正则表达式匹配功能配置方案分析前的内容
    pattern = r"(.*)编排分析："
    match = re.search(pattern, text, re.DOTALL)
    if match:
        orchestration_content = match.group(1)
        memory_module.record("orchestration_content", orchestration_content)
        print("功能编排提取成功")
        print(orchestration_content)
    else:
        print("未找到匹配的内容")

    # 使用正则表达式匹配功能配置方案分析后的内容
    pattern = r"编排分析：(.*)"
    match = re.search(pattern, text, re.DOTALL)  # 修正变量名为 text

    if match:
        # 提取匹配的内容
        analysis_content = match.group(1).strip()
        memory_module.record("analysis_content", analysis_content)
        print("编排分析提取成功")
        print(analysis_content)
    else:
        print("未找到功能配置方案分析的内容")

    convert_prompt_prefix = """
    请将参考下方示例格式将输入的内容转换为数组的格式。
    示例数据：
    节点一：text_text
    节点二：text_image
    节点三：image_text
    示例结果如下：
    "{"id": "node1", "function": "text_text"}",
    "{"id": "node2", "function": "text_image"}",
    "{"id": "node3", "function": "image_text"}"
    结果仅输出数组，无其他内容。
    待转换的内容如下：
    """
    converter = DataFormatConverter(convert_prompt_prefix)

    # 转换格式
    converted_result_raw = converter.convert_to_json_format(orchestration_content)
    converted_result = converted_result_raw.strip('```json\n')
    memory_module.record("converted_result", converted_result)

    # 打印结果
    print(converted_result)

