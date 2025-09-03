# 代码生成时间: 2025-09-04 07:35:27
# hash_calculator.py

import falcon
import hashlib
import json
from falcon import HTTP_200, HTTP_400, HTTP_404

# 定义哈希计算工具资源类
class HashCalculator:
    def on_get(self, req, resp):
        # 获取请求参数
        text = req.get_param('text')
        if not text:
            # 如果参数不存在，返回400错误
            raise falcon.HTTPBadRequest('Missing text parameter', 'Please provide the text parameter')
        
        # 计算哈希值
        try:
            hash_value = self.calculate_hash(text)
        except Exception as e:
            # 如果计算过程中出现异常，返回400错误
            raise falcon.HTTPBadRequest('Error calculating hash', str(e))
        
        # 返回计算结果
        resp.media = {'hash': hash_value}
        resp.status = HTTP_200

    def calculate_hash(self, text):
        """
        计算给定文本的哈希值。
        
        参数:
        text (str): 要计算哈希值的文本。
        
        返回:
        str: 计算出的哈希值。
        """
        # 使用SHA-256算法计算哈希值
        hash_object = hashlib.sha256(text.encode())
        return hash_object.hexdigest()

# 创建Falcon应用实例
app = falcon.API()

# 添加资源
hash_calculator_resource = HashCalculator()
app.add_route('/hash', hash_calculator_resource)

# 定义启动服务器的函数
def start_server():
    # 设置服务器主机和端口
    host = '0.0.0.0'
    port = 8000
    
    # 使用wsgiref服务器运行Falcon应用
    from wsgiref.simple_server import make_server
    server = make_server(host, port, app)
    print(f'Starting server on {host}:{port}')
    server.serve_forever()

# 如果直接运行脚本，则启动服务器
if __name__ == '__main__':
    start_server()