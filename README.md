**PhishGuard – Phishing Simulation & Awareness Platform**
PhishGuard is a full-stack phishing simulation platform designed to help organizations and individuals improve their phishing awareness. It allows administrators to create phishing campaigns, track user engagement (clicks), and provide personalized awareness feedback to improve cybersecurity training.

**Features**
Landing Page (Marketing Style)
Modern landing page highlighting app features and benefits with dark theme branding.

**Campaign Management Dashboard**
Create and manage phishing campaigns with customizable email templates.
Send campaigns to users (mock emails) and track click statistics in real time.

**Click Tracking & Reporting**
Monitor which users clicked phishing links.
Visual reporting with charts (click rate, total clicks, non-clicked users).
Department-level insights for targeted training.

**User Feedback Collection**
Capture reasons why users clicked phishing links.
Display personalized awareness tips (rule-based or AI-enhanced).

**Admin Panel**
View all campaigns, associated clicks, and user reasons.
Analyze user behavior for improving training strategies.

**Modern UI / UX**
Global dark theme using Bootstrap 5 and custom CSS.
Sidebar navigation (Landing, Dashboard, Admin Panel).
Favicon and branding (PhishGuard logo).

**Tech Stack**
Frontend: HTML, CSS, Bootstrap (dark theme)
Backend: Python (Flask)
Database: SQLite (SQLAlchemy ORM)
Email Sending: SMTP (mock email delivery)
Optional AI Feedback: OpenAI API (GPT-3.5) or fallback rule-based system

```Structure
phishguard/
│── app.py # Main Flask app
│── models.py # Database models (User, Campaign, Click)
│── config.py # Database configuration
│── utils.py # Email sending logic
│── seed.py # Seed script for dummy data
│── templates/ # HTML templates (landing, dashboard, reports, admin)
│── static/ # Static files (CSS, images, favicon)
│── phishing_sim.db # SQLite database
│── .env # API keys (OpenAI)
│── README.md # Project documentation
```

**Setup**
Clone Repo
`git clone https://github.com/your-username/phishguard.git
cd phishguard`

Create a Virtual Environment
`python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate`

Install Dependencies
`pip install -r requirements.txt` (If requirements.txt is missing, run pip freeze > requirements.txt after installing Flask, SQLAlchemy, python-dotenv, openai, etc.)

Initialize Database
`python seed.py`   # seeds with demo users and campaigns

Run the App
`python app.py`

**Usage**
Usage
Visit Landing Page (/) – Overview of PhishGuard and “Get Started” button.
Dashboard (/home) – View and manage campaigns, simulate clicks, view reports.
Admin Panel (/admin) – Analyze detailed user click behavior and reasons.
Reports (/report/<campaign_id>) – Visual breakdown of campaign engagement.
