from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
from models import db, Users, Patient, Doctor, Staff, Pharmacy

#creating the app and defining th path of db
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.sqlite'
app.config["SECRET_KEY"] = "supersecretkey"

#initialising database and login manager
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#----------------------------------- HOME PAGE REDIRECTING TO LOGIN PAGE ----------------------------------------

@app.route('/')
def home():
    return redirect(url_for("login",message="Welcome"))

#----------------------------------ADMIN REGISTER'S ANYBODY------------------------------------------------------

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        id = request.form.get("id")
        username = request.form.get("username")
        password = request.form.get("password")

        if Users.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already taken!")

        new_user = Users(username=username, password=password, flag="Active")
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

#---------------------------------- REGISTARTION BY DOCTOR/STAFF/PHARMACY --------------------------------------------------------

@app.route('/registration-form', methods=["GET","POST"])
def registration():
    time=datetime.datetime.now()

    if request.method == "POST":
        designation = request.form.get("designation")

        if designation == "doctor":
            name = request.form.get("name")
            imcid = request.form.get("imcid")
            aadhar= request.form.get("aadhar")
            city = request.form.get("city")
            state = request.form.get("state")

            newd = Doctor(name=name, imcid=imcid, aadhar=aadhar, city=city, state=state)
            db.session.add(newd)
            db.session.commit()

            newu = Users(username=imcid, password=name)
            db.session.add(newu)
            db.session.commit()

            return redirect(url_for("login", message="Registered Successfully, Kindly Wait for admin approval!"))
        
        elif designation == "staff":
            name = request.form.get("name")
            aadhar= request.form.get("aadhar")
            city = request.form.get("city")
            state = request.form.get("state")

            newd = Staff(name=name, aadhar=aadhar, city=city, state=state)
            db.session.add(newd)
            db.session.commit()

            newu = Users(username=aadhar, password=name)
            db.session.add(newu)
            db.session.commit()

            return redirect(url_for("login", message="Registered Successfully, Kindly Wait for admin approval!"))
        
        elif designation == "pharmacy":
            name = request.form.get("name")
            aadhar= request.form.get("aadhar")
            city = request.form.get("city")
            state = request.form.get("state")

            newd = Pharmacy(name=name, aadhar=aadhar, city=city, state=state)
            db.session.add(newd)
            db.session.commit()

            newu = Users(username=aadhar, password=name)
            db.session.add(newu)
            db.session.commit()

            return redirect(url_for("login", message="Registered Successfully, Kindly Wait for admin approval!"))
        return render_template("registration.html")
    return render_template("registration.html", time=time)

#------------------------------------------------ USER LOGIN PORTAL ---------------------------------------------------------

@app.route('/login', methods=["GET","POST"])
def login():
    time=datetime.datetime.now()
    msg = request.args.get("message")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and user.password==password :
            login_user(user)
            return redirect(url_for("reception",message = "Welcome "+ user.username))
        else:
            return redirect(url_for("registration", error = "Invalid username or password!"))
            #return render_template("login.html", error = "Invalid username or password!", time=time)
    return render_template('login.html',time=time,message=msg)

#---------------------------------------------- RECEPTIONIST DASHBOARD -------------------------------------------------------------

@app.route('/reception', methods=["GET","POST"])
@login_required
def reception():
    msg = request.args.get("message")
    time = datetime.datetime.now()
    return render_template("reception.html",time=time, message=msg)

#--------------------------------------------- LOGOUT FACILITY ----------------------------------------------------

@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

#------------------------------------------- PATIENT ADMISSION FORM ---------------------------------------------

@app.route('/admission', methods=["GET","POST"])
@login_required
def admission():
    if request.method == "POST":
        name = request.form.get("name")
        uhid = request.form.get("uhid")
        aadhar = request.form.get("aadhar")
        city = request.form.get("city")
        state = request.form.get("state")
        mobile = request.form.get("mobile")
        emergency = request.form.get("emergency")
        doctor = request.form.get("doctor")
        department = request.form.get("department")
        docid = request.form.get("docid")
        date = request.form.get("date")

        newp = Patient(name=name, uhid=uhid, aadhar=aadhar, city=city, state=state, mobile=mobile, emergency=emergency, doctor=doctor, department=department, docid=docid, date=date)
        db.session.add(newp)
        db.session.commit()
        
        return redirect(url_for("reception", message="Patient Registered Successfully!"))
    return render_template("admission.html")
#----------------------------------------- PATIENT SEARCH -------------------------------------------------

#@app.route('/search')

#----------------------------------------- PATIENT RECORDS ------------------------------------------------

@app.route('/patientrecord', methods=["GET","POST"])
def patientrecord():
    patients = Patient.query.all()
    return render_template("patientrecord.html",patients=patients)

#-------------------------------------Doctor Schedule -----------------------------------------------------

@app.route('/doctor-schedule', methods=["GET"])
def doctor_schedule():
    # Get the ID from the search input field
    search_id = request.args.get('doctor_id')
    appointments = []
    
    if search_id:
        # Filter patients by the doctor's ID
        # Ensure your Patient model has doctor_id as we discussed
        appointments = Patient.query.filter_by(docid=search_id).all()
        
    return render_template("doctor_schedule.html", appointments=appointments, search_id=search_id)


#------------------------------------------------ FINAL RUN THE APP ----------------------------------------
if __name__=="__main__":
    app.run(debug=True)