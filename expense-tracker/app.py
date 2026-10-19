from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from database.db import get_db, init_db, seed_db, get_user_by_id, get_user_expense_stats, get_recent_transactions

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        error = None

        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters.'

        if error is None:
            db = get_db()
            try:
                hashed_password = generate_password_hash(password)
                db.execute(
                    'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                    (name, email, hashed_password)
                )
                db.commit()
                db.close()
                return redirect(url_for('login'))
            except db.IntegrityError:
                error = 'Email already registered.'
                db.close()

        return render_template("register.html", error=error)

    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            db = get_db()
            cursor = db.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            db.close()

            if user and check_password_hash(user['password_hash'], password):
                session.clear()
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                return redirect(url_for('profile'))
            else:
                error = 'Incorrect email or password.'

        return render_template("login.html", error=error)

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('landing'))


@app.route("/profile")
def profile():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    user = get_user_by_id(user_id)
    stats = get_user_expense_stats(user_id)
    recent_transactions = get_recent_transactions(user_id, limit=5)

    category_colors = {
        'Food': '#1a472a',        # Accent green
        'Transport': '#d4a574',   # Tan
        'Bills': '#4a90e2',       # Blue
        'Health': '#c0392b',      # Red
        'Entertainment': '#9b59b6', # Purple
        'Shopping': '#c17f24',    # Accent orange
        'Other': '#a0a0a0'        # Gray
    }

    return render_template("profile.html", user=user, stats=stats, recent_transactions=recent_transactions, category_colors=category_colors)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
