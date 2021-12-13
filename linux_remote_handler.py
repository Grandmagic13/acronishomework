from remote_handler_base import RemoteHandlerBase


class LinuxRemoteHandler(RemoteHandlerBase):
    def __init__(self, ip_address):
        super().__init__(ip_address)