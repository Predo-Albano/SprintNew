from models import Agendamento

class AgendamentoRepository:
    def __init__(self, db):
        self.db = db

    def salvar(self, agendamento):
        self.db.session.add(agendamento)
        self.db.session.commit()

    def buscar_por_usuario(self, user_id):
        return Agendamento.query.filter_by(user_id=user_id).all()
    def buscar_todos(self):
        return Agendamento.query.all()
