# Markov model
import numpy as np
import pandas as pd

import pygal
from pygal.style import Style

# Function takes data inputs and returns transition probabilities
def calc_trans(pMIlte50, pMIgt50, pDeathMI, pStroke, pDthStrk):
    OtherDthLte50 = 0.10
    OtherDthGt50 = 0.16
    #Transition probabilities for <=50
    P_AliveLte50 = (1-OtherDthLte50) * (1-(pMIlte50 + pStroke))
    
    #Fix division by 0 if pMI = 0 and pStroke = 0 for MI < 50 yrs transition probs
    if (pMIlte50 + pStroke) > 0:
        percentMIlte50 = pMIlte50 / (pMIlte50+pStroke)
        percentStrokelte50 = pStroke / (pMIlte50+pStroke)
    else: 
        percentMIlte50 = 0
        percentStrokelte50 = 0
    
    P_MILte50 = ((1-OtherDthLte50) * (pMIlte50 + pStroke) * 
                percentMIlte50 * (1-pDeathMI))
    P_StrokeLte50 = ((1-OtherDthLte50) * (pMIlte50 + pStroke) * 
                percentStrokelte50 * (1-pDthStrk))
    P_OthDthLte50 = OtherDthLte50
    P_FatalMILte50 = ((1-OtherDthLte50) * (pMIlte50 + pStroke) * 
                percentMIlte50 * (pDeathMI))
    P_FatalStrkLte50 = ((1-OtherDthLte50) * (pMIlte50 + pStroke) * 
                percentStrokelte50 * (pDthStrk))
    #Transition probabilities for >50
    
    #Fix division by 0 if pMI = 0 and pStroke = 0 for MI > 50 transition probs
    if (pMIgt50 + pStroke) > 0:
        percentMIgt50 = pMIgt50 / (pMIgt50+pStroke)
        percentStrokegt50 = pStroke / (pMIgt50+pStroke)
    else: 
        percentMIgt50 = 0
        percentStrokegt50 = 0
        
    P_AliveGt50 = (1-OtherDthGt50) * (1-(pMIgt50 + pStroke))
    P_MIGt50 = ((1-OtherDthGt50) * (pMIgt50 + pStroke) * 
                percentMIgt50 * (1-pDeathMI))
    P_StrokeGt50 = ((1-OtherDthGt50) * (pMIgt50 + pStroke) * 
                percentStrokegt50 * (1-pDthStrk))
    P_OthDthGt50 = OtherDthGt50
    P_FatalMIGt50 = ((1-OtherDthGt50) * (pMIgt50 + pStroke) * 
                percentMIgt50 * (pDeathMI))
    P_FatalStrkGt50 = ((1-OtherDthGt50) * (pMIgt50 + pStroke) * 
                percentStrokegt50 * (pDthStrk))
    #Put transitions into lists
    P_transLte50 = [P_AliveLte50, P_MILte50, P_StrokeLte50, OtherDthLte50, P_FatalMILte50,
                    P_FatalStrkLte50]
    P_transGte50 = [P_AliveGt50, P_MIGt50, P_StrokeGt50, P_OthDthGt50, P_FatalMIGt50,
                    P_FatalStrkGt50] 
    return P_transLte50, P_transGte50
    
