from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from services.usuario_service import UsuarioService
from models import Usuario, Agendamento

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            usuario = UsuarioService().autenticar(email, password)
            if usuario:
                session['usuario_id'] = usuario.id
                flash(f'Login realizado com sucesso, bem-vindo(a) {usuario.nome}!', 'success')  # Mensagem mais específica
                if usuario.is_admin:
                    return redirect(url_for('admin.painel'))
                else:
                    return redirect(url_for('usuario.painel'))
            else:
                flash('E-mail ou senha inválidos!', 'danger')
        except Exception as e:  # Tratamento de erros
            flash(f'Ocorreu um erro: {str(e)}', 'danger')

        return redirect(url_for('usuario.login'))  # Redireciona em caso de erro ou falha no login

    return render_template('login.html')

@usuario_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('password')

        try:
            UsuarioService().cadastrar(nome, email, senha)
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('usuario.login'))  # Redireciona para o login após o cadastro
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:  # Tratamento de erros
            flash(f'Ocorreu um erro: {str(e)}', 'danger')

        return render_template('cadastro.html')  # Renderiza o formulário em caso de erro

    return render_template('cadastro.html')

@usuario_bp.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('usuario.login'))

@usuario_bp.route('/painel')
def painel():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('usuario.login'))

    user_id = session['usuario_id']
    usuario = Usuario.query.get(user_id)

    if usuario:
        agendamentos = Agendamento.query.filter_by(user_id=user_id).all()
        return render_template('dashboard.html', usuario=usuario, agendamentos=agendamentos)
    else:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('usuario.login'))
