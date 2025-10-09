# 代码生成时间: 2025-10-09 20:47:35
# drug_inventory.py
# 药品库存管理系统，使用FALCON框架

from falcon import API, HTTP_200, HTTP_400, HTTP_404, HTTP_500
from falcon_cors import CORS, CORSMiddleware
from falcon import HTTPError
import json

class DrugInventoryResource:
    '''药品库存资源类'''
    def __init__(self):
        self.drugs = {}

    def _create_drug(self, drug_name, quantity):
        '''创建药品条目'''
        if drug_name in self.drugs:
            raise HTTPError(f"Drug '{drug_name}' already exists", status=400)
        self.drugs[drug_name] = quantity
        return self.drugs[drug_name]

    def _update_drug(self, drug_name, quantity):
        '''更新药品库存量'''
        if drug_name not in self.drugs:
            raise HTTPError(f"Drug '{drug_name}' not found", status=404)
        if quantity < 0:
            raise HTTPError("Quantity cannot be negative", status=400)
        self.drugs[drug_name] = quantity
        return self.drugs[drug_name]

    def on_get(self, req, resp):
        '''获取当前药品库存列表'''
        resp.body = json.dumps(self.drugs)
        resp.status = HTTP_200

    def on_post(self, req, resp):
        '''添加新药品到库存'''
        try:
            body = json.load(req.stream)
            drug_name = body['name']
            quantity = body['quantity']
            self._create_drug(drug_name, quantity)
            resp.status = HTTP_200
        except KeyError:
            raise HTTPError("Invalid request body", status=400)
        except HTTPError as e:
            raise HTTPError(str(e), status=e.status)

    def on_put(self, req, resp, drug_name):
        '''更新指定药品的库存量'''
        try:
            body = json.load(req.stream)
            quantity = body['quantity']
            self._update_drug(drug_name, quantity)
            resp.status = HTTP_200
        except KeyError:
            raise HTTPError("Invalid request body", status=400)
        except HTTPError as e:
            raise HTTPError(str(e), status=e.status)

# 设置CORS允许所有来源
cors = CORSMiddleware(allow_origin_list=['*'])

# 初始化API和CORS
api = API(middleware=cors)

# 添加资源到API
inventory = DrugInventoryResource()
api.add_route('/inventory', inventory)
api.add_route('/inventory/{drug_name}', inventory)