from fastapi.responses import HTMLResponse  
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from database.connection import create_connection
from utils.mailersend import signup_mailer
import bcrypt
import random
import string
import uvicorn  
import os
from dotenv import load_dotenv

load_dotenv()
PRODUCT_URL = os.getenv("PRODUCT_URL")

app = FastAPI()


@app.get("/api/verify-email")
async def verify_email(token: str, request: Request):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET status = 'verified' WHERE verification_token = '{token}'")
            conn.commit()
            html_content = f"""  
                <!DOCTYPE html>  
                <html>  
                <head>  
                    <title>Email Verified</title>  
                     <script type="text/javascript">  
                        setTimeout(function() {{ 
                            window.location.href = "{PRODUCT_URL}";
                        }}, 1500);  
                    </script>  
                </head>  
                <body>  
                    <h1>Email Verified Successfully!</h1>  
                    <p>You will be redirected shortly...</p>  
                </body>  
                </html>  
            """  
            return HTMLResponse(content=html_content, status_code=200) 
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

if __name__ == "__main__":  
    print("server up")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 