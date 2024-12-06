import pymysql
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)

# 连接到数据库的函数，作为上下文管理器
@contextmanager
def connect_db(config):
    connection = pymysql.connect(**config)
    try:
        yield connection
    finally:
        connection.close()

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