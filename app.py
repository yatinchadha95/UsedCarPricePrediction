
from flask import Flask, render_template, request
#import jsonify
#import requests
import pickle
#import numpy as np

# Flask constructor takes the name of current module (__name__) as argument.
app = Flask(__name__) 
# reading the pickle file
model = pickle.load(open('random_forest_regression_model.pkl','rb'));

@app.route("/", methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict",methods=['POST'] )
def predict():
    
    if request.method == 'POST':
        year = int(request.form['Year'])
        presentPrice = float(request.form['Present_Price'])
        kmsDriven = int(request.form['Kms_Driven'])
        owner = int(request.form['Owner'])
        fuelTypePetrol = request.form['Fuel_Type_Petrol']
        
        if (fuelTypePetrol == 'Petrol'):
            fuelTypePetrol = 1
            fuelTypeDiesel = 0
        
        else:
            fuelTypePetrol = 0
            fuelTypeDiesel = 1
        
        year = 2020 - year
        sellerTypeIndividual = request.form['Seller_Type_Individual']
        if (sellerTypeIndividual == 'Individual'):
            sellerTypeIndividual = 1
        else:
            sellerTypeIndividual = 0
                
        transmissionManual=request.form['Transmission_Manual']
        if(transmissionManual=='Manual'):
            transmissionManual=1
        else:
            transmissionManual=0
        
        prediction = model.predict([[presentPrice, kmsDriven, owner, fuelTypeDiesel, fuelTypePetrol, sellerTypeIndividual, transmissionManual]])
        output = round(prediction[0],2)
        
        if output < 0:
            return render_template('index.html',predictionTexts = 'Sorry you cannot sell this car.')
        
        else:
            return render_template('index.html', predictionTexts = ('Approx. Selling Price of the car is : '+ str(output)))
        
    else:
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug= True)