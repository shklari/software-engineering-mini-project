from Domain.Client import Client


class SystemManager(Client):

    def __init__(self, new_name, new_password):
        super(new_name, new_password)
        self.sys_manager = None

    @staticmethod
    def get_instance(self, system_manager_user_name, system_manager_password):
        if self.sys_manager is None:
            self.sys_manager = SystemManager(system_manager_user_name, system_manager_password)

        return self.sys_manager

    def get_sys_manager(self):
        return self.sys_manager
