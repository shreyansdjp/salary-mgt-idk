from flask import Flask, render_template, flash, request, redirect, url_for, session, abort
from functools import wraps
from mysql import get_connection
from helpers import Company, Administrator, Employee, check_int

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
            company_data = company.get(name, registration_no)
            if company_data:
                administrator = Administrator()
                if administrator.create(owner_full_name, username, password, company_data['id'], is_owner=1, is_supervisor=1):
                    flash('You have successfully registered and can login', 'success')
                    return redirect(url_for('login'))
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
            session['name'] = verification_and_data['name']
            session['is_owner'] = verification_and_data['is_owner']
            session['is_supervisor'] = verification_and_data['is_supervisor']
            session['company_id'] = verification_and_data['company_id']
            flash('You are now successfully logged in', 'success')
            return redirect(url_for('employees'))
        else:
            flash('Wrong username or password', 'danger')
            return redirect(url_for('login'))
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
    employees = Employee().get(session['company_id'])
    return render_template('employees.html', employees=employees)


@app.route('/user/employees/add', methods=["POST", "GET"])
@login_required
def add_employees():
    if request.method == "POST":
        if session['is_owner'] != 1:
            flash('You are not authorized', 'danger')
            return redirect(url_for('employees'))
        name = request.form['full_name']
        hour_rate = request.form['hour_rate']
        hours_worked = request.form['hours_worked']
        designation = request.form['designation']
        department_no = request.form['department_no']

        if name == '' or hour_rate == '' or  hours_worked == '' \
            or designation == '' or department_no == '':
            flash('You forgot to enter some fields', 'danger')
            return redirect(url_for('add_employees'))

        if not (check_int(hour_rate) and check_int(hours_worked)):
            flash('You did not enter correct Hour rate or Hours Worked', 'danger')
            return redirect(url_for('add_employees'))
        
        employee = Employee()
        if employee.create(name, hour_rate, hours_worked, designation, department_no, session['company_id']):
            flash('Successfully added a new Employee', 'success')
            return redirect(url_for('employees'))
        else:
            flash('Something went wrong', 'danger')
            return redirect(url_for('add_employees'))
    else:
        if session['is_owner'] != 1:
            flash('You are not authorized', 'danger')
            return redirect(url_for('employees'))
        return render_template('add_employees.html')


@app.route('/user/employees/<int:id>', methods=["POST", "GET"])
@login_required
def employee(id):
    employee = Employee()
    employee = employee.get_one(id)
    return render_template('employee.html', employee=employee)


@app.route('/user/employees/<int:id>/edit', methods=["POST", "GET"])
@login_required
def edit_employee(id):
    if request.method == "POST":
        if session['is_owner'] != 1 or session['is_supervisor'] != 1:
            flash('You are not authorized', 'danger')
            return redirect(url_for('employees'))
        name = request.form['full_name']
        hour_rate = request.form['hour_rate']
        hours_worked = request.form['hours_worked']
        designation = request.form['designation']
        department_no = request.form['department_no']
        if name == '' or hour_rate == '' or  hours_worked == '' \
            or designation == '' or department_no == '':
            flash('You forgot to enter some fields', 'danger')
            return redirect(url_for('add_employees'))

        if not (check_int(hour_rate) and check_int(hours_worked)):
            flash('You did not enter correct Hour rate or Hours Worked', 'danger')
            return redirect(url_for('add_employees'))
        
        employee = Employee()
        if employee.update(id, name, hour_rate, hours_worked, designation, department_no, session['company_id']):
            flash('Update one Employee', 'success')
            return redirect(url_for('employees'))
        else:
            flash('Something went wrong', 'danger')
            return redirect(url_for('edit_employee'))
    else:
        employee = Employee()
        employee = employee.get_one(id)
        return render_template('edit_employee.html', employee=employee)