# Computes the model calculations and returns dataframe of results
def markov_structure(num_cycles, startage, l_p_le50, l_p_gt50, costdrug, cstroke, cMI, uMI, 
                     ustroke, rdisc):
    #Create cycle vars 
    cycle = np.arange(num_cycles + 1)
    markov = pd.DataFrame(data=cycle)
    markov.columns=['cycle']
    markov['age'] = cycle + startage
    #All patients begin in the alive state
    markov['alive'] = np.where(cycle==0,1.0,0.0)
    markov['mi'] = 0.0
    markov['stroke'] = 0.0
    
    #Estimate numbers of patients in each state during each cycle
    cond = cycle != 0
    cond1 = markov['age'] <= 50 
    cond2 = markov['age'] > 50
    
    for index, row in markov.iterrows():

        markov['alive']  =  np.where(cond & cond1, l_p_le50[0] * (markov['alive'].shift(1) + 
                           markov['mi'].shift(1) + markov['stroke'].shift(1)), 
                              np.where(cond & cond2, l_p_gt50[0] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)),1.0))
                             
        markov['mi'] =  np.where(cond & cond1, l_p_le50[1] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)), 
                              np.where(cond & cond2, l_p_gt50[1] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)),0.0)) 
                             
        markov['stroke']  =  np.where(cond & cond1, l_p_le50[2] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)), 
                              np.where(cond & cond2, l_p_gt50[2] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)),0.0)) 
                              
        markov['other_dth'] =  np.where(cond & cond1, l_p_le50[3] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)), 
                              np.where(cond & cond2, l_p_gt50[3] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)),0.0))
                              
        markov['fatal_mi'] =   np.where(cond & cond1, l_p_le50[4] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)), 
                              np.where(cond & cond2, l_p_gt50[4] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)),0.0)) 
                              
        markov['fatal_stroke'] =  np.where(cond & cond1, l_p_le50[5] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)), 
                              np.where(cond & cond2, l_p_gt50[5] * (markov['alive'].shift(1) + 
                              markov['mi'].shift(1) + markov['stroke'].shift(1)),0.0)) 
    
    #Convert drug cost per day to cost per year
    costdrug = costdrug * 360            
                              
    total_death = (markov['other_dth'] + markov['fatal_mi'] + markov['fatal_stroke'])
    
    markov['cost'] = (markov['alive'] * costdrug + (markov['mi'] * (costdrug + cMI)) + 
                      (markov['stroke'] * (costdrug + cstroke)) + (markov['fatal_mi'] * cMI) + 
                      (markov['fatal_stroke'] * cstroke))
                      
    markov['utility'] = markov['alive'] + markov['mi'] * uMI + markov['stroke'] * ustroke
    
    markov['cost_disc'] = markov['cost'].rolling(window=2,center=False).mean()/(1+rdisc)**markov['cycle']
    
    # markov['cost_disc'] = pd.rolling_mean(markov['cost'],2)/(1+rdisc)**markov['cycle']
    
    markov['util_disc'] = markov['utility'].rolling(window=2,center=False).mean()/(1+rdisc)**markov['cycle'] 
    
    # markov['util_disc'] = pd.rolling_mean(markov['utility'],2)/(1+rdisc)**markov['cycle'] 
                      
    markov['total_death'] = total_death.cumsum()
    
    #Detailed cost variables for the graph
    c_drug = (markov['alive'] * costdrug + markov['mi'] * costdrug + markov['stroke'] * costdrug)
    c_MI = (markov['mi'] * cMI + markov['fatal_mi'] * cMI)
    c_stroke = (markov['stroke'] * cstroke + markov['fatal_stroke'] * cstroke)
    
    markov['c_drug_d'] = c_drug.rolling(window=2,center=False).mean()/(1+rdisc)**markov['cycle']  
    markov['c_MI_d'] = c_MI.rolling(window=2,center=False).mean()/(1+rdisc)**markov['cycle'] 
    markov['c_stroke_d'] = c_stroke.rolling(window=2,center=False).mean()/(1+rdisc)**markov['cycle'] 
    
#     markov['c_drug_d'] = pd.rolling_mean(c_drug,2)/(1+rdisc)**markov['cycle']  
#     markov['c_MI_d'] = pd.rolling_mean(c_MI,2)/(1+rdisc)**markov['cycle'] 
#     markov['c_stroke_d'] = pd.rolling_mean(c_stroke,2)/(1+rdisc)**markov['cycle']                
                              
    return markov.round({'alive': 3, 'mi': 3, 'stroke':3, 'other_dth':3, 'fatal_mi':3, 'fatal_stroke':3,
                        'markov_cost' : 1, 'utility': 2, 'cost_disc':1, 'util_disc':4, 'total_death': 2,
                        'c_drug_d' : 1, 'c_MI_d' : 1, 'c_stroke_d' : 1})  
        
