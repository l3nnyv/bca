from flask import Flask, render_template, url_for, redirect, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.events import get_all_events, get_event_by_id, get_events_by_date, get_events_by_category
from models.venues import insert_venue
from models.users import insert_user, get_hashed_password_by_email, check_email, get_user_by_email


app = Flask(__name__)

app.secret_key = 'BAD_SECRET_KEY'

@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
        user_email = request.form["user_email"]
        user_dob = request.form["user_dob"]
        user_phone = request.form["user_phone"]
        user_lname = request.form["user_lname"]
        user_fname = request.form["user_fname"]
        user_postcode = request.form["user_postcode"]
        user_address = request.form["user_address"]
        user_password = request.form["user_password"]
        role_id = request.form["role_id"]
        user_password_hash = generate_password_hash(user_password)
        email_count = check_email(user_email)
        if email_count == 0:
            insert_user(user_email, user_dob, user_phone, user_lname, user_fname, user_postcode, user_address, user_password_hash, role_id)
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        user_email = request.form["user_email"]
        entered_password = request.form["entered_password"]

        hashed_password = get_hashed_password_by_email(user_email)
        if hashed_password != None:
            print(hashed_password["user_hashed_password"])
            if check_password_hash(hashed_password["user_hashed_password"], entered_password):
                user = get_user_by_email(user_email)
                session["logged_in"] = True
                session["user_id"] = user["user_id"]
                session["user_dob"] = user["user_dob"]
                session["user_email"] = user["user_email"]
                session["user_phone"] = user["user_phone"]
                session["user_lname"] = user["user_lname"]
                session["user_fname"] = user["user_fname"]
                session["user_postcode"] = user["user_postcode"]
                session["user_address"] = user["user_address"]
                session["role_id"] = user["role_id"]
                print("logged in!")
                return redirect(url_for("home"))
            else:
                print("Email or password is wrong")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        from_date = request.form["from_date"]
        to_date = request.form["to_date"]
        events = get_events_by_date(from_date, to_date)
        if events == []:
            error_msg = "Sorry, there are no events for the criteria you searched for."
            return render_template("home.html", error_msg = error_msg)
        print(events)
    else:
        events = get_all_events()
        print("getting all events by id")
    try:
        print(session["user_id"])
        print(session["user_email"])
    except:
        print("no session email")
    return render_template("home.html", events = events)

@app.route("/<int:category>/")
def category(category):
    events = get_events_by_category(category)
    return render_template("home.html", events = events)

@app.route("/<int:event_id>", methods=["GET", "POST"])
def event(event_id):
    event = get_event_by_id(event_id)
    print(event)
    return render_template("event.html", event = event)

@app.route("/checkout")
def checkout():
    if session.get('logged_in') == True:
        return render_template("checkout.html")
    else:
        return redirect(url_for('login'))

@app.route("/admin", methods = ["GET", "POST"])
def admin():
    if request.method == "POST":
        venue_name = request.form["venue_name"]
        venue_capacity = request.form["venue_capacity"]
        venue_postcode = request.form["venue_postcode"]
        venue_address = request.form["venue_address"]
        venue_img_paths = request.form.getlist("venue_img_path[]")
        venue_img_alts = request.form.getlist("venue_img_alt[]")
        insert_venue(venue_name, venue_capacity, venue_postcode, venue_address, venue_img_paths, venue_img_alts)
    return render_template("admin.html")