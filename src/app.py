# Externals
from flask import Flask
import os

# Personal
from config import config
from routes import main

# Config app
flask_env = os.environ.get('FLASK_ENV', 'development')

# Create app
app = Flask(__name__)
app.config.from_object(config[flask_env])

# Agregar blueprints
app.register_blueprint(main)

# Run app
if __name__ == "__main__":
        app.run()