import mysql.connector
import streamlit as st

def conectar():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="remedio_em_casa_db"
        )
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar com o banco de dados: {err}")
        return None
