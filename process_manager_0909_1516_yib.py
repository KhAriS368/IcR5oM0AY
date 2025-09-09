# 代码生成时间: 2025-09-09 15:16:23
# process_manager.py
# Falcon application to manage system processes
#
# Requirements:
#   - Python 3.7+
#   - Falcon >= 3.0.0

import falcon
import subprocess
import sys
import psutil
from falcon import API, req, resp

# Define the Process Manager API
class ProcessManager:
    """
    A Falcon resource to manage system processes.
    """"
    def on_get(self, req, resp):
        """
        GET endpoint to list all processes.
        """
        try:
            processes = [proc.as_dict(attrs=['pid', 'name', 'status']) for proc in psutil.process_iter()]
            resp.media = processes
            resp.status = falcon.HTTP_200
        except Exception as exc:
            resp.body = f"An error occurred: {exc}"
            resp.status = falcon.HTTP_500

    def on_post(self, req, resp):
        """
        POST endpoint to start a new process.
        """
        try:
            cmd = req.media['command']
            subprocess.Popen(cmd, shell=True)
            resp.media = {'message': 'Process started successfully'}
            resp.status = falcon.HTTP_201
        except KeyError:
            resp.body = 'Missing command in request'
            resp.status = falcon.HTTP_400
        except Exception as exc:
            resp.body = f'Failed to start process: {exc}'
            resp.status = falcon.HTTP_500

    def on_delete(self, req, resp, pid):
        """
        DELETE endpoint to terminate a process by PID.
        """
        try:
            process = psutil.Process(pid)
            if process.is_running():
                process.terminate()
                resp.media = {'message': 'Process terminated successfully'}
                resp.status = falcon.HTTP_200
            else:
                resp.media = {'message': 'Process not running'}
                resp.status = falcon.HTTP_404
        except psutil.NoSuchProcess:
            resp.media = {'message': 'Process not found'}
            resp.status = falcon.HTTP_404
        except Exception as exc:
            resp.body = f'An error occurred: {exc}'
            resp.status = falcon.HTTP_500

# Initialize the Falcon API
api = API()

# Add the ProcessManager resource to the API
api.add_route('/processes', ProcessManager())
api.add_route('/processes/{pid}', ProcessManager())

# Run the API
if __name__ == '__main__':
    api.run(port=8000, host='0.0.0.0')  # Run the Falcon API on port 8000