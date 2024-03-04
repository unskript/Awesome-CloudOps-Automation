from abc import ABC, abstractmethod

class BaseRepository(ABC):

    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def insert(self, data):
        pass

    @abstractmethod
    def insert_many(self, models):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def find_by_parent_id(self):
        pass

    @abstractmethod
    def close(self):
        pass