from database import db
from models import Servico

class ServicoRepository:
    def __init__(self, db):
        self.db = db

    def buscar_todos(self):
        return Servico.query.all()
