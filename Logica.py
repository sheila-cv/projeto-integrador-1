from datetime import datetime
from db import conectar

def buscar_usuario_por_login(nome, nascimento_str, senha):
    nascimento = nascimento_str  # já é um datetime.date do st.date_input

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM pacientes
        WHERE nome = %s AND nascimento = %s AND senha = %s
    """, (nome, nascimento, senha))

    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()
    return usuario


def listar_agendamentos_por_paciente(id_paciente):
    """
    Retorna todos os agendamentos do paciente ordenados pela data mais recente primeiro.
    """
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM agendamento
        WHERE id_paciente = %s
        ORDER BY data_agendada DESC
    """, (id_paciente,))

    agendamentos = cursor.fetchall()

    cursor.close()
    conexao.close()
    return agendamentos
from db import conectar

def buscar_agendamento_ativo(id_paciente):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM agendamento
        WHERE id_paciente = %s AND status IN ('agendado', 'reagendado')
        ORDER BY data_agendada DESC
        LIMIT 1
    """, (id_paciente,))
    
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()
    return resultado
