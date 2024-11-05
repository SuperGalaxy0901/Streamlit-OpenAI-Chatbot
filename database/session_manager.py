import streamlit as st  
from database.connection import create_connection  

def create_session_table():  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            create_table_query = """  
            CREATE TABLE IF NOT EXISTS session (  
                id SERIAL PRIMARY KEY,  
                user_id INT NOT NULL,  
                start_session TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
                end_session TIMESTAMP NULL  
            );  
            """  
            cursor.execute(create_table_query)  
            conn.commit()  
            # st.success("Table 'session' created successfully or already exists.")  
        except Exception as e:  
            # st.error(f"Error creating table: {e}")  
            print(e)
        finally:  
            cursor.close()  
            conn.close()  

def insert_start_session(user_id):  
    conn = create_connection()  
    new_id = None  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute("SELECT id, end_session FROM session ORDER BY id DESC LIMIT 1")  
            record = cursor.fetchone()  
            if record and record[1] is None:  
                update_end_session(record[0])  
            cursor.execute("INSERT INTO session (user_id) VALUES (%s) RETURNING id;", (user_id,))  
            new_id = cursor.fetchone()[0]  
            conn.commit()  
            # st.success("Session started successfully.")  
        except Exception as e:  
            # st.error(f"Error: {e}")  
            print(e)
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()  
    return new_id  

def update_end_session(session_id):  
    query = "UPDATE session SET end_session = CURRENT_TIMESTAMP WHERE id = %s"  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute(query, (session_id,))  
            conn.commit()  
            # st.success("Session ended successfully.")  
        except Exception as e:  
            # st.error(f"Error: {e}")  
            print(e)
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()