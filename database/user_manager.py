import streamlit as st  
from database.connection import create_connection  
from utils.mailersend import signup_mailer  
import bcrypt  
import random  

def generate_6_digit_number():  
    return random.randint(100000, 999999)  

def create_users_table():  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            create_table_query = """  
            CREATE TABLE IF NOT EXISTS users (  
                id SERIAL PRIMARY KEY,  
                email VARCHAR(255) UNIQUE NOT NULL,  
                password VARCHAR(255) NOT NULL,  
                verify_id VARCHAR(255),  
                status VARCHAR(20),  
                country VARCHAR(30),  
                verification_token VARCHAR(255),  
                is_gmail INT  
            );  
            """  
            cursor.execute(create_table_query)  
            conn.commit()  
        except Exception as e:  
            print(e)
        finally:  
            cursor.close()  
            conn.close()  
    else:  
        st.error("Unable to connect to the database.")  

def create_user(email, password):  
    print("create user!!!!!!")
    flag = 0  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
            verify_id = generate_6_digit_number()  
            status = "pending"  
            cursor.execute(  
                "INSERT INTO users (email, password, verification_token, status, is_gmail) VALUES (%s, %s, %s, %s, %s)",  
                (email, hashed_password, verify_id, status, 0)  
            )  
            print("signup_mailer called!!!!!!")
            signup_mailer(email, verify_id)  
            conn.commit()  
        except Exception as e:  
            print(e)
            flag = 1  
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()  
            if flag == 0:  
                return verify_id  
            else:  
                return "error"  

def create_google_user(email):  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))  
            result = cursor.fetchone()  
            if result is None:  
                status = "verified"  
                cursor.execute(  
                    "INSERT INTO users (email, password, status, is_gmail) VALUES (%s, %s, %s, %s)",  
                    (email, 'XXX', status, 1)  
                )  
                conn.commit()  
            else:  
                print(email)  
        except Exception as e:  
            print(e)  
            pass  
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()  

def verify_user(email):  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute(  
                "UPDATE users SET status = %s WHERE email = %s",  
                ('verified', email)  
            )  
            conn.commit()  
        except Exception as e:  
            print(e)
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()  

def authenticate_user(email, password):  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            query = "SELECT password, status FROM users WHERE email = %s AND is_gmail = %s"  
            cursor.execute(query, (email, 0))  
            record = cursor.fetchone()  

            if record:  
                if bcrypt.checkpw(password.encode('utf-8'), record[0].encode('utf-8')):  
                    if record[1] == "verified":  
                        return "Success"  
                    else:  
                        return "Email has not been verified"  
                else:  
                    return "Invalid email or password"  
            else:  
                return "Invalid email or password"  
        except Exception as e:  
            print(e)
            return False  
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()  
    else:  
        print(e)
        return False  

def get_user_id(email):  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))  
            record = cursor.fetchone()  
            if record:  
                return record[0]  
            else:  
                return None  
        except Exception as e:  
            print(e)
            return None  
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()  

def update_user_country(email, country):  
    conn = create_connection()  
    if conn:  
        try:  
            cursor = conn.cursor()  
            cursor.execute(  
                "UPDATE users SET country = %s WHERE email = %s",  
                (country, email)  
            )  
            conn.commit()  
        except Exception as e:  
            print(e)
        finally:  
            if 'cursor' in locals():  
                cursor.close()  
            conn.close()