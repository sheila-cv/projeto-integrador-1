import streamlit as st

def tela_capa():

    st.sidebar.title("Menu")
    opcao = st.sidebar.radio("", ["Início", "Acessar Sistema", "Sobre o Programa", "Lei Municipal 3380/2021", "Contatos"],)

    def set_background_url(url):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("{url}");
                background-size: 10%;
                background-repeat: no-repeat;
                background-position: 95% 90%;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # Chamada
    set_background_url("https://img.freepik.com/vetores-premium/jogo-de-frascos-da-medicina-com-etiquetas-e-comprimidos-em-um-fundo-branco-medicamentos-comprimidos-capsulas-de-vitaminas-termometro-ilustracao-em-estilo-simples_185004-143.jpg?w=826")


    if opcao == "Início":
        st.markdown("<h1 style='text-align: center;'>Programa Remédio em Casa</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Estância Turística de Brotas </h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:18px; margin-top: 10px;'>Sistema de agendamento de entrega domiciliar de medicamentos.</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:16px; margin-top: 10px;'>Levando cuidado e saúde até a porta de quem realmente precisa.</p>", unsafe_allow_html=True)

        
    elif opcao == "Acessar Sistema":
            st.session_state.pagina = "login"
            st.rerun()
    
    elif opcao == "Sobre o Programa":
        st.subheader("Sobre o Programa")
        st.markdown("""
            O **Programa Remédio** em casa foi criado em atendimento a lei municipal 3380/2021, para atendimento
            aos pacientes idosos, com mobilidade reduzida, deficientes ou especiais que utilizam medicações de uso
            contínuo.

            O programa foi instituído através da Farmácia municipal, Nadir Aparecida Degrandi Vital, a qual é
            responsável pelo cadastramento, agendamento e gestão.""")
        
    elif opcao == "Lei Municipal 3380/2021":
        st.subheader("Lei Municipal")
        st.markdown("""
        **Lei municipal 3380/2021**  
        Leia na íntegra a lei que institui o Programa remédio em casa na Estância turística de Brotas, bem como suas diretrizes.
        """)
        with open("LEI_3380_2021/lei_3380_2021.pdf", "rb") as f:
            st.download_button("📄 Baixar Lei (PDF)", data=f, file_name="lei_3380_2021.pdf")



    elif opcao == "Contatos":
        st.subheader("Contatos")
        st.markdown("""
        **Farmácia Municipal de Brotas**   
        
        📍 Rua José dos reis, 118 - Centro  
        📞 (14) 3653-5180   
        📧 farmacia@brotas.sp.gov.br  

       """)
        st.markdown("""--- """)
        st.markdown("""
        **Secretaria Municipal de Saúde**

        📍 Avenida Padre Barnabé Giron, nº 365 - Centro   
        📞 (14) 3653-6163 / (14) 3653-2250   
        📧 saude@brotas.sp.gov.br
        

        
        """)
