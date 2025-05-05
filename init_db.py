from app import app, db
from app.models import Poll, PollDate, Response, ResponseSelection
import os

def init_db():
    """Initialize the database with all required tables."""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Run any pending migrations
        from flask_migrate import upgrade
        upgrade()
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize the database
    init_db() 