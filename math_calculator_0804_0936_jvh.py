# 代码生成时间: 2025-08-04 09:36:22
import falcon

# 定义错误响应类
class ErrorResponder:
    def process_request(self, req, resp):
        resp.status = falcon.HTTP_400  # 设置响应状态码
        resp.json = {"error": "Bad request"}  # 设置JSON响应体

# 定义数学计算工具集资源类
class MathCalculatorResource:
    def on_get(self, req, resp):
        # 处理GET请求
        try:
            query_params = req.params
            operation = query_params.get("operation")
            if operation not in ["add", "subtract", "multiply", "divide"]:
                raise ValueError("Invalid operation")
            
            num1 = float(query_params.get("num1", 0))
            num2 = float(query_params.get("num2", 0))
            
            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                if num2 == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result = num1 / num2
                
            resp.json = {"result": result}  # 设置JSON响应体
        except ValueError as e:
            raise falcon.HTTPBadRequest("Invalid input", str(e))
        except ZeroDivisionError as e:
            raise falcon.HTTPBadRequest("Invalid input", str(e))

# 创建Falcon应用实例
app = falcon.App(
    middleware=[ErrorResponder()]  # 添加错误响应中间件
)

# 添加资源和路由
app.add_route("/math", MathCalculatorResource())

# 程序入口点
if __name__ == "__main__":
    import sys
    from wsgiref.simple_server import make_server
    
    # 创建WSGI服务器并运行应用
    host, port = "0.0.0.0", 8000
    httpd = make_server(host, port, app)
    print(f"Serving on {host}:{port}")
    httpd.serve_forever()