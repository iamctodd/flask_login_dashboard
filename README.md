# Flask Login Dashboard

A Flask application with OAuth authentication support for GitHub, Google, and other OAuth providers. Users can log in using their preferred OAuth provider and access a personalized dashboard.

## Features

- 🔐 OAuth 2.0 authentication with GitHub and Google
- 👤 User session management with Flask-Login
- 💾 SQLite database for user storage
- 🎨 Modern, responsive UI
- 🔒 Protected dashboard routes
- 📊 User profile display with avatar support

## Prerequisites

- Python 3.8 or higher
- GitHub OAuth App (for GitHub login)
- Google OAuth Client (for Google login)

## OAuth Provider Setup

### GitHub OAuth Setup

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the application details:
   - **Application name**: Flask Login Dashboard
   - **Homepage URL**: `http://localhost:5000`
   - **Authorization callback URL**: `http://localhost:5000/authorize/github`
4. Click "Register application"
5. Copy the **Client ID** and generate a **Client Secret**

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" and create "OAuth 2.0 Client ID"
5. Configure the consent screen if needed
6. Set the application type to "Web application"
7. Add authorized redirect URIs:
   - `http://localhost:5000/authorize/google`
8. Copy the **Client ID** and **Client Secret**

## Installation

1. Clone the repository:
```bash
git clone https://github.com/iamctodd/flask_login_dashboard.git
cd flask_login_dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. Edit `.env` and add your OAuth credentials:
```
SECRET_KEY=your-random-secret-key
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Click "Login" and choose your preferred OAuth provider

## Project Structure

```
flask_login_dashboard/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore rules
└── templates/         # HTML templates
    ├── base.html      # Base template
    ├── index.html     # Home page
    ├── login.html     # Login page
    └── dashboard.html # Dashboard page
```

## Security Notes

- Never commit your `.env` file or expose your OAuth secrets
- Use strong, random values for `SECRET_KEY` in production
- For production deployment, use a proper database (PostgreSQL, MySQL) instead of SQLite
- Configure proper HTTPS and update OAuth redirect URIs accordingly

## Adding More OAuth Providers

The application uses Authlib, which supports many OAuth providers. To add a new provider:

1. Register your app with the OAuth provider
2. Add the credentials to `.env`
3. Update `config.py` with the new configuration
4. Register the OAuth provider in `app.py`
5. Add routes for login and authorization
6. Update the login template with a button for the new provider

## License

MIT License - see LICENSE file for details
