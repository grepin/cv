import abc
from abc import ABCMeta


class LoginService(metaclass=ABCMeta):
    @abc.abstractmethod
    def login(self, data: dict, **kwargs):
        pass


class UpdateService(metaclass=ABCMeta):
    @abc.abstractmethod
    def update(self, data: dict, **kwargs):
        pass


class CreateService(metaclass=ABCMeta):
    @abc.abstractmethod
    def create(self, data: dict, **kwargs):
        pass


class ReadService(metaclass=ABCMeta):
    @abc.abstractmethod
    def delete(self, data: dict, **kwargs):
        pass


class DeleteService(metaclass=ABCMeta):
    @abc.abstractmethod
    def delete(self, data: dict, **kwargs):
        pass
