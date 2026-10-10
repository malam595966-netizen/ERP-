"""WSGI entry point for production deployment."""
import os
from app import create_app, seed_database

app = create_app()

# Optional: Uncomment to seed database on first deployment
# if __name__ != "__main__":
#     with app.app_context():
#         seed_database(app)

if __name__ == "__main__":
    app.run()
