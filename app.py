from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import subprocess
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

# Configuración de autenticación
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Credenciales desde variables de entorno
VALID_USERNAME = os.environ.get('LOGIN_USERNAME', 'admin')
VALID_PASSWORD = os.environ.get('LOGIN_PASSWORD', 'admin123')

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id == VALID_USERNAME else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            user = User(username)
            login_user(user)
            return redirect(url_for('list_containers'))
        
        return "Credenciales inválidas", 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def list_containers():
    try:
        result = subprocess.check_output(['docker', 'ps', '-a', '--format', '{{.Names}} | {{.Status}}'])
        containers = [line.split(' | ') for line in result.decode().split('\n') if line]
        return render_template('containers.html', containers=containers)
    except Exception as e:
        return str(e), 500

@app.route('/logs/<container_name>')
@login_required
def show_logs(container_name):
    try:
        logs = subprocess.check_output(['docker', 'logs', '--tail', '200', container_name])
        return render_template('logs.html', 
                             container_name=container_name,
                             logs=logs.decode('utf-8', errors='replace'))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)