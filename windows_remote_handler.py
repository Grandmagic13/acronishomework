from remote_handler_base import RemoteHandlerBase
import winrm


class WindowsRemoteHandler(RemoteHandlerBase):
    def __init__(self, username, password, host, domain=None):
        super().__init__(host)
        self.domain = domain
        self.username = username
        self.password = password
        user_creds = '{0}@{1}'.format(self.username, self.domain) if domain else username
        self.session = winrm.Session(self.ip_address, auth=(user_creds, self.password), transport='ntlm')

    def execute_in_commandline(self, command):
        return self.session.run_ps(command)

    def restart(self):
        return self.execute_in_commandline("shutdown /r /t 0")

    def power_off(self):
        return self.execute_in_commandline("shutdown /p")

    def get_windefender_params(self):
        raise NotImplementedError()

    # not sure about what this one has to do exactly yet, assuming it has to return a list of registry keys
    def get_registry_keys(self):
        raise NotImplementedError()