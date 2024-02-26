#python3 -m venv venv
#source venv/bin/activate (deactivate)
#pip install -r requirements.txt
#createdb employees_db
#python3 seed.py
#python3 app.py(auto reload if app.debug=True) or flask run
#################################################################################
import os
from flask import Flask,request,render_template,redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension#put raise where to inspect with debugtool
from models import db,connect_db,Department,Employee,Project,EmployeeProject,get_directory,get_directory_join,get_directory_join_class,get_directory_all_join
from forms import AddEquipmentForm,EmployeeForm
###########################################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///employees_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False#no intercept redirect
app.debug = True #for auto reload(with command:$python3 app.py, not $flask run)
connect_db(app)#establish connection to database
with app.app_context():#within app context,create tables
    db.create_all()
# toolbar = DebugToolbarExtension(app)
######################################################
@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/employees')
def list_employees():
    emps = Employee.query.all()
    return render_template('employees.html', emps=emps)

@app.route('/equipment/new', methods=["GET", "POST"])
def add_equipment():
    form = AddEquipmentForm()
    if form.validate_on_submit():
        name =form.name.data
        price=form.price.data
        flash(f"Equipment added: {name}, price: ${price}")
        return redirect('/')
    else:
        return render_template("add_equipment_form.html", form=form)
    
@app.route('/employees/new', methods=["GET", "POST"])
def add_employee():
    form = EmployeeForm()
    # depts = db.session.query(Department.dept_code, Department.dept_name)#ORIGINAL CODE: DON'T WORK
    # form.dept_code.choices = depts#ORIGINAL CODE: DON'T WORK
    depts = Department.query.with_entities(Department.dept_code, Department.dept_name).all()#Fetch department codes from db    
    form.dept_code.choices = [(dept.dept_code, dept.dept_name) for dept in depts]#Set department choices for form field

    if form.validate_on_submit():
        name = form.name.data 
        state= form.state.data
        dept_code = form.dept_code.data

        emp = Employee(name=name, state=state, dept_code=dept_code)
        db.session.add(emp)
        db.session.commit()
        return redirect('/employees')
    else:
        return render_template('add_employee_form.html', form=form)
    
@app.route('/employees/<int:id>/edit', methods=["GET", "POST"])
def edit_employee(id):
    emp = Employee.query.get_or_404(id)#will not break code
    form = EmployeeForm(obj=emp)
    depts = Department.query.with_entities(Department.dept_code, Department.dept_name).all()#Fetch department codes from db    
    form.dept_code.choices = [(dept.dept_code, dept.dept_name) for dept in depts]#Set department choices for form field
    if form.validate_on_submit():
        emp.name = form.name.data
        emp.state = form.state.data
        emp.dept_code = form.dept_code.data
        db.session.commit()
        return redirect('/employees')
    else:
        return render_template("edit_employee_form.html", form=form)
#########################################################################
if __name__ == '__main__': app.run(debug=True)