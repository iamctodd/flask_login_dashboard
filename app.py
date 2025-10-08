from flask import Flask, render_template, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from config import Config
from models import db, User
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize OAuth
oauth = OAuth(app)

# GitHub OAuth configuration
github = oauth.register(
    name='github',
    client_id=app.config['GITHUB_CLIENT_ID'],
    client_secret=app.config['GITHUB_CLIENT_SECRET'],
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# Google OAuth configuration
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/github')
def login_github():
    redirect_uri = url_for('authorize_github', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/authorize/github')
def authorize_github():
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    profile = resp.json()
    
    # Get or create user
    user = User.query.filter_by(oauth_provider='github', oauth_id=str(profile['id'])).first()
    if not user:
        user = User(
            username=profile['login'],
            email=profile.get('email'),
            oauth_provider='github',
            oauth_id=str(profile['id']),
            avatar_url=profile.get('avatar_url')
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return redirect(url_for('dashboard'))

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def authorize_google():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        # Get or create user
        user = User.query.filter_by(oauth_provider='google', oauth_id=user_info['sub']).first()
        if not user:
            user = User(
                username=user_info.get('email', '').split('@')[0],
                email=user_info.get('email'),
                oauth_provider='google',
                oauth_id=user_info['sub'],
                avatar_url=user_info.get('picture')
            )
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