@app.route('/user/employees/<int:id>/delete')
@login_required
def delete_employee(id):
    if session['is_owner'] != 1:
            flash('You are not authorized', 'danger')
            return redirect(url_for('employees'))
    employee = Employee()
    if employee.delete(id, session['company_id']):
        flash('Successfully deleted one employee', 'success')
        return redirect(url_for('employees'))
    else:
        flash('Something went wrong', 'danger')
        return redirect(url_for('edit_employee'))


@app.route('/user/employees/<int:id>/view')
@login_required
def view(id):
    overtime = request.args['overtime']
    if not check_int(overtime):
        flash('You did not enter valid input', 'danger')
        return redirect(url_for('employees'))
    employee = Employee()
    employee = employee.get_one(id)
    if overtime != '0':
        total_salary = int(employee['hours_worked']) * int(employee['hour_rate']) * int(overtime)
    else:
        total_salary = int(employee['hours_worked']) * int(employee['hour_rate'])
    return render_template('view.html', employee=employee, overtime=overtime, total_salary=total_salary)


@app.route('/user/administrators/add', methods=["POST", "GET"])
@login_required
def add_administrators():
    if request.method == "POST":
        if session['is_owner'] != 1:
            flash('You are not authorized', 'danger')
            return redirect(url_for('employees'))
        name = request.form['full_name']
        username = request.form['username']
        password = request.form['password']
        try:
            is_owner = request.form['is_owner']
            if not (check_int):
                is_owner = 0
        except Exception as e:
            is_owner = 0

        if name == '' or username == '' or password == '' \
            or is_owner == '':
            flash('Some Field is missing', 'danger')
            return redirect('add_administrators')
        administrator = Administrator()
        if administrator.create(name, username, password, session['company_id'], is_owner):
            flash('Successfully added a new administrator', 'success')
            return redirect(url_for('employees'))
        else:
            flash('Something went wrong', 'danger')
            return redirect(url_for('employees'))
    else:
        if session['is_owner'] != 1:
            flash('You are not authorized', 'danger')
            return redirect(url_for('employees'))
        return render_template('add_administrators.html')

    
@app.route('/user/administrators/<int:id>/edit', methods=["POST", "GET"])
@login_required
def edit_administrators(id):
    if request.method == "POST":
        if session['is_owner'] != 1:
            flash('You are not authorized', 'danger')
            return redirect(url_for('employees'))
        name = request.form['full_name']
        username = request.form['username']
        password = request.form['password']
        try:
            is_owner = request.form['is_owner']
            if not (check_int):
                is_owner = 0
        except Exception as e:
            is_owner = 0

        if name == '' or username == '' or password == '' \
            or is_owner == '':
            flash('Some Field is missing', 'danger')
            return redirect('edit_administrator')
        administrator = Administrator()
        if administrator.update(id, name, username, password, is_owner, session['company_id']):
            flash('Successfully updated administrator', 'success')
            return redirect(url_for('employees'))
        else:
            flash('Something went wrong', 'danger')
            return redirect(url_for('employees'))
    else:
        if session['is_owner'] != 1:
            flash('You are not authorized', 'danger')
            return redirect(url_for('employees'))
        administrator = Administrator().get_one(id)
        return render_template('edit_administrators.html', administrator=administrator)


@app.route('/user/administrators/<int:id>/delete')
@login_required
def delete_administrators(id):
    if session['is_owner'] != 1:
            flash('You are not authorized', 'danger')
            return redirect(url_for('employees'))
    administrator = Administrator()
    if administrator.delete(id, session['company_id']):
        flash('Successfully deleted one employee', 'success')
        return redirect(url_for('employees'))
    else:
        flash('Something went wrong', 'danger')
        return redirect(url_for('view_administrators'))


@app.route('/user/administrators/', methods=["POST", "GET"])
@login_required
def view_administrators():
    administrators = Administrator().get(session['company_id'])
    return render_template('administrators.html', administrators=administrators)


if __name__ == '__main__':
    app.run(debug=True, port=2000)