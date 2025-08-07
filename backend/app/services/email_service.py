import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException
from .config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 30

def create_reset_token(email: str):
    expires_delta = timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def send_password_reset_email(email: str, reset_url: str):
    message = MIMEText(f"""
    <h2>Restablecimiento de Contraseña</h2>
    <p>Para restablecer tu contraseña, haz clic en el siguiente enlace:</p>
    <a href="{reset_url}">{reset_url}</a>
    <p>Este enlace expirará en 30 minutos.</p>
    """, 'html')
    
    message['Subject'] = 'Restablecer contraseña - NexuStock'
    message['From'] = settings.EMAIL_FROM
    message['To'] = email

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
        return True
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al enviar el correo: {str(e)}"
        )

def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None
