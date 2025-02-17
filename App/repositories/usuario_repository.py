from models import Usuario

class UsuarioRepository:
    def __init__(self, db):
        self.db = db

    def buscar_por_email(self, email):
        return self.db.session.query(Usuario).filter_by(email=email).first()

    def salvar(self, usuario):
        self.db.session.add(usuario)
        self.db.session.commit()
