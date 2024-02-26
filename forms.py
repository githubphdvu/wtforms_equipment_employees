from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Optional
#################################################################################################
STATES=["AL","AK","AZ","AR","CA","CO","CT","DC","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO",
        "MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
#################################################################################################
class EmployeeForm(FlaskForm):
    name     =StringField("Name",validators=[InputRequired(message="can't be blank")])
    state    =SelectField('State',choices=[(st, st) for st in STATES])
    dept_code=SelectField("Department Code")
class AddEquipmentForm(FlaskForm):
    name = StringField("Equipment Name", validators=[InputRequired(message="Name can't be blank")])
    price = FloatField("Price $$$")
    quantity = IntegerField("Quantity")
    is_portable = BooleanField("Portable?")
    category = SelectField("Category", choices=[('gym', 'Gym Equipment'), ('kitchen', 'Kitchen Appliances'), ('tech', 'Tech Gadgets')])

