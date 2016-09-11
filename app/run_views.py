from flask import Flask
app = Flask(__name__)
app.secret_key = 'longliveakita'

# HTML methods
from flask import request, render_template, redirect, url_for
    
# Forms
from flask_wtf import Form
from wtforms import DecimalField, StringField

# Module that runs the model calculations
import Markovcalcs
import re
    
# Binding URLs to functions

@app.route('/overview')
def overview():
    return render_template('overview.html', title = 'Overview')
    
@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

class MyForm(Form):
    pMIlte50_A = DecimalField('MI (age<=50)')
    pMIgt50_A = DecimalField('MI (age>50)')
    pDeathMI_A = DecimalField('Death after MI')
    pStroke_A = DecimalField('Stroke')
    pDthStrk_A = DecimalField('Death after Stroke')
    
    pMIlte50_B = DecimalField('MI (age<=50)')
    pMIgt50_B = DecimalField('MI (age>50)')
    pDeathMI_B = DecimalField('Death after MI')
    pStroke_B = DecimalField('Stroke')
    pDthStrk_B = DecimalField('Death after Stroke')
    
    MI_cost =  StringField('MI event')
    Stroke_cost = StringField('Stroke event')
    DrugA_cost = StringField('Drug A')
    DrugB_cost = StringField('Drug B')
    
    MI_util =  DecimalField('Utility MI')
    Stroke_util = DecimalField('Utility Stroke')
    Discount = DecimalField('Discount rate')
    
# Helper function to convert text data from form into float to feed into the model
def convert_form_data(method):        
    # Initialize list and dict variables to access different data on form
    # Probabilities and utility values
    putilval = ['pMIlte50_A', 'pMIgt50_A', 'pDeathMI_A', 'pStroke_A', 'pDthStrk_A',
                'pMIlte50_B', 'pMIgt50_B', 'pDeathMI_B', 'pStroke_B', 'pDthStrk_B',
                'MI_util', 'Stroke_util', 'Discount']
                       
    cvars = ['MI_cost', 'Stroke_cost', 'DrugA_cost', 'DrugB_cost']
                       
    prob_util_vars = dict()
    cost_vars = dict()
        
    if method == 'POST':
            
        #Create dictionaries to convert text data from form into numerical data
        for element in putilval:
            prob_util_vars[element] = float(request.form[element])
                
        for element in cvars:
            cost_vars[element] = float( request.form[element].replace(',','') )

        return prob_util_vars, cost_vars
        
    else:
        for element in putilval:
            prob_util_vars[element] = float(form[element].data)
            
        for element in cvars:
            cost_vars[element] = float(form[element].data)
            
        return prob_util_vars, cost_vars
            
# Helper function to restore default values       
def default_var_dicts():
    prob_util_vars = {'pMIlte50_A': 0.20,
                      'pMIgt50_A' : 0.26,
                      'pDeathMI_A': 0.40,
                      'pStroke_A' : 0.15,
                      'pDthStrk_A': 0.30,
                      'pMIlte50_B': 0.30,
                      'pMIgt50_B' : 0.30,
                      'pDeathMI_B': 0.40,
                      'pStroke_B' : 0.18,
                      'pDthStrk_B': 0.30,
                      'MI_util' : 0.7,
                      'Stroke_util' : 0.5,
                      'Discount' : 0.03}
                          
    cost_vars = {'MI_cost' : 1000,
                 'Stroke_cost' : 4500,
                 'DrugA_cost' : 6,
                 'DrugB_cost' : 3}
    return prob_util_vars, cost_vars
    
@app.route('/', methods=('GET', 'POST'))
def submit():
    global form
    
    form = MyForm(pMIlte50_A = 0.20, pMIgt50_A = 0.26, pDeathMI_A = 0.40, pStroke_A = 0.15, pDthStrk_A = 0.30,
                  pMIlte50_B = 0.30, pMIgt50_B = 0.30, pDeathMI_B = 0.40, pStroke_B = 0.18, pDthStrk_B = 0.30,
                  MI_cost = 1000, Stroke_cost = 4500, DrugA_cost = 6, DrugB_cost = 3, MI_util = 0.7,
                  Stroke_util = 0.5, Discount = 0.03)
                                      
    if request.method == 'POST':
    
        # Initialize error switch to 0 - no errors
        error = 0
        txt = 0
    
        try:
        
            # Control for entering invalid data with commas (xx,xx) and text
            # if user enters numbers with commas, check to see if they are followed by 3 digits, if not = error
            for anyvalue in request.form:
                if ',' in request.form[anyvalue]:
                    if not re.search(r'^\d{1,3}([,]\d{3})*$',request.form[anyvalue],flags=0):
                        error = 1        
                        print 'error', error, request.form[anyvalue]
                
            # Convert text data from form into numerical data to feed into the model
            prob_util_vars, cost_vars = convert_form_data(request.method)
                         
        #If user enters text and kicks a value error...
        except ValueError: 
            print 'value error' 
            error = 1
            
            # Create input vars to send to model for default run
            prob_util_vars, cost_vars = default_var_dicts()
            
            # Run model to create vars for the html table          
            costA, costB, costDiff, qalyA, qalyB, qalyDiff, ceratio = Markovcalcs.execute_calcs(prob_util_vars, 
                                                                                            cost_vars)                                                                                       
            bar = Markovcalcs.chart()
        
            return render_template('hello_rev.html', title = 'Model Concept', form=form, costA=costA, costB=costB, 
                                   costDiff=costDiff, qalyA=qalyA, qalyB=qalyB, qalyDiff=qalyDiff, 
                                   ceratio=ceratio, bar=bar)
            
        # Validate event probs and utilities
        for item , value in prob_util_vars.iteritems():
            if value > 1 :
                print '> 1'
                error = 1
            # Check for value greater 0
            elif value <= 0 :
                print 'Error: < 0'
                error = 1
        
        if not error :
            # Validate cost vars
            for item, value in cost_vars.iteritems():
                # Check for value greater than or equal to 0
                if value < 0:
                    print '< 0'
                    error = 1            
            
        # Run model if no errors...
        if not error :

            # Run model to create vars for the html table          
            costA, costB, costDiff, qalyA, qalyB, qalyDiff, ceratio = Markovcalcs.execute_calcs(prob_util_vars, 
                                                                                            cost_vars) 

            bar = Markovcalcs.chart()
             
            return render_template('hello_rev.html', title = 'Model Concept', form=form, costA=costA, costB=costB, 
                                   costDiff=costDiff, qalyA=qalyA, qalyB=qalyB, qalyDiff=qalyDiff, 
                                   ceratio=ceratio, bar=bar)
                                   
    # Create input vars to send to model for default runs
    prob_util_vars, cost_vars = default_var_dicts()
            
    # Run model to create vars for the html table          
    costA, costB, costDiff, qalyA, qalyB, qalyDiff, ceratio = Markovcalcs.execute_calcs(prob_util_vars, 
                                                                                            cost_vars)
                                                                                            
    bar = Markovcalcs.chart()
        
    return render_template('hello_rev.html', title = 'Model Concept', form=form, costA=costA, costB=costB, 
                                   costDiff=costDiff, qalyA=qalyA, qalyB=qalyB, qalyDiff=qalyDiff, 
                                   ceratio=ceratio, bar=bar)        
