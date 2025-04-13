from db import conectar
from datetime import datetime, timedelta, date

class Agendamento:
    """
    Classe responsável por gerenciar o agendamento de entregas de medicamentos.
    """

    def __init__(self, id_paciente):
        self.id_paciente = id_paciente

    def proxima_sexta(self):
        """
        Retorna a data da próxima sexta-feira a partir de hoje.
        """
        hoje = datetime.today()
        dias_ate_sexta = (4 - hoje.weekday()) % 7  # 4 representa sexta-feira
        if dias_ate_sexta == 0:
            dias_ate_sexta = 7
        proxima = hoje + timedelta(days=dias_ate_sexta)
        return proxima.date()

    def pode_agendar(self):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        # Verifica se já existe agendamento ativo
        cursor.execute("""
            SELECT * FROM agendamento
            WHERE id_paciente = %s AND status IN ('agendado', 'reagendado')
        """, (self.id_paciente,))
        agendamento_ativo = cursor.fetchone()

        if agendamento_ativo:
            cursor.close()
            conexao.close()
            return False, "Você já possui um agendamento ativo."

        # Busca a última entrega feita
        cursor.execute("""
            SELECT medicamento_para, data_agendada FROM agendamento
            WHERE id_paciente = %s AND status = 'entregue'
            ORDER BY data_agendada DESC
            LIMIT 1
        """, (self.id_paciente,))
        ultima_entrega = cursor.fetchone()

        cursor.close()
        conexao.close()

        if ultima_entrega:
            dias_recebidos = int(ultima_entrega['medicamento_para'])
            data_entrega = ultima_entrega['data_agendada']

            dias_passados = (date.today() - data_entrega).days

            if dias_recebidos - dias_passados > 39:
                return False, f"Você ainda possui {dias_recebidos - dias_passados} dias de medicamento. Aguarde até poder agendar novamente."

        return True, "Agendamento permitido."

    def registrar_agendamento(self, data_entrega, dias_de_medicamento=60):
        """
        Registra um novo agendamento com a data escolhida e o número de dias de medicamento.
        """
        status = "agendado"
        data_solicitacao = date.today()

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO agendamento (id_paciente, data_agendada, status, medicamento_para, data_solicitacao)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.id_paciente, data_entrega, status, dias_de_medicamento, data_solicitacao))

        conexao.commit()
        cursor.close()
        conexao.close()

        return f"Agendamento registrado para {data_entrega.strftime('%d/%m/%Y')} com {dias_de_medicamento} dias de medicamento."

    def buscar_ultimo_agendamento(self):
        """
        Busca o último agendamento feito pelo paciente.
        """
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT data_agendada, status, medicamento_para
            FROM agendamento
            WHERE id_paciente = %s
            ORDER BY data_agendada DESC
            LIMIT 1
        """, (self.id_paciente,))

        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()

        return resultado
