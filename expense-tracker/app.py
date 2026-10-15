from flask import Flask, render_template

app = Flask(__name__)


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")
Add a modal to @templates/landing.html that opens when the user
clicks
"See how it works".

Requirements:

Clicking "See how it works" opens a modal overlay
- Modal contains an embedded YouTube video (use any placeholder
YouTube URL
for now, I will replace it later)
- Video should be playable inside the modal
- Clicking the close button OR clicking outside the modal closes
it
- When the modal closes, the video must stop playing (not
continue in background)
- No page libraries or dependencies - vanilla JS only, since we
are not
using any JS framework in this project

Do not modify any other part of the page.

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
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
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


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
