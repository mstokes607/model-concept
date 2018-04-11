# model-concept
A Flask 'model-concept' application created to experiment with web-based approaches to health economic modeling. 

Visit <a>https://model-concept.herokuapp.com/</a> to view the Flask site.

# synopsis
The code in this repository creates a simple Markov model using the Flask web framework. Markov models are used to represent stochastic processes and are frequently used in health economic evaluations, usually to model chronic diseases. In a Markov model, the disease under study is divided into distinct states with transition probabilities used to describe the likelihood of moving from one state to the next over a fixed period of time (usually 6-month or 1-year periods). Long term outcomes and costs associated with a disease can then be estimated by attaching unit costs and health effects to states in the model and running the model over a large number of cycles. 
# usage
First, create a virtual environment with the dependencies listed in 'requirements.txt' (highly recommended). Next, tell your terminal that you want to work with the 'run_views.py' file: <strong>export FLASK_APP=run_views</strong>.  Fire up your local Flask development server with the following command: <strong>flask run</strong>.
