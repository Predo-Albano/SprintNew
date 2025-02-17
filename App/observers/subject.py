class Subject:
    def __init__(self):
        self._observers = []

    def adicionar_observador(self, observer):
        self._observers.append(observer)

    def remover_observador(self, observer):
        self._observers.remove(observer)

    def notificar(self, mensagem):
        for observer in self._observers:
            observer.atualizar(mensagem)
