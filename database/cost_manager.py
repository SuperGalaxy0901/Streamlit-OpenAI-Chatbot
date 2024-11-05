import streamlit as st  
from database.connection import create_connection  

def create_cost_table():  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            create_table_query = """  
            CREATE TABLE IF NOT EXISTS cost (  
                id SERIAL PRIMARY KEY,  
                session_id INT NOT NULL,  
                cost FLOAT NOT NULL  
            );  
            """  
            cursor.execute(create_table_query)  
            conn.commit()  
        except Exception as e:
            print(e)
        finally:  
            cursor.close()  
            conn.close()  

def insert_cost(session_id, cost):  
    query = "INSERT INTO cost (session_id, cost) VALUES (%s, %s)"  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute(query, (session_id, cost))  
            conn.commit()  
        except Exception as e:  
            print(f"Error: {e}")  
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()