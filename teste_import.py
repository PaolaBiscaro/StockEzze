# test_import.py
try:
    import mysql.connector
    from mysql.connector import Error
    print("Importação bem-sucedida")
except ImportError as e:
    print(f"Erro ao importar: {e}")
