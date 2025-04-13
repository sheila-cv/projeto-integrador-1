import streamlit as st
from datetime import datetime, timedelta, date
from Logica import buscar_usuario_por_login
from Agendamento import Agendamento
from Home import tela_capa
from Logica_funcionario import (
    listar_agendamentos_por_status,
    confirmar_entrega_com_doses,
    desfazer_entrega,
    cadastrar_usuario,
    buscar_pacientes_por_nome,
    atualizar_dados_usuario
)

st.set_page_config(page_title="Remédio em Casa", layout="centered",)



# Inicializa sessão
if "pagina" not in st.session_state:
    st.session_state.pagina = "capa"
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "agendamento_realizado" not in st.session_state:
    st.session_state.agendamento_realizado = False

if st.session_state.pagina == "capa":
    tela_capa()

# === TELA DE LOGIN ===
elif st.session_state.pagina == "login":
    st.title("Login")
    nome = st.text_input("Nome Completo")
    nascimento = st.date_input("Data de Nascimento", format="DD/MM/YYYY", min_value=date(1900, 1, 1), max_value=date.today())
    senha = st.text_input("Senha", type="password")

    col4, col5, col6, col7 = st.columns([0.5,0.5,1.5,1.5 ])
    with col4:
        if st.button("Entrar"):
            usuario = buscar_usuario_por_login(nome, nascimento, senha)
            if usuario:
                st.session_state.usuario = usuario
                if usuario["tipo_de_cadastro"] == "funcionario":
                    st.session_state.pagina = "painel_controle"
                else:
                    st.session_state.pagina = "boas_vindas"
                st.rerun()
            else:
                st.error("Dados inválidos. Verifique e tente novamente.")
    with col5:    
        if st.button("Voltar"):
            st.session_state.pagina = "capa"
            st.rerun()



# === BOAS-VINDAS (PACIENTE) ===
elif st.session_state.pagina == "boas_vindas":
    usuario = st.session_state.usuario
    st.title(f"👋 Olá, {usuario['nome'].split()[0]}!")
    st.write(f"📍 Endereço: {usuario['endereco']}")
    st.write(f"📞 Telefone: {usuario['telefone']}")

    agendamento = Agendamento(usuario['id'])
    ultimo_agendamento = agendamento.buscar_ultimo_agendamento()

    if ultimo_agendamento:
        st.markdown("---")
        st.subheader("📦 Seu último agendamento")
        st.write(f"🗓 Data agendada: **{ultimo_agendamento['data_agendada'].strftime('%d/%m/%Y')}**")
        st.write(f"🔄 Status: **{ultimo_agendamento['status'].capitalize()}**")

    st.markdown("---")
    st.info("Verifique se pode fazer um agendamento")

    if st.button("Avançar para Agendamento"):
        st.session_state.pagina = "agendamento"
        st.rerun()

    if st.button("🔓 Sair"):
        st.session_state.pagina = "login"
        st.session_state.usuario = None
        st.rerun()

# === AGENDAMENTO (PACIENTE) ===
elif st.session_state.pagina == "agendamento":
    st.title("📅 Agendamento de Entrega")
    agendamento = Agendamento(st.session_state.usuario["id"])

    if st.session_state.agendamento_realizado:
        st.success("✅ Agendamento registrado com sucesso!")
        st.session_state.agendamento_realizado = False

    pode, mensagem = agendamento.pode_agendar()
    st.write(mensagem)

    if pode:
        hoje = date.today()
        data_sugestiva = hoje + timedelta((4 - hoje.weekday()) % 7)
        data_selecionada = st.date_input(
            "Selecione uma data de entrega (somente sextas-feiras são permitidas)",
            min_value=hoje,
            value=data_sugestiva,
            format="DD/MM/YYYY"
        )

        if data_selecionada.weekday() == 4:
            if st.button("Confirmar agendamento"):
                agendamento.registrar_agendamento(data_selecionada)
                st.session_state.agendamento_realizado = True
                st.rerun()
        else:
            st.warning("⚠️ Só é possível agendar para uma sexta-feira.")
    else:
        st.warning("Você não pode agendar no momento.")

    if st.button("🔙 Voltar"):
        st.session_state.pagina = "boas_vindas"
        st.rerun()

