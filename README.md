# Shivam Tripathi — Portfolio

Welcome to my personal portfolio! I'm a Full-Stack Web Developer interested in building responsive web applications and useful digital experiences.

## 🌐 Live Portfolio

**Visit my portfolio:** [Open Portfolio](https://shivam-tripathi-portfolio-ui.onrender.com)

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python, FastAPI
- **Email Integration:** Resend
- **Deployment:** Render
- **Version Control:** Git and GitHub

## ✨ Features

- Responsive portfolio website
- Sections to explore my profile, skills, projects, and contact information
- Contact form connected to a FastAPI backend
- Email notifications for submitted contact messages
- Input validation and basic rate limiting on the contact API

## 🚀 Deployment

The frontend and backend are deployed separately on Render.

- **Frontend:** https://shivam-tripathi-portfolio-ui.onrender.com
- **Backend API:** https://shivam-tripathi-portfolio.onrender.com
- **API documentation:** https://shivam-tripathi-portfolio.onrender.com/docs

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/shivamtripathi-2084/Shivam-Tripathi-Portfolio.git
cd Shivam-Tripathi-Portfolio
```

### 2. Run the frontend

Open the `portfolio-UI` folder and serve `index.html` using a local development server such as VS Code Live Server.

### 3. Run the backend

Open a terminal in the backend folder (`portfolio-contact-api`) and create/activate a virtual environment.

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the backend folder with the required environment variables:

```env
RESEND_API_KEY=your_resend_api_key
RESEND_FROM_EMAIL=your_verified_sender_email
RECEIVER_EMAIL=your_email_address
```

Never commit your real `.env` file or API key to GitHub. Configure production environment variables in Render's dashboard.

Start the API:

```bash
uvicorn main:app --reload
```

The API will usually run at `http://127.0.0.1:8000`.

## 📬 Contact

Please visit the [live portfolio](https://shivam-tripathi-portfolio-ui.onrender.com) to find my contact information and send a message.

---

Made with ❤️ by Shivam Tripathi.
