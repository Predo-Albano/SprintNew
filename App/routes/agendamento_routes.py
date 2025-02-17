from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from services.agendamento_service import AgendamentoService
from datetime import datetime
from models import ConfiguracaoHorario  # Importe o modelo de ConfiguracaoHorario

agendamento_bp = Blueprint('agendamento', __name__)

# Função para validar se o agendamento está dentro do horário configurado pelo administrador
def validar_horario_agendamento(horario_agendamento):
    """Verifica se o horário do agendamento está dentro do intervalo definido pelo admin."""
    configuracao = ConfiguracaoHorario.query.first()  # Obtemos a configuração de horário
    if configuracao:
        hora_inicio = configuracao.hora_inicio
        hora_fim = configuracao.hora_fim

        # Verifique se o horário do agendamento está dentro do intervalo
        if hora_inicio <= horario_agendamento.time() <= hora_fim:
            return True
    return False

@agendamento_bp.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('usuario.login'))

    user_id = session['usuario_id']

    if request.method == 'POST':
        data_str = request.form.get('data')
        servico = request.form.get('servico')

        try:
            data = datetime.strptime(data_str, '%Y-%m-%dT%H:%M')  # Converte a string para datetime

            # Verifique se o horário está dentro do permitido
            if not validar_horario_agendamento(data):
                flash('O horário escolhido está fora do intervalo permitido para agendamentos.', 'danger')
                return render_template('agendamento.html')

            # Criar o agendamento se for válido
            AgendamentoService().criar_agendamento(user_id, data, servico)
            flash('Agendamento efetuado com sucesso!', 'success')
            return redirect(url_for('usuario.painel'))  # Redireciona para o painel
        except ValueError as e:
            flash(f'Dados inválidos: {str(e)}', 'danger')
            return render_template('agendamento.html')
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')
            return render_template('agendamento.html')

    return render_template('agendamento.html')

@agendamento_bp.route('/menu')
def menu():
    return render_template('menu.html')