# === PAINEL DO FUNCIONÁRIO ===
elif st.session_state.pagina == "painel_controle":
    st.title("🛠️ Painel de Controle do Funcionário")
    st.write("Escolha a funcionalidade desejada:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Cadastrar usuário"):
            st.session_state.pagina = "cadastrar_usuario"
            st.rerun()
        if st.button("📋 Confirmar entregas"):
            st.session_state.pagina = "confirmar_entregas"
            st.rerun()
    with col2:
        if st.button("✏️ Editar usuário"):
            st.session_state.pagina = "editar_usuario_menu"
            st.rerun()
        if st.button("🛠️ Corrigir entregas"):
            st.session_state.pagina = "corrigir_entregas"
            st.rerun()

    if st.button("🔓 Sair"):
        st.session_state.pagina = "login"
        st.session_state.usuario = None
        st.rerun()

# === CADASTRAR USUÁRIO ===
elif st.session_state.pagina == "cadastrar_usuario":
    st.title("➕ Cadastro de Novo Usuário")
    nome = st.text_input("Nome completo")
    nascimento = st.date_input("Data de nascimento")
    nome_mae = st.text_input("Nome da mãe")
    responsavel = st.text_input("Responsável")
    cns = st.text_input("CNS")
    endereco = st.text_input("Endereço")
    telefone = st.text_input("Telefone")
    tipo = st.selectbox("Tipo de cadastro", ["paciente", "funcionario"])
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        if nome and senha:
            cadastrar_usuario(nome, nascimento, nome_mae, responsavel, cns, endereco, telefone, tipo, senha)
            st.success("Usuário cadastrado com sucesso!")
        else:
            st.warning("Nome e senha são obrigatórios.")

    if st.button("🔙 Voltar ao Painel"):
        st.session_state.pagina = "painel_controle"
        st.rerun()

# === MENU DE EDIÇÃO DE USUÁRIO ===
elif st.session_state.pagina == "editar_usuario_menu":
    st.title("✏️ Buscar usuário para editar")
    todos_pacientes = buscar_pacientes_por_nome("")
    nomes_opcoes = [f"{p['nome']} - {p['endereco']}" for p in todos_pacientes]
    selecionado = st.selectbox("Selecione o paciente para editar", nomes_opcoes)

    if selecionado:
        index = nomes_opcoes.index(selecionado)
        paciente = todos_pacientes[index]
        if st.button("✏️ Editar"):
            st.session_state.paciente_edicao = paciente
            st.session_state.pagina = "editar_usuario"
            st.rerun()

    if st.button("🔙 Voltar ao Painel"):
        st.session_state.pagina = "painel_controle"
        st.rerun()

# === EDIÇÃO DE USUÁRIO ===
elif st.session_state.pagina == "editar_usuario":
    paciente = st.session_state.paciente_edicao
    st.title(f"✏️ Editar dados de: {paciente['nome']}")

    nome = st.text_input("Nome completo", value=paciente["nome"])
    nascimento = st.date_input("Data de nascimento", value=paciente["nascimento"])
    nome_mae = st.text_input("Nome da mãe", value=paciente["nome_da_mae"])
    responsavel = st.text_input("Responsável", value=paciente["responsavel"])
    cns = st.text_input("CNS", value=paciente["cns"])
    endereco = st.text_input("Endereço", value=paciente["endereco"])
    telefone = st.text_input("Telefone", value=paciente["telefone"])
    tipo = st.selectbox("Tipo de cadastro", ["paciente", "funcionario"], index=0 if paciente["tipo_de_cadastro"] == "paciente" else 1)
    senha = st.text_input("Senha", value=paciente["senha"])

    if st.button("Salvar alteração"):
        atualizar_dados_usuario(
            paciente["id"], nome, nascimento, nome_mae, responsavel,
            cns, endereco, telefone, tipo, senha
        )
        st.success("Alterações salvas com sucesso!")
        st.session_state.pagina = "painel_controle"
        st.rerun()

    if st.button("🔙 Voltar ao Painel"):
        st.session_state.pagina = "painel_controle"
        st.rerun()

