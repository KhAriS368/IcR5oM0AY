# 代码生成时间: 2025-08-31 07:48:55
# password_encryption_decryption_tool.py

# 导入Falcon框架和加密库
from falcon import API, HTTPNotFound, HTTPBadRequest, HTTPInternalServerError
import falcon
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib
import hmac
import os
import json

# 定义加密和解密函数
class EncryptionDecryptionTool:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        """加密明文数据"""
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(iv + ct_bytes).decode('utf-8')

    def decrypt(self, ciphertext):
        """解密密文数据"""
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:AES.block_size]
        ct = ciphertext[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')

# Falcon资源类
class PasswordEncryptionDecryptionResource:
    def __init__(self, key):
        self.encryption_decryption_tool = EncryptionDecryptionTool(key)

    def on_post(self, req, resp):
        """处理加密解密请求"""
        # 解析请求体
        try:
            request_body = json.load(req.stream)
            operation = request_body['operation']
            password = request_body['password']
        except (json.JSONDecodeError, KeyError):
            raise HTTPBadRequest('Invalid request body', 'Request body must be a JSON object with operation and password fields')

        # 执行加密或解密操作
        try:
            if operation == 'encrypt':
                encrypted_password = self.encryption_decryption_tool.encrypt(password)
            elif operation == 'decrypt':
                encrypted_password = request_body['encrypted_password']
                decrypted_password = self.encryption_decryption_tool.decrypt(encrypted_password)
                encrypted_password = None
            else:
                raise ValueError('Invalid operation', 'Operation must be either encrypt or decrypt')
        except ValueError as e:
            raise HTTPBadRequest(str(e))
        except Exception as e:
            raise HTTPInternalServerError(str(e))

        # 返回响应
        response_body = {'operation': operation, 'encrypted_password': encrypted_password, 'decrypted_password': decrypted_password}
        json_body = json.dumps(response_body)
        resp.status = falcon.HTTP_OK
        resp.body = json_body

# 创建加密密钥
key = hashlib.sha256(os.urandom(16)).digest()

# 创建Falcon API
api = API()
api.add_route('/encrypt-decrypt', PasswordEncryptionDecryptionResource(key))

# 运行API
if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)