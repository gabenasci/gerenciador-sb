from abc import ABC, abstractmethod
import datetime


class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome: str, data_nascimento: datetime.date, telefone: int):
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(data_nascimento, datetime.date):
            self.__data_nascimento = data_nascimento
        if isinstance(telefone, int):
            self.__telefone = telefone

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: datetime.date):
        if isinstance(data_nascimento, datetime.date):
            self.__data_nascimento = data_nascimento

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: int):
        if isinstance(telefone, int):
            self.__telefone = telefone
