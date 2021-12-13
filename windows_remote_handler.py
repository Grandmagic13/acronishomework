from remote_handler_base import RemoteHandlerBase


class WindowsRemoteHandler(RemoteHandlerBase):
    def __init__(self, ip_address):
        super().__init__(ip_address)

    def get_windefender_params(self):
        raise NotImplementedError()

    # not sure about what this one has to do exactly yet, assuming it has to return a list of registry keys
    def get_registry_keys(self):
        raise NotImplementedError()