from Domain import Client


class SystemManager(Client):

    def __init__(self, new_name, new_password):
        super(new_name, new_password)

    def get_system_manager(self, system_manager_user_name, system_manager_password):
        manager = 0
        if self.system_manager is None:
            manager = SystemManager(system_manager_user_name, system_manager_password)

        return manager
