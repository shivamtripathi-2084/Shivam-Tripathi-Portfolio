import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

load_dotenv()

app = FastAPI(title="Portfolio Contact API")

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        
    ],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class ContactMessage(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=3, max_length=150)
    message: str = Field(min_length=10, max_length=5000)
    website: str = Field(default="", max_length=200)


@app.get("/")
def home():
    return {"message": "Portfolio Contact API is running"}


@app.post("/api/contact")
@limiter.limit("5/minute")
def send_contact_message(request: Request,data: ContactMessage):
    
    if data.website.strip():
        return {
            "message": "Your message has been sent successfully!"
        }
    
    sender_email = os.getenv("SMTP_EMAIL")
    app_password = os.getenv("SMTP_APP_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not sender_email or not app_password or not receiver_email:
        raise HTTPException(
            status_code=500,
            detail="Email configuration is missing on the server.",
        )

    email_message = EmailMessage()
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message["Reply-To"] = str(data.email)
    email_message["Subject"] = f"Portfolio contact: {data.subject}"

    email_message.set_content(
        f"New message from your portfolio\n\n"
        f"Name: {data.name}\n"
        f"Visitor email: {data.email}\n"
        f"Subject: {data.subject}\n\n"
        f"Message:\n{data.message}"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as server:
            server.login(sender_email, app_password)
            server.send_message(email_message)

    except (smtplib.SMTPException, OSError):
        raise HTTPException(
            status_code=502,
            detail="The email could not be sent. Please try again later.",
        )

    return {"message": "Your message has been sent successfully!"}
