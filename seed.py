from app import app
from models import db, User, Campaign

# Run inside app context
with app.app_context():
    # Add sample users
    users = [
        User(name="Alice Johnson", email="alice@example.com", department="HR"),
        User(name="Bob Smith", email="bob@example.com", department="Finance"),
        User(name="Charlie Brown", email="charlie@example.com", department="IT")
    ]
    db.session.add_all(users)

    # Add sample campaign
    campaign = Campaign(
        name="Password Reset Scam",
        email_template="Please reset your password here: <a href='{{ phishing_link }}'>Reset Password</a>"
    )
    db.session.add(campaign)

    db.session.commit()

print("Sample data inserted successfully.")
