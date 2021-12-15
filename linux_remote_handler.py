import functools

import paramiko as paramiko

from remote_handler_base import RemoteHandlerBase


class LinuxRemoteHandler(RemoteHandlerBase):
    def __init__(self, username, password, host, port=22):
        super().__init__(host)
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.client.connect(self.ip_address, self.port, self.username, self.password)

    def disconnect(self):
        self.client.close()

    def execute_in_commandline(self, command, print_stdout=False):
        stdin, stdout, stderr = self.client.exec_command(command)
        if print_stdout:
            [print(line) for line in stdout.readlines()]
        return {"stdin": stdin, "stdout": stdout, "stderr": stderr}

    def restart(self):
        stdin, stdout, stderr = self.client.exec_command("echo {} | sudo -S reboot -f".format(self.password))
        return {"stdin": stdin, "stdout": stdout, "stderr": stderr}

    def power_off(self):
        stdin, stdout, stderr = self.client.exec_command("echo {} | sudo -S shutdown -P -f now".format(self.password))
        return {"stdin": stdin, "stdout": stdout, "stderr": stderr}