# === CORRIGIR ENTREGAS ===
elif st.session_state.pagina == "confirmar_entregas":
    st.title("📋 Confirmar Entregas")

    agendamentos = listar_agendamentos_por_status(status=["agendado", "reagendado"])

    if not agendamentos:
        st.info("Nenhum agendamento pendente.")
    else:
        for ag in agendamentos:
            st.markdown("---")
            st.subheader(f"🧑 {ag['nome_paciente']}")
            st.write(f"📅 Data Agendada: {ag['data_agendada']}")
            st.write(f"💊 Doses atuais: {ag['medicamento_para']} dias")
            st.write(f"📍 Endereço: {ag['endereco']}")

            nova_dose = st.number_input(
                f"Editar dose para {ag['nome_paciente']}",
                min_value=1, max_value=120,
                value=int(ag['medicamento_para']),
                key=f"dose_{ag['id_agendamento']}"
            )

            if st.button(f"✅ Confirmar entrega de {ag['nome_paciente']}", key=f"abrir_dialog_{ag['id_agendamento']}"):
                st.session_state.dialog_aberto = ag['id_agendamento']
                st.session_state.dialog_dose = nova_dose
                st.session_state.dialog_info = {
                    "id_agendamento": ag["id_agendamento"],
                    "nome_paciente": ag["nome_paciente"],
                    "data_agendada": ag["data_agendada"],
                    "endereco": ag["endereco"]
                }
                st.rerun()

            if (
                "dialog_aberto" in st.session_state and
                st.session_state.dialog_aberto == ag["id_agendamento"]
            ):
                dados = st.session_state.dialog_info

                @st.dialog(f"Confirmação da entrega para {dados['nome_paciente']}")
                def confirmar_entrega_dialog():
                    st.write(f"📅 Data Agendada: {dados['data_agendada']}")
                    st.write(f"💊 Doses: {st.session_state.dialog_dose} dias")
                    st.write(f"📍 Endereço: {dados['endereco']}")

                    if st.button("✅ Confirmar agora", key=f"confirmar_final_{dados['id_agendamento']}"):
                        confirmar_entrega_com_doses(
                            dados["id_agendamento"],
                            st.session_state.dialog_dose
                        )
                        st.success(f"Entrega confirmada para {dados['nome_paciente']} com {st.session_state.dialog_dose} dias.")
                        st.session_state.dialog_aberto = None
                        st.rerun()

                confirmar_entrega_dialog()

    if st.button("🔙 Voltar ao Painel"):
        st.session_state.pagina = "painel_controle"
        st.rerun()

elif st.session_state.pagina == "corrigir_entregas":
    st.title("🛠️ Corrigir Entregas")

    try:
        entregues = listar_agendamentos_por_status(status=["entregue"])

        if not entregues:
            st.info("Nenhuma entrega foi registrada ainda.")
        else:
            for ag in entregues:
                st.markdown("---")
                st.write(f"🧑 Paciente: **{ag['nome_paciente']}**")
                st.write(f"📅 Data da entrega: {ag['data_agendada'].strftime('%d/%m/%Y')}")
                st.write(f"💊 Doses: {ag['medicamento_para']} dias")
                st.write(f"📍 Endereço: {ag['endereco']}")

                if st.button(f"↩️ Desfazer entrega de {ag['nome_paciente']}", key=f"desfazer_{ag['id_agendamento']}"):
                    desfazer_entrega(ag["id_agendamento"])
                    st.success(f"Entrega desfeita para {ag['nome_paciente']}.")
                    st.rerun()

    except Exception as e:
        st.error(f"❌ Erro ao carregar entregas: {e}")

    st.markdown("---")
    if st.button("🔙 Voltar ao Painel"):
        st.session_state.pagina = "painel_controle"
        st.rerun()
