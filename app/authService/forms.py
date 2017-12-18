from flask_security.forms import RegisterForm, ConfirmRegisterForm
from wtforms import TextField, SelectField
from wtforms.validators import Required
import pycountry

#TODO: Refactor me and remove static list. Use DB

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

class AHARegisterForm(RegisterForm):
    name = TextField('Full Name', [Required()])
    sex = SelectField(u'Sex', choices=[("", "---"), ("M", "Male"), ("F", "Female")])
    city = TextField('City')
    state = TextField('State')
    country = SelectField(u'Country', choices=[(country.alpha_2, country.name) for country in pycountry.countries])
    nationality = SelectField(u'Nationality', choices=[(i+1, n) for i,n in enumerate(nationalities)], coerce=int)
    occupation = SelectField(u'Occupation', choices=[(i+1, n) for i,n in enumerate(occupations)], coerce=int)

class AHAConfirmForm(ConfirmRegisterForm):
    name = TextField('Full Name', [Required()])
    sex = SelectField(u'Sex', choices=[("", "---"), ("M", "Male"), ("F", "Female")])
    city = TextField('City')
    state = TextField('State')
    country = SelectField(u'Country', choices=[(country.alpha_2, country.name) for country in pycountry.countries])
    nationality = SelectField(u'Nationality', choices=[(i+1, n) for i,n in enumerate(nationalities)], coerce=int)
    occupation = SelectField(u'Occupation', choices=[(i+1, n) for i,n in enumerate(occupations)], coerce=int)

