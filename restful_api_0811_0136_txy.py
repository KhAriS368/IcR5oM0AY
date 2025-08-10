# 代码生成时间: 2025-08-11 01:36:09
import falcon
from falcon import HTTP_200, HTTP_404, HTTP_500
import json

# 定义资源对象
class ItemResource:
    def on_get(self, req, resp, item_id):
        """
        Handles GET requests.
        """
        # 检查item_id是否存在
        if item_id not in items:
            raise falcon.HTTPNotFound(
                "Item with ID {0} not found".format(item_id))
            
        # 响应请求
        resp.status = HTTP_200
        resp.body = json.dumps(items[item_id])

    def on_post(self, req, resp, item_id):
        """
        Handles POST requests.
        """
        global items
        try:
            # 解析请求体中的JSON数据
            data = json.load(req.stream)
        except json.JSONDecodeError:
            raise falcon.HTTPBadRequest("Invalid JSON")
        
        # 检查item_id是否已经存在
        if item_id in items:
            raise falcon.HTTPConflict(
                "Item with ID {0} already exists".format(item_id))
            
        # 添加新的item
        items[item_id] = data
        resp.status = HTTP_200
        resp.body = json.dumps(data)

# 初始的items字典
items = {}

# 创建API实例
api = falcon.API()

# 添加资源和路由
api.add_route("/items/{item_id}", ItemResource())

# 测试代码
if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server("", 8000, api)
    print("Serving on port 8000...")
    httpd.serve_forever()