from flask import Flask, render_template, request, redirect, flash, session, url_for
from routes import routes_main
from ep_users import endpoint_user
from ep_dashboard import endpoint_dashboard
from ep_reports import endpoint_reports
from ep_today import ep_today
from ep_enterprise import endpoint_enterprise
from ep_device import endpoint_device

app = Flask(__name__)
app.secret_key = 'tu_secreto_aqui'

#-----------Registro de Blue Prints -----------#
app.register_blueprint(routes_main)
app.register_blueprint(endpoint_user)
app.register_blueprint(endpoint_dashboard)
app.register_blueprint(endpoint_reports)
app.register_blueprint(ep_today)
app.register_blueprint(endpoint_enterprise)
app.register_blueprint(endpoint_device)

#----------- Validacion temporal del login -----------#
#usuarios
USUARIOS = {
    "luis":"123"
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if username in USUARIOS  and USUARIOS[username] == password:
            session['username'] = username
            return redirect(url_for('routes.routes'))
        else:
            flash("Error de credenciales")
    return render_template('login.html', error=error)

if __name__=='__main__':
    app.run(debug=True)
