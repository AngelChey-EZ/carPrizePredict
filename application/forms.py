from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField, StringField, PasswordField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import Length, InputRequired, NumberRange, Optional
import datetime 

# login form
class LoginForm(FlaskForm):
    userName = StringField("User Name", validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("Log In")
    
# sign up form
class SignUpForm(FlaskForm):
    userName = StringField("User Name", validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("Sign Up")
    
# predict form
class PredictForm(FlaskForm):
    # 1980 to year now, data range: 1994 - 2020
    year_purchase = IntegerField('Year of Purchase', validators=[InputRequired(), NumberRange(1980, datetime.date.today().year)])
    # unit cc/l, 1000cc-1L, data range: 624 - 3604 in cc
    engine_displacement = DecimalField('Engine Displacement ', validators=[InputRequired()], places=1)
    engine_unit = SelectField('engine_unit', choices=[('1', 'cc'), ('2', 'L')], default='1')
    # unit hp or kw, 1hp = 745.7 watts, 1kw=1000watts, data range: 32.8 - 400.0 in hp
    max_power = DecimalField('Max Power', places=1, validators=[InputRequired()])
    max_power_unit = SelectField('max_power_unit', choices=[('1', 'hp'), ('2', 'kw')], default='1')
    
    # data range: 47.1 - 1863.9 in nm, Nm and kgm, 1kgm = 9.81Nm
    torque = DecimalField('Torque', places=1, validators=[InputRequired()])
    torque_unit = SelectField('torque_unit', choices=[('1', 'Nm'), ('2', 'kgm')], default='1')
    # 31 unique brand
    brand = SelectField('Brand', 
                        choices=[('1', 'Ambassador'), ('2', 'Ashok'), ('3', 'Audi'), 
                                 ('4', 'BMW'), ('5', 'Chevrolet'), ('6', 'Daewoo'), 
                                 ('7', 'Datsun'), ('8', 'Fiat'), ('9', 'Force'), 
                                 ('10', 'Ford'), ('11', 'Honda'), ('12', 'Hyundai'), 
                                 ('13', 'Isuzu'), ('14', 'Jaguar'), ('15', 'Jeep'),
                                 ('16', 'Kia'), ('17' ,'Land'), ('18', 'Lexus'), 
                                 ('19', 'MG'), ('20', 'Mahindra'), ('21', 'Maruti'), 
                                 ('22', 'Mercedes'), ('23', 'Mitsubishi'), ('24', 'Nissan'), 
                                 ('25', 'Opel'), ('26', 'Renault'), ('27', 'Skoda'), ('28', 'Tata' ),
                                 ('29', 'Toyota'), ('30', 'Volkswagen'), ('31', 'Volvo')])
    # ['Diesel' 'Petrol' 'LPG' 'CNG']
    fuel = SelectField('Fuel', choices=[('1', 'CNG'), ('2', 'Diesel'), ('3', 'LPG'), ('4', 'Petrol') ])
    # ['First_Owner' 'Second_Owner' 'Third_Owner' 'Fourth_Above_Owner' 'Test_Drive_Car']
    owner = SelectField('Owner Type', choices=[('1', 'First_Owner'), ('2', 'Second_Owner'), 
                                               ('3', 'Third_Owner'), ('4', 'Fourth_Above_Owner'), ('5', 'Test_Drive_Car') ])
    submit = SubmitField("Predict")
    
# search form 
class SearchForm(FlaskForm):
    yp_min = IntegerField('Year of Purchase', validators=[Optional()])
    yp_max = IntegerField('Year of Purchase Max', validators=[Optional()])

    ed_max = DecimalField('Engine Displacement Max', places=1, validators=[Optional()])
    ed_min = DecimalField('Engine Displacement', places=1, validators=[Optional()])
    engine_unit = SelectField('engine_unit', choices=[('1', 'cc'), ('2', 'L')], default='1')

    mp_max = DecimalField('Max Power Max', places=1, validators=[Optional()])
    mp_min = DecimalField('Max Power', places=1, validators=[Optional()])
    max_power_unit = SelectField('max_power_unit', choices=[('1', 'hp'), ('2', 'kw')], default='1')
    
    t_min = DecimalField('Torque', places=1, validators=[Optional()])
    t_max = DecimalField('Torque Max', places=1, validators=[Optional()])
    torque_unit = SelectField('torque_unit', choices=[('1', 'Nm'), ('2', 'kgm')], default='1')
    # 31 unique brand
    brand = SelectMultipleField('Brand', 
                        choices=[('1', 'Ambassador'), ('2', 'Ashok'), ('3', 'Audi'), 
                                 ('4', 'BMW'), ('5', 'Chevrolet'), ('6', 'Daewoo'), 
                                 ('7', 'Datsun'), ('8', 'Fiat'), ('9', 'Force'), 
                                 ('10', 'Ford'), ('11', 'Honda'), ('12', 'Hyundai'), 
                                 ('13', 'Isuzu'), ('14', 'Jaguar'), ('15', 'Jeep'),
                                 ('16', 'Kia'), ('17' ,'Land'), ('18', 'Lexus'), 
                                 ('19', 'MG'), ('20', 'Mahindra'), ('21', 'Maruti'), 
                                 ('22', 'Mercedes'), ('23', 'Mitsubishi'), ('24', 'Nissan'), 
                                 ('25', 'Opel'), ('26', 'Renault'), ('27', 'Skoda'), ('28', 'Tata' ),
                                 ('29', 'Toyota'), ('30', 'Volkswagen'), ('31', 'Volvo')])
    # ['Diesel' 'Petrol' 'LPG' 'CNG']
    fuel = SelectMultipleField('Fuel', choices=[('1', 'CNG'), ('2', 'Diesel'), ('3', 'LPG'), ('4', 'Petrol') ])
    # ['First_Owner' 'Second_Owner' 'Third_Owner' 'Fourth_Above_Owner' 'Test_Drive_Car']
    owner = SelectMultipleField('Owner Type', choices=[('1', 'First_Owner'), ('2', 'Second_Owner'), 
                                               ('3', 'Third_Owner'), ('4', 'Fourth_Above_Owner'), ('5', 'Test_Drive_Car') ])
    submit = SubmitField("Search")
    