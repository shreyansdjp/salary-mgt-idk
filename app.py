from flask import Flask, render_template, flash, request, redirect, url_for, session
from functools import wraps
from mysql import get_connection
from helpers import Company, Administrator

app = Flask(__name__)
# i know i know
app.secret_key = '1Fb56I77YfwV14dPBc36'


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = '0374b97ace9317f3012a541291ae83db'
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token


# custom decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/company/register', methods=["POST", "GET"])
def company():
    if request.method == "POST":
        name = request.form['company_name']
        address = request.form['company_address']
        registration_no = request.form['company_registration_no']
        owner_full_name = request.form['full_name']
        username = request.form['username']
        password = request.form['password']
        if name == '' or address == '' or registration_no == '' \
            or owner_full_name == '' or username == '' or password == '':
            flash('You forgot to enter some fields', 'danger')
            return redirect(url_for('company'))
        company = Company()
        if company.create(name, address, registration_no):
            print('made a company')
            company_data = company.get(name, registration_no)
            print('got data')
            if company_data:
                administrator = Administrator()
                print('making new administrator')
                if administrator.create(owner_full_name, username, password, company_data['id'], is_owner=1, is_supervisor=1):
                    print('made one')
                    flash('You have successfully registered and can login', 'success')
                    return redirect(url_for('login'))
                print('not working')
    else:
        return render_template('company.html')


@app.route('/user/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        administrator = Administrator()
        verification_and_data = administrator.verify_and_get(username, password)
        if verification_and_data:
            session['id'] = verification_and_data['id']
            session['username'] = verification_and_data['username']
            session['is_owner'] = verification_and_data['is_owner']
            session['is_supervisor'] = verification_and_data['is_supervisor']
            session['company_id'] = verification_and_data['company_id']
            flash('You are now successfully logged in', 'success')
            return redirect(url_for('employees'))
    else:
        return render_template('login.html')


@app.route('/user/logout')
@login_required
def logout():
    session.clear()
    flash('Successfully Logged Out', 'success')
    return redirect(url_for('login'))

@app.route('/user/employees')
@login_required
def employees():
    return render_template('employees.html')


@app.route('/user/employees/add', methods=["POST", "GET"])
@login_required
def add_employees():
    if request.method == "POST":
        pass
    else:
        return render_template('add_employees.html')


@app.route('/user/administrators/add', methods=["POST", "GET"])
@login_required
def add_administrators():
    if request.method == "POST":
        pass
    else:
        return render_template('add_administrators.html')


@app.route('/user/employees/<int:id>', methods=["POST", "GET"])
@login_required
def employee():
    if request.method == "POST":
        pass
    else:
        return render_template('employee.html')


@app.route('/user/employees/<int:id>/view')
@login_required
def view():
    return render_template('view.html')


if __name__ == '__main__':
    app.run(debug=True, port=2000)