import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    try:
         return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
        )
         
    except mysql.connector.Error as erro:
        print("❌ Erro ao conectar no banco de dados:")
        print(erro)
        return None
