from flask import Flask, render_template, flash, request, redirect, url_for

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


if __name__ == '__main__':
    app.run(debug=True, port=2000)