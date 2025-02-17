# meu_app/services/servico_service.py
from meu_app.repositories.servico_repository import ServicoRepository  # Importação correta
from database import db

class ServicoService:
    def __init__(self):
        self.servico_repository = ServicoRepository(db)

    def listar_servicos(self):
        return self.servico_repository.buscar_todos()
