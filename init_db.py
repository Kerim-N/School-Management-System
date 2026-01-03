from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database and create default users"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Create default director if not exists
        if not User.query.filter_by(username='director').first():
            director = User(
                username='director',
                password=generate_password_hash('director123'),
                full_name='Direktor',
                role='director'
            )
            db.session.add(director)
            db.session.commit()
            print("✓ Default director created:")
            print("  Username: director")
            print("  Password: director123")
        else:
            print("✓ Director already exists")
        
        print("\nDatabase initialization completed!")
        print("You can now run: python app.py")

if __name__ == '__main__':
    init_database()