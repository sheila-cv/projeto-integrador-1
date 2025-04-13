from db import conectar

def listar_agendamentos_por_status(status):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    # Cria os placeholders para o IN (%s, %s, ...)
    placeholders = ', '.join(['%s'] * len(status))

    query = f"""
        SELECT a.agendamento_id AS id_agendamento, a.*, p.nome AS nome_paciente, p.endereco
        FROM agendamento a
        JOIN pacientes p ON a.id_paciente = p.id
        WHERE a.status IN ({placeholders})
        ORDER BY a.data_agendada ASC
    """


    cursor.execute(query, tuple(status))
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()
    return resultado


def confirmar_entrega(id_agendamento):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE agendamento
        SET status = 'entregue'
        WHERE agendamento_id = %s
    """, (id_agendamento,))


    conexao.commit()
    cursor.close()
    conexao.close()


def buscar_pacientes_por_nome(nome_parcial):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM pacientes
        WHERE nome LIKE %s
        ORDER BY nome ASC
    """, (f"%{nome_parcial}%",))

    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados


def atualizar_dados_usuario(id_usuario, nome, nascimento, nome_mae, responsavel, cns, endereco, telefone, tipo, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE pacientes SET
            nome = %s,
            nascimento = %s,
            nome_da_mae = %s,
            responsavel = %s,
            cns = %s,
            endereco = %s,
            telefone = %s,
            tipo_de_cadastro = %s,
            senha = %s
        WHERE id = %s
    """, (nome, nascimento, nome_mae, responsavel, cns, endereco, telefone, tipo, senha, id_usuario))

    conexao.commit()
    cursor.close()
    conexao.close()

def desfazer_entrega(id_agendamento):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE agendamento
        SET status = 'agendado'
        WHERE agendamento_id = %s
    """, (id_agendamento,))

    conexao.commit()
    cursor.close()
    conexao.close()

from db import conectar

def cadastrar_usuario(nome, nascimento, nome_mae, responsavel, cns, endereco, telefone, tipo_de_cadastro, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO pacientes (nome, nascimento, nome_da_mae, responsavel, cns, endereco, telefone, tipo_de_cadastro, senha)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nome, nascimento, nome_mae, responsavel, cns, endereco, telefone, tipo_de_cadastro, senha))

    conexao.commit()
    cursor.close()
    conexao.close()
def confirmar_entrega_com_doses(id_agendamento, nova_dose):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE agendamento
        SET status = 'entregue', medicamento_para = %s
        WHERE agendamento_id = %s
    """, (nova_dose, id_agendamento))

    conexao.commit()
    cursor.close()
    conexao.close()
