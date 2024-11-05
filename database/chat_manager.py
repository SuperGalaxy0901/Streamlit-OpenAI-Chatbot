import streamlit as st  
from database.connection import create_connection  
import bcrypt  

def create_chat_table():  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            create_table_query = """  
            CREATE TABLE IF NOT EXISTS chat (  
                id SERIAL PRIMARY KEY,  
                user_id INT NOT NULL,  
                vector_id VARCHAR(255) NOT NULL,  
                thread_id VARCHAR(255) NOT NULL,  
                file_id VARCHAR(255) NOT NULL,  
                assistant_id VARCHAR(255) NOT NULL  
            );  
            """  
            cursor.execute(create_table_query)  
            conn.commit()  
        except Exception as e:  
            print(e)
        finally:  
            cursor.close()  
            conn.close()  

def create_chat(user_id, vector_id, thread_id, file_id, assistant_id):  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute("INSERT INTO chat (user_id, vector_id, thread_id, file_id, assistant_id) VALUES (%s, %s, %s, %s, %s)",   
                           (user_id, vector_id, thread_id, file_id, assistant_id))  
            conn.commit()  
        except Exception as e:  
            print(e)
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()  

def get_individual_chat(id):  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute("SELECT user_id, vector_id, thread_id, file_id, assistant_id FROM chat WHERE id = %s", (id,))  
            record = cursor.fetchone()  
            if record:  
                return record  
            else:  
                return None  
        except Exception as e:  
            print(e)
            return None  
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()  

def get_user_chats(user_id):  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute("SELECT * FROM chat WHERE user_id = %s", (user_id,))  
            record = cursor.fetchall()  
            if record:  
                return record  
            else:  
                return None  
        except Exception as e:  
            print(e)
            return None  
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()