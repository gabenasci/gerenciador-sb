from entidade.pessoa import Pessoa

class Cliente(Pessoa):
    def __init__(self, nome: str, data_nascimento: str, telefone: str, instagram: str, tipo_cliente: str, obs: str):
        super().__init__(nome, data_nascimento, telefone)
        if isinstance(instagram, str):
            self.__instagram = instagram
        if isinstance(tipo_cliente, str):
            self.__tipo_cliente = tipo_cliente
        if isinstance(obs, str):
            self.__obs = obs

    @property
    def instagram(self):
        return self.__instagram

    @instagram.setter
    def instagram(self, instagram):
        self.__instagram = instagram

    @property
    def tipo_cliente(self):
        return self.__tipo_cliente

    @tipo_cliente.setter
    def tipo_cliente(self, tipo_cliente):
        self.__tipo_cliente = tipo_cliente

    @property
    def obs(self):
        return self.__obs

    @obs.setter
    def tipo_cliente(self, obs):
        self.__obs = obs