'''Engine of the model - receives user input data from form, feeds them into the calc_trans function so that 
   transition probs may be calculated; finally the Markov structure function gets called to create the model and
   returns a dataframe on which analyses may be run 
'''
def execute_calcs(inputs, cost_vars):
    global A_calcs, B_calcs
        
    #Extract vars from dictionary of inputs
    pMIlte50_A = inputs['pMIlte50_A']
    pMIgt50_A = inputs['pMIgt50_A']
    pDeathMI_A = inputs['pDeathMI_A']
    pStroke_A = inputs['pStroke_A']
    pDthStrk_A = inputs['pDthStrk_A']
    
    costdrugA = cost_vars['DrugA_cost']
           
    pMIlte50_B = inputs['pMIlte50_B']
    pMIgt50_B = inputs['pMIgt50_B']
    pDeathMI_B = inputs['pDeathMI_B']
    pStroke_B = inputs['pStroke_B']
    pDthStrk_B = inputs['pDthStrk_B']
    
    costdrugB = cost_vars['DrugB_cost']
    
    cstroke = cost_vars['Stroke_cost']
    cMI = cost_vars['MI_cost']
    uMI = inputs['MI_util']
    ustroke = inputs['Stroke_util']
    rdisc = inputs['Discount']
    
    #Nonuser defined inputs
    startage = 40
    num_cycles = 30
        
    #Create transition probs for Treatment A
    P_transLte50_A, P_transGte50_A = calc_trans(pMIlte50_A, pMIgt50_A, 
                                                               pDeathMI_A, pStroke_A, pDthStrk_A)
    #Create transition probs for Treatment B
    P_transLte50_B, P_transGte50_B = calc_trans(pMIlte50_B, pMIgt50_B, 
                                                               pDeathMI_B, pStroke_B, pDthStrk_B)
                                                               
    A_calcs = markov_structure(num_cycles, startage, P_transLte50_A, P_transGte50_A, costdrugA, 
                               cstroke, cMI, uMI, ustroke, rdisc) 
    B_calcs = markov_structure(num_cycles, startage, P_transLte50_B, P_transGte50_B, costdrugB, 
                               cstroke, cMI, uMI, ustroke, rdisc) 
    
    c_totalA = A_calcs['cost_disc'].sum()
    qaly_A = A_calcs['util_disc'].sum()
    
    c_totalB = B_calcs['cost_disc'].sum()
    qaly_B = B_calcs['util_disc'].sum()
    
#     print 'Treatment A'
#     print A_calcs.head(10)
    
#   print 'Treatment B'
#   print B_calcs.head(10)
     
    #Calculate & format vars to feed into the html table
    c_diff = c_totalA - c_totalB
    qaly_diff = qaly_A - qaly_B
    ceratio = c_diff / qaly_diff

    c_totalA = '${:,.0f}'.format(c_totalA)
    c_totalB = '${:,.0f}'.format(c_totalB)
    c_diff = '${:,.0f}'.format(c_diff)
    ceratio = '${:,.0f}'.format(ceratio)
    qaly_A = '{0:.2f}'.format(qaly_A)
    qaly_B = '{0:.2f}'.format(qaly_B)
    qaly_diff = '{0:.2f}'.format(qaly_diff)
    
#   print A_series, type(A_series)
     
    return c_totalA, c_totalB, c_diff, qaly_A, qaly_B, qaly_diff, ceratio

custom_style = Style(
  background='transparent',
  plot_background='transparent',
  foreground='#555',
  foreground_strong='#20B2AA',
  foreground_subtle='#630C0D',
  opacity='.8',
  opacity_hover='.6',
  tooltip_font_size = '11',
  major_label_font_size = '12',
  font_family = 'Arial',
  transition='400ms ease-in',
  colors=('#20B2AA', '#808080', '#F0E68C'))  
  
#53E89B 
    
#Line chart
def chart():
    bar_chart = pygal.StackedBar(height=300, width=345, explicit_size=True, title=u'Costs by category (in $)',
                            disable_xml_declaration=True, legend_at_bottom=True, legend_at_bottom_columns=3, 
                            style=custom_style)
    bar_chart.x_labels = ['A', 'B']
    
    drugA = A_calcs['c_drug_d'].sum()
    MI_A = A_calcs['c_MI_d'].sum()
    strokeA = A_calcs['c_stroke_d'].sum()
    
    drugB = B_calcs['c_drug_d'].sum()
    MI_B = B_calcs['c_MI_d'].sum()
    strokeB = B_calcs['c_stroke_d'].sum()
    
    bar_chart.add('Drug', [drugA, drugB])
    bar_chart.add('MI',  [MI_A, MI_B])
    bar_chart.add('Stroke', [strokeA, strokeB])
    bar_chart.render_to_file('bar_chart.svg') 
       
    return bar_chart


