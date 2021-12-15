from remote_handler_base import RemoteHandlerBase
import winrm


## Helpers

def print_stdout(command_result):
    print(command_result.std_out.decode("utf-8"))


def extract_key_value_tuple(line):
    return tuple(map(lambda line: line.strip(), line.split(":", 1)))


def generate_dict_out_of(command_result):
    lines = command_result.std_out.decode("utf-8").split("\r\n")
    filtered_lines = list(filter(lambda line: len(line) > 0, lines))
    return dict(
        map(lambda line: (extract_key_value_tuple(line)), filtered_lines)
    )


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

    ## wasn't sure which windows defender parameters the task was referring to so I'm implementing both

    # returns dict of antimalware status key-value pairs and optionally prints command's console output
    def get_windefender_antimalware_status(self, print_readable=False):
        result = self.execute_in_commandline("Get-MpComputerStatus")
        if print_readable:
            print_stdout(result)
        return generate_dict_out_of(result)

    # returns dict of windows defender preferences key-value pairs and optionally prints command's console output
    def get_windefender_params(self, print_readable=False):
        result = self.execute_in_commandline("Get-MpPreference")
        if print_readable:
            print_stdout(result)
        return generate_dict_out_of(result)

    # not sure about what this one has to do exactly yet, assuming it has to return a list of registry keys
    def get_registry_keys(self):
        raise NotImplementedError()
