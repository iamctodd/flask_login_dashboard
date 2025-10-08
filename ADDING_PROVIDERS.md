# Adding Additional OAuth Providers

This guide explains how to add more OAuth providers to the Flask Login Dashboard.

## Supported by Authlib

The application uses [Authlib](https://docs.authlib.org/), which supports many OAuth providers including:
- GitHub ✅ (Already implemented)
- Google ✅ (Already implemented)
- Microsoft/Azure AD
- Facebook
- Twitter
- LinkedIn
- GitLab
- Bitbucket
- Discord
- And many more...

## Step-by-Step Guide

### 1. Register Your Application with the OAuth Provider

Each provider has a developer portal where you can register your app:
- **Microsoft**: https://portal.azure.com/ → Azure AD → App registrations
- **Facebook**: https://developers.facebook.com/apps/
- **Twitter**: https://developer.twitter.com/en/portal/dashboard
- **LinkedIn**: https://www.linkedin.com/developers/apps
- **GitLab**: https://gitlab.com/-/profile/applications
- **Discord**: https://discord.com/developers/applications

When registering:
1. Set the redirect/callback URL to: `http://localhost:5000/authorize/<provider_name>`
2. Note down the Client ID and Client Secret

### 2. Update Configuration

Add the credentials to `.env`:
```bash
# Example for Microsoft
MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret
```

Add to `config.py`:
```python
# Microsoft OAuth
MICROSOFT_CLIENT_ID = os.environ.get('MICROSOFT_CLIENT_ID')
MICROSOFT_CLIENT_SECRET = os.environ.get('MICROSOFT_CLIENT_SECRET')
```

### 3. Register OAuth Provider in app.py

Add the provider configuration after the existing ones:

```python
# Microsoft OAuth configuration
microsoft = oauth.register(
    name='microsoft',
    client_id=app.config['MICROSOFT_CLIENT_ID'],
    client_secret=app.config['MICROSOFT_CLIENT_SECRET'],
    server_metadata_url='https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)
```

### 4. Add Login and Authorization Routes

```python
@app.route('/login/microsoft')
def login_microsoft():
    redirect_uri = url_for('authorize_microsoft', _external=True)
    return microsoft.authorize_redirect(redirect_uri)

@app.route('/authorize/microsoft')
def authorize_microsoft():
    token = microsoft.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        # Get or create user
        user = User.query.filter_by(
            oauth_provider='microsoft', 
            oauth_id=user_info['sub']
        ).first()
        
        if not user:
            user = User(
                username=user_info.get('email', '').split('@')[0],
                email=user_info.get('email'),
                oauth_provider='microsoft',
                oauth_id=user_info['sub'],
                avatar_url=user_info.get('picture')
            )
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
    
    return redirect(url_for('dashboard'))
```

### 5. Update Login Template

Add a button in `templates/login.html`:

```html
<a href="{{ url_for('login_microsoft') }}" class="btn btn-microsoft">
    <svg style="width: 20px; height: 20px; vertical-align: middle; margin-right: 8px;" 
         fill="currentColor" viewBox="0 0 24 24">
        <!-- Add Microsoft icon SVG here -->
    </svg>
    Login with Microsoft
</a>
```

Add CSS for the button in `templates/base.html`:

```css
.btn-microsoft {
    background: #00a4ef;
    color: white;
}
```

## Provider-Specific Notes

### OAuth 1.0a Providers (e.g., Twitter)

For OAuth 1.0a providers like Twitter, use different configuration:

```python
twitter = oauth.register(
    name='twitter',
    client_id=app.config['TWITTER_CLIENT_ID'],
    client_secret=app.config['TWITTER_CLIENT_SECRET'],
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    api_base_url='https://api.twitter.com/1.1/',
)
```

### OIDC Providers

For OpenID Connect providers, you can use the `server_metadata_url`:

```python
# Google, Microsoft, and many others support OIDC
provider = oauth.register(
    name='provider_name',
    client_id=app.config['PROVIDER_CLIENT_ID'],
    client_secret=app.config['PROVIDER_CLIENT_SECRET'],
    server_metadata_url='https://provider.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)
```

## Testing New Providers

1. Start the app: `python app.py`
2. Navigate to http://localhost:5000/login
3. Click the new provider button
4. Complete the OAuth flow
5. Verify you're redirected to the dashboard with user info

## Common Issues

### Invalid Redirect URI
- Ensure the callback URL matches exactly what you configured in the provider's settings
- Use `_external=True` in `url_for()` to generate absolute URLs

### Missing User Info
- Check the provider's documentation for the correct scope
- Some providers require additional API calls to fetch user profile

### Token Errors
- Verify client ID and secret are correct
- Check if the provider requires specific token parameters

## Resources

- [Authlib Documentation](https://docs.authlib.org/en/latest/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [OpenID Connect](https://openid.net/connect/)
