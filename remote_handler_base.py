class RemoteHandlerBase:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def power_off(self):
        raise NotImplementedError()

    def restart(self):
        raise NotImplementedError()

    def execute_in_commandline(self, command):
        raise NotImplementedError()