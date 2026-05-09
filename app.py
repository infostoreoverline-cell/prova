from flask import Flask
from extensions import db, login_manager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Vercel's file system is read-only except for /tmp
if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/site.db')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'main.login'

from routes import bp as main_bp
app.register_blueprint(main_bp)

with app.app_context():
    import models
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
