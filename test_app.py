"""
Simple test to verify Flask OAuth Dashboard setup
"""
import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        from app import app, db, oauth, github, google
        from models import User
        from config import Config
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config():
    """Test configuration is properly set up"""
    print("\nTesting configuration...")
    try:
        from app import app
        assert app.config['SECRET_KEY'] is not None
        assert app.config['SQLALCHEMY_DATABASE_URI'] is not None
        print("✓ Configuration loaded successfully")
        print(f"  - Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"  - Secret Key: {'Set' if app.config['SECRET_KEY'] else 'Not set'}")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_routes():
    """Test that all expected routes are registered"""
    print("\nTesting routes...")
    try:
        from app import app
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/login', '/login/github', '/authorize/github', 
                          '/login/google', '/authorize/google', '/dashboard', '/logout']
        
        for route in expected_routes:
            if route in routes:
                print(f"✓ Route {route} registered")
            else:
                print(f"✗ Route {route} missing")
                return False
        return True
    except Exception as e:
        print(f"✗ Route test failed: {e}")
        return False

def test_database():
    """Test database model and creation"""
    print("\nTesting database...")
    try:
        from app import app, db
        from models import User
        
        with app.app_context():
            # Try to create tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Verify User model has required fields
            required_fields = ['id', 'username', 'email', 'oauth_provider', 'oauth_id']
            for field in required_fields:
                if hasattr(User, field):
                    print(f"✓ User model has '{field}' field")
                else:
                    print(f"✗ User model missing '{field}' field")
                    return False
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_templates():
    """Test that all template files exist"""
    print("\nTesting templates...")
    templates = ['base.html', 'index.html', 'login.html', 'dashboard.html']
    template_dir = 'templates'
    
    for template in templates:
        path = os.path.join(template_dir, template)
        if os.path.exists(path):
            print(f"✓ Template {template} exists")
        else:
            print(f"✗ Template {template} missing")
            return False
    return True

def main():
    print("=" * 60)
    print("Flask OAuth Dashboard - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_routes,
        test_database,
        test_templates
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
