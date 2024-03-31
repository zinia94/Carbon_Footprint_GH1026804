from wtforms import SubmitField, FloatField, ValidationError
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm

# carbon calculation query forms

class EnergyUsageForm(FlaskForm):
    title = 'Energy Usage'
    avgElectricityBill = FloatField('What is your average monthly electricity bill in euros?', validators=[InputRequired()])
    naturalGasBill = FloatField('What is your average monthly natural gas bill in euros?', validators=[InputRequired()])
    avgFuelBill = FloatField('What is your average monthly fuel bill for transportation in euros?', validators=[InputRequired()])
    submit = SubmitField('Next')


class WasteForm(FlaskForm):
    title = 'Waste'
    wasteGenerated = FloatField('How much waste do you generate per month in kilograms?', validators=[InputRequired()])
    wasteRecycled = FloatField('How much of that waste is recycled or composed per month in kilograms?', validators=[InputRequired()])
    submit = SubmitField('Next')
    
    def validate_wasteRecycled(form, field):
        if form.data['wasteRecycled'] > form.data['wasteGenerated'] :
            raise ValidationError("Recycled waste can't be larger than generated waste!")


class BusinessTravelForm(FlaskForm):
    title = 'Business Travel'
    travelPerYear = FloatField('How many kilometers do your employees travel per year for business purposes?', validators=[InputRequired()])
    fuelEfficiency = FloatField('What is the average fuel efficiency of the vehicles used for business travel in liters per 100 kilometers?', validators=[InputRequired()])
    submit = SubmitField('Next')