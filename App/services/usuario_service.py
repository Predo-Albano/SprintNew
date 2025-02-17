from repositories.usuario_repository import UsuarioRepository
from database import db  # Importa o db DIRETAMENTE
from models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioService:
    def __init__(self):
        self.usuario_repository = UsuarioRepository(db) # Injeta a dependência

    def autenticar(self, email, senha):
        usuario = self.usuario_repository.buscar_por_email(email) # Usa o repositorio com a dependencia injetada
        if usuario and check_password_hash(usuario.senha, senha):
            return usuario
        return None

    def cadastrar(self, nome, email, senha):
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        self.usuario_repository.salvar(novo_usuario) # Usa o repositorio com a dependencia injetada
