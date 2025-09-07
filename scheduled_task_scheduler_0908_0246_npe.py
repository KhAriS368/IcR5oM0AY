# 代码生成时间: 2025-09-08 02:46:03
# scheduled_task_scheduler.py

"""
定时任务调度器，使用Python和Falcon框架实现。
"""

import falcon
from falcon import Request, Response
import schedule
import time
import logging
from threading import Thread

# 设置日志记录
logging.basicConfig(level=logging.INFO)

# 定时任务列表
scheduled_tasks = []

# 示例定时任务函数
def task1():
    """
    任务1: 打印当前时间
    """
    logging.info("Task 1 executed at: %s", time.ctime())

def task2():
    """
    任务2: 打印当前时间
    """
    logging.info("Task 2 executed at: %s", time.ctime())

# 定义定时任务调度器
class ScheduledTaskScheduler:
    def __init__(self):
        self.scheduler_thread = None

    def start(self):
        """
        启动定时任务调度器
        """
        self.scheduler_thread = Thread(target=self.run)
        self.scheduler_thread.start()

    def run(self):
        """
        运行定时任务调度器
        """
        while True:
            schedule.run_pending()
            time.sleep(1)

    def add_task(self, task_func, interval):
        """
        添加定时任务
        
        Args:
            task_func (function): 任务函数
            interval (int): 间隔时间（秒）
        """
        schedule.every(interval).seconds.do(task_func)
        logging.info("Task added: %s with interval %s seconds", task_func.__name__, interval)

# 定义Falcon资源
class ScheduledTaskAPI:
    def on_get(self, req: Request, resp: Response):
        """
        GET请求: 返回所有定时任务的状态
        """
        # 获取定时任务状态
        task_status = [task.next_run for task in scheduled_tasks]
        
        # 返回JSON响应
        resp.media = {"tasks": task_status}
        resp.status = falcon.HTTP_OK

# 初始化定时任务调度器
scheduler = ScheduledTaskScheduler()

# 添加定时任务
scheduler.add_task(task1, 10)  # 每10秒执行一次任务1
scheduler.add_task(task2, 20)  # 每20秒执行一次任务2

# 启动定时任务调度器
scheduler.start()

# 初始化Falcon API
api = falcon.API()
api.add_route("/tasks", ScheduledTaskAPI())

# 运行Falcon API
if __name__ == "__main__":
    api.run(port=8000, host="0.0.0.0")
