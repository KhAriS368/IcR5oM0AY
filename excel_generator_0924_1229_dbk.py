# 代码生成时间: 2025-09-24 12:29:14
import falcon
import xlsxwriter
from falcon import API
from falcon import MediaResource
from datetime import datetime
import os


# 定义一个类用于生成Excel文件
class ExcelFileGenerator:
    def __init__(self, output_folder):
        """初始化函数，设置输出文件夹。
        Args:
            output_folder (str): 存放生成Excel文件的目录。"""
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def generate_excel(self, filename, data):
        """生成Excel文件。
        Args:
            filename (str): Excel文件名。
            data (list of list): 要写入Excel的数据。
        Returns:
            file_path (str): 生成的Excel文件的完整路径。"""
        try:
            # 定义文件路径
            file_path = os.path.join(self.output_folder, filename)
            # 创建Workbook
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet()

            # 写入数据
            for row_num, row_data in enumerate(data):
                for col_num, col_data in enumerate(row_data):
                    worksheet.write(row_num, col_num, col_data)

            # 关闭Workbook
            workbook.close()
            return file_path
        except Exception as e:
            print(f"Error generating Excel file: {e}")
            return None


# 定义一个资源类，用于处理FALCON请求
class ExcelGeneratorResource(MediaResource):
    def on_post(self, req, resp):
        """处理POST请求，生成Excel文件。"""
        # 获取请求体中的数据
        try:
            data = req.media or []
            # 创建一个Excel文件生成器
            excel_generator = ExcelFileGenerator("./excel_files")
            # 生成Excel文件
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
            file_path = excel_generator.generate_excel(filename, data)
            if file_path:
                resp.media = {
                    "message": "Excel file generated successfully.",
                    "file_path": file_path
                }
                resp.status = falcon.HTTP_200
            else:
                resp.media = {"message": "Failed to generate Excel file."}
                resp.status = falcon.HTTP_500
        except Exception as e:
            resp.media = {"message": f"Error: {e}"}
            resp.status = falcon.HTTP_500


# 创建FALCON应用
app = API()

# 添加资源到应用
app.add_route('/generate_excel', ExcelGeneratorResource())

# 运行应用（在实际部署时，这部分代码可能不会直接运行）
if __name__ == '__main__':
    # 这里使用默认的主机和端口，也可以通过环境变量或者配置文件来设置
    app.run(host='0.0.0.0', port=8000, debug=True)
