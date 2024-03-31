from flask import redirect, render_template, url_for, request
import flask_excel as excel
from .query_form import BusinessTravelForm, EnergyUsageForm, WasteForm
from src.db import BusinessTravel, EnergyUsage, Waste, getHistory, getRecord, saveData

class Routes:
    def __init__(self, app, session) -> None:
        self.app = app
        self.session = session
    
    def initRoutes(self):
        @self.app.route('/')
        def index():
            self.session.clear() # clear session while starting the app
            return render_template('home.html')
        
        @self.app.route("/calculate-carbon-footprint/", methods=['GET'])
        def calculateCarbonFootprint():
            return redirect(url_for('step', step=1))
        
        @self.app.route("/export", methods=['GET'])
        def doExport():
            (_, data) = getHistory()
            return excel.make_response_from_records(data , "xlsx", file_name="carbon_footprint")
        
        @self.app.route("/history", methods=['GET'])
        def history():
            try:
                (columns, data) = getHistory()
                return render_template('history.html',  columns = columns, data = data)
            except:
                return redirect(url_for('error'))
            
        @self.app.route('/error', methods = ['GET'])
        def error():
            return render_template("error.html")
        
        @self.app.route('/suggestion')
        def suggestion():
            return render_template('suggestion.html')
        
        @self.app.route('/calculate-carbon-footprint/result')
        def result():
            return render_template('result.html', data=self.session['result'])
        
        @self.app.route('/calculate-carbon-footprint/step/<int:step>',  methods = ['POST', 'GET'])
        def step(step):
            forms = {
                1: EnergyUsageForm(),
                2: WasteForm(),
                3: BusinessTravelForm()
            }
            form = forms.get(step, 1)
            if request.method == 'POST':
                if form.validate_on_submit():
                    # Save form data to session
    
                    self.session['step{}'.format(step)] = form.data
                    if step < len(forms):
                        # Redirect to next step
                        return redirect(url_for('step', step=step+1))
                    else:
                        #save data to database while redirecting to the result
                        try: 
                            energy_usage = EnergyUsage(self.session['step1'])
                            waste = Waste(self.session['step2'])
                            travel = BusinessTravel(self.session['step3'])
                            saveData(energy_usage, waste, travel)
                            result = getRecord(energy_usage, waste, travel)
                            self.session['result'] = result
                            
                        except: 
                            return redirect(url_for('error'))
                    
                        # Redirect to result
                        return redirect(url_for('result'))
                    
            # If form data for this step is already in the session, populate the form with it
            if 'step{}'.format(step) in self.session:
                form.process(data=self.session['step{}'.format(step)])
                
            content = {
                'progress': int(step / len(forms) * 100),
                'step': step, 
                'form': form
            }
            return render_template('step.html', **content)