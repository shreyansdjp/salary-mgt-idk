from flask import Flask, render_template, flash, request, redirect, url_for
from mysql import get_connection

app = Flask(__name__)
# i know i know
app.secret_key = '1Fb56I77YfwV14dPBc36'

# custom decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in request.session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    # flash(u'congratulations', 'success')
    return render_template('landing.html')


@app.route('/company')
def company():
    return render_template('company.html')


@app.route('/company/user')
def company_user():
    if request.method == "POST":
        pass
    else:
        return render_template('company_user.html')


@app.route('/user/login')
def login():
    if request.method == "POST":
        pass
    else:
        return render_template('login.html')


@app.route('/user/employees')
@login_required
def employees():
    return render_template('employees.html')


@app.route('/user/employees/<int:id>')
@login_required
def employee():
    return render_template('employee.html')


@app.route('/user/employees/<int:id>/view')
@login_required
def view():
    return render_template('view.html')


if __name__ == '__main__':
    app.run(debug=True, port=2000)