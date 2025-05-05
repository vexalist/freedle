from app import app
from init_db import init_db
import os

if __name__ == '__main__':
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize database
    init_db()
    
    # Run the Flask application
    app.run(host='0.0.0.0', port=5001, debug=True) 