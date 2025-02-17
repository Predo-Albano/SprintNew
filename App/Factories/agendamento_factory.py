from models import Agendamento

class AgendamentoFactory:
    TIPOS = {'agendamento': Agendamento}

    @staticmethod
    def create(tipo, user_id, data, servico):
        if tipo not in AgendamentoFactory.TIPOS:
            raise ValueError("Tipo de agendamento inválido")
        return AgendamentoFactory.TIPOS[tipo](user_id=user_id, data=data, servico=servico)
