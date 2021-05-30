from flask import Flask
app = Flask(__name__)
import os
import pickle
from flask import request

@app.route('/predict')
def predict():
    trained_model = retrieve_model("lgbr_cars.model")
    model_test_input = [eval(request.args.get('input'))]
    predict_value = make_prediction(trained_model, model_test_input)
    return {"predict_value":round(predict_value, 2)}

def retrieve_model(file):
    cur_dir_path = os.path.abspath(os.getcwd())
    absolute_file_name = os.path.join(cur_dir_path,file)
    with open(absolute_file_name, 'rb') as file:  
        trained_model = pickle.load(file)
    return trained_model

def make_prediction(trained_model, single_input):
    predicted_value = trained_model.predict(single_input)[0]
    return predicted_value