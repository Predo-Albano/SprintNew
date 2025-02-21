from database import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    servico = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Agendamento {self.data}>'
    
    #  Nova tabela para armazenar horários configurados pelo administrador
class ConfiguracaoHorario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    intervalo = db.Column(db.Integer, nullable=False)  # Intervalo em minutos

    def __repr__(self):
        return f'<Configuração {self.hora_inicio} - {self.hora_fim}, intervalo: {self.intervalo} min>'
    
class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)

    def __repr__(self):
        return f'<Servico {self.nome}>'
