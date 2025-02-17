from models import Usuario

class UsuarioFactory:
    TIPOS = {'usuario': Usuario}

    @staticmethod
    def create(tipo, nome, email, senha):
        if tipo not in UsuarioFactory.TIPOS:
            raise ValueError("Tipo de usuário inválido")
        return UsuarioFactory.TIPOS[tipo](nome=nome, email=email, senha=senha)
