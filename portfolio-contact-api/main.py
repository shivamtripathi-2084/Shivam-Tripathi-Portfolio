import os
import html
import resend
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
def send_contact_message(request: Request, data: ContactMessage):

    # Honeypot: ignore automated spam submissions
    if data.website.strip():
        return {
            "message": "Your message has been sent successfully!"
        }

    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv(
        "RESEND_FROM_EMAIL",
        "onboarding@resend.dev",
    )
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not api_key or not receiver_email:
        raise HTTPException(
            status_code=500,
            detail="Email configuration is missing on the server.",
        )

    # Escape user-provided values before inserting them into HTML
    safe_name = html.escape(data.name)
    safe_email = html.escape(str(data.email))
    safe_subject = html.escape(data.subject)
    safe_message = html.escape(data.message).replace("\n", "<br>")

    resend.api_key = api_key

    try:
        result = resend.Emails.send({
            "from": from_email,
            "to": [receiver_email],
            "reply_to": str(data.email),
            "subject": f"Portfolio contact: {data.subject}",
            "html": f"""
                <h2>New message from your portfolio</h2>
                <p><strong>Name:</strong> {safe_name}</p>
                <p><strong>Visitor email:</strong> {safe_email}</p>
                <p><strong>Subject:</strong> {safe_subject}</p>
                <p><strong>Message:</strong></p>
                <p>{safe_message}</p>
            """,
            "text": (
                f"New message from your portfolio\n\n"
                f"Name: {data.name}\n"
                f"Visitor email: {data.email}\n"
                f"Subject: {data.subject}\n\n"
                f"Message:\n{data.message}"
            ),
        })

        print("Resend request completed:", result)

    except Exception as exc:
        # Avoid logging secrets or message contents
        print(f"Resend email failed: {type(exc).__name__}")

        raise HTTPException(
            status_code=502,
            detail="The email could not be sent. Please try again later.",
        )

    return {
        "message": "Your message has been sent successfully!"
    }
