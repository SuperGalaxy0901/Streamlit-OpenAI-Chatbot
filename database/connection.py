import psycopg2  
from config import settings  

def create_connection():  
    try:  
        conn = psycopg2.connect(  
            host=settings.DB_HOST,  
            database=settings.DB_NAME,  
            user=settings.DB_USER,  
            password=settings.DB_PASSWORD  
        )  
        return conn 
    except Exception as e:  
        print(e)
        return None  