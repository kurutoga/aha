from flask_wtf import FlaskForm
from wtforms import TextField, SelectField, StringField
from wtforms.validators import Required, DataRequired, Email
import pycountry

nationalities = [ "Caucasian", "Hispanic", "African American", "Native American", "Asian", \
                  "Multiple nationalities", "Other", "Do not want to report" ]
occupations = [ "Homemaker", "Retired", "Student", "Unemployed", "Agriculture, Forestry, Fishing, or Hunting",\
                "Arts, Entertainment, or Recreation","Broadcasting","Education - College, University, or Adult",\
                "Education - Primary/Secondary (K-12)","Education - Other","Construction","Finance and Insurance",\
                "Government and Public Administration","Health Care and Social Assistance","Hotel and Food Services",\
                "Information - Services and Data","Information - Other","Processing","Legal Services",\
                "Manufacturing - Computer and Electronics", "Manufacturing - Other", "Military", "Mining",\
                "Publishing", "Real Estate, Rental, or Leasing","Religious","Retail","Scientific or Technical Services","Software","Telecommunications",\
                "Transportation and Warehousing","Utilities","Wholesale","Other"]

class UserEditForm(FlaskForm):
    name = TextField('Full Name', [Required()])
    nickname = TextField('Nick Name')
    sex = SelectField(u'Sex', choices=[("", "---"), ("M", "Male"), ("F", "Female")])
    city = TextField('City')
    state = TextField('State')
    country = SelectField(u'Country', choices=[(country.alpha_2, country.name) for country in pycountry.countries])
    nationality = SelectField(u'Nationality', choices=[(i+1, n) for i,n in enumerate(nationalities)], coerce=int)
    occupation = SelectField(u'Occupation', choices=[(i+1, n) for i,n in enumerate(occupations)], coerce=int)

class UserVerifyForm(FlaskForm):
    email = StringField('Student Email Address', [DataRequired(), Email()])
