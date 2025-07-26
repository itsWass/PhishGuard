from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, User, Campaign
from utils import send_phishing_email
from flask import jsonify
from models import Click
from flask import render_template
from flask import render_template
from flask import request, redirect, url_for
import random

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize database
db.init_app(app)

# Home route
@app.route('/')
def home():
    campaigns = Campaign.query.all()
    
    # Build campaign data with click stats
    campaign_data = []
    total_users = User.query.count()  # same total users for all campaigns

    for campaign in campaigns:
        clicked_count = len(campaign.clicks)
        click_rate = round((clicked_count / total_users) * 100, 2) if total_users else 0

        campaign_data.append({
            'id': campaign.id,
            'name': campaign.name,
            'created_at': campaign.created_at,
            'click_rate': click_rate
        })

    return render_template('home.html', campaigns=campaign_data)

# Debug route to view data
@app.route('/debug')
def debug():
    users = User.query.all()
    campaigns = Campaign.query.all()

    html = "<h2>Users</h2><ul>"
    for u in users:
        html += f"<li>{u.id}: {u.name} ({u.email}) - {u.department}</li>"
    html += "</ul>"

    html += "<h2>Campaigns</h2><ul>"
    for c in campaigns:
        html += f"<li>{c.id}: {c.name} - Template: {c.email_template}</li>"
    html += "</ul>"

    return html

@app.route('/send-emails/<int:campaign_id>')
def send_emails(campaign_id):
    # Get campaign and users
    campaign = Campaign.query.get_or_404(campaign_id)
    users = User.query.all()

    for user in users:
        # Generate tracking link (placeholder for now)
        phishing_link = f"http://127.0.0.1:5000/track/{campaign.id}/{user.id}"
        
        # Insert link into template
        html_content = campaign.email_template.replace("{{ phishing_link }}", phishing_link)
        
        # Send email
        send_phishing_email(user.email, campaign.name, html_content)

    return jsonify({"status": "emails sent", "campaign_id": campaign.id})

@app.route('/track/<int:campaign_id>/<int:user_id>')
def track_click(campaign_id, user_id):
    # Create a new click record
    click = Click(user_id=user_id, campaign_id=campaign_id)
    db.session.add(click)
    db.session.commit()

    # Show the clicked page
    return render_template('clicked.html')

@app.route('/report/<int:campaign_id>')
def report(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    users = User.query.all()

    clicked_user_ids = [click.user_id for click in campaign.clicks]
    clicked_users = [u for u in users if u.id in clicked_user_ids]
    non_clicked_users = [u for u in users if u.id not in clicked_user_ids]

    total_users = len(users)
    click_rate = round((len(clicked_users) / total_users) * 100, 2) if total_users else 0

    chart_data = [len(clicked_users), len(non_clicked_users)]

    return render_template(
        'report.html',
        campaign=campaign,
        total_users=total_users,
        clicked_users=clicked_users,
        non_clicked_users=non_clicked_users,
        click_rate=click_rate,
        chart_data=chart_data  # passed safely
    )

@app.route('/create-campaign', methods=['GET', 'POST'])
def create_campaign():
    if request.method == 'POST':
        name = request.form['name']
        email_template = request.form['email_template']

        # Create new campaign
        new_campaign = Campaign(name=name, email_template=email_template)
        db.session.add(new_campaign)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('create_campaign.html')

@app.route('/delete-campaign/<int:campaign_id>', methods=['POST'])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    # Delete related clicks first (to avoid orphan data)
    for click in campaign.clicks:
        db.session.delete(click)

    db.session.delete(campaign)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/simulate-campaign-clicks/<int:campaign_id>', methods=['POST'])
def simulate_campaign_clicks(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    # Find users who haven't clicked yet
    clicked_user_ids = [click.user_id for click in campaign.clicks]
    non_clicked_users = User.query.filter(~User.id.in_(clicked_user_ids)).all()

    # Simulate click for ONE random user
    if non_clicked_users:
        random_user = random.choice(non_clicked_users)
        click = Click(user_id=random_user.id, campaign_id=campaign.id)
        db.session.add(click)
        db.session.commit()

    return redirect(url_for('home'))


# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures tables exist
    app.run(debug=True)