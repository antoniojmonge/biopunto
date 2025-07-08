from flask import Blueprint, render_template, request, session, redirect, url_for
from mysql.connector import Error

routes_main = Blueprint("routes",__name__)

#-----------ENRUTADOR DE LINKS -----------
@routes_main.route('/routes', methods=["GET"])
def routes():
    if 'username' not in session:
        return redirect('/')
    
    return render_template('/dashboard.html',
                           username=session.get('username'),                     
                           )

@routes_main.route('/today', methods=['GET'])
def today():
    if 'username' not in session:
        return redirect('/')
    return render_template('today.html')

@routes_main.route('/help', methods = ["GET"])
def help():
    if 'username' not in session:
        return redirect('/')
    return  render_template('help.html')

@routes_main.route('/docs', methods=['GET'])
def docs():
    if 'username' not in session:
        return redirect('/')
    return render_template('docs.html')

@routes_main.route('/account', methods=['GET'])
def account():
    if 'username' not in session:
        return redirect('/')
    return render_template('account.html',
                           username=session.get('username'))

@routes_main.route('/users', methods=["GET"])
def users():
    if 'username' not in session:
        return redirect('/')
    return render_template('users.html')

@routes_main.route('/enterprise', methods=["GET"])
def enterprise():
    if 'username' not in session:
        return redirect ('/')
    return render_template('enterprise.html')

@routes_main.route('/device', methods =["GET"])
def device():
    if 'username' not in session:
        return redirect('/')
    return render_template('device.html')


@routes_main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



