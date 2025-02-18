from observers.subject import Subject
from observers.admin_observer import AdminObserver
from repositories.agendamento_repository import AgendamentoRepository
from database import db
from factories.agendamento_factory import AgendamentoFactory  

class AgendamentoService(Subject):
    def __init__(self):
        super().__init__()
        self.adicionar_observador(AdminObserver())
        self.agendamento_repository = AgendamentoRepository(db)

    def criar_agendamento(self, user_id, data, servico): 
       
        agendamento = AgendamentoFactory.create('agendamento', user_id, data, servico)
        
        
        if not self.validar_horario_agendamento(data):
            raise ValueError("O horário escolhido está fora do intervalo permitido para agendamentos.")
        
       
        self.agendamento_repository.salvar(agendamento)
        
        # Notificar os observadores
        self.notificar(f"Novo agendamento para {servico} em {data}")
        return agendamento

    def obter_todos_agendamentos(self):
        """Retorna todos os horários agendados no sistema"""
        return [agendamento.data.strftime('%Y-%m-%d %H:%M') for agendamento in self.agendamento_repository.buscar_todos()]


