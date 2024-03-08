from abc import abstractmethod


class Context:

    @abstractmethod
    def run(self):
        pass
