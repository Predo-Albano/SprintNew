from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models import Agendamento, Usuario, ConfiguracaoHorario, Servico  
from database import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/painel')
def painel():
    """Exibe o painel de administrador com a lista de agendamentos e serviços."""

    if 'usuario_id' not in session:
        flash('Você precisa estar logado como administrador para acessar esta página.', 'warning')
        return redirect(url_for('usuario.login'))

    user_id = session['usuario_id']
    usuario = Usuario.query.get(user_id)

    if not usuario.is_admin:
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('usuario.painel'))

    agendamentos = Agendamento.query.all()  # Busca todos os agendamentos
    servicos = Servico.query.all()  # Busca todos os serviços

    return render_template('admin_dashboard.html', agendamentos=agendamentos, servicos=servicos)  

@admin_bp.route('/configurar-horarios', methods=['GET', 'POST'])
def configurar_horarios():
    """Lida com a configuração de horários e intervalos de agendamento."""

    if 'usuario_id' not in session:
        flash('Você precisa estar logado como administrador para acessar esta página.', 'warning')
        return redirect(url_for('usuario.login'))

    user_id = session['usuario_id']
    usuario = Usuario.query.get(user_id)

    if not usuario.is_admin:
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('usuario.painel'))

    if request.method == 'POST':
        hora_inicio = request.form.get('inicio')
        hora_fim = request.form.get('fim')
        intervalo = request.form.get('intervalo')

        try:
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
            hora_fim = datetime.strptime(hora_fim, '%H:%M').time()
            intervalo = int(intervalo)
        except ValueError:
            flash('Dados inválidos. Certifique-se de que as horas estão no formato HH:MM e o intervalo é um número inteiro.', 'danger')
            return redirect(url_for('admin.configurar_horarios'))

        configuracao = ConfiguracaoHorario.query.first()
        if configuracao:
            configuracao.hora_inicio = hora_inicio
            configuracao.hora_fim = hora_fim
            configuracao.intervalo = intervalo
        else:
            configuracao = ConfiguracaoHorario(hora_inicio=hora_inicio, hora_fim=hora_fim, intervalo=intervalo)
            db.session.add(configuracao)

        db.session.commit()

        flash('Configurações salvas com sucesso!', 'success')
        return redirect(url_for('admin.painel'))

    return render_template('admin_dashboard.html')

@admin_bp.route('/cadastrar_servico', methods=['POST'])  # Rota para cadastrar serviço
def cadastrar_servico():
    """Cadastra um novo serviço."""

    if 'usuario_id' not in session:
        flash('Você precisa estar logado como administrador para acessar esta página.', 'warning')
        return redirect(url_for('usuario.login'))

    user_id = session['usuario_id']
    usuario = Usuario.query.get(user_id)

    if not usuario.is_admin:
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('usuario.painel'))

    nome_servico = request.form.get('nome_servico')
    descricao_servico = request.form.get('descricao_servico')

    novo_servico = Servico(nome=nome_servico, descricao=descricao_servico)
    db.session.add(novo_servico)
    db.session.commit()

    flash('Serviço cadastrado com sucesso!', 'success')
    return redirect(url_for('admin.painel'))  # Redireciona para o painel
