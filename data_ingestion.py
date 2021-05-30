import pandas as pd
from urllib.request import urlopen
import json
import unittest
import os
import pickle

def flatten_json(nested_json, exclude=['']):
    """Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
            exclude: Keys to exclude from output.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude: flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


def jsonresponse(url):
    response = urlopen(url)
    json_data = response.read().decode('utf-8', 'replace')
    data = json.loads(json_data)
    return data


def get_clp_places(url):
    data = jsonresponse(url)
    data = pd.DataFrame([flatten_json(x) for x in data])
    data[data['address_cityName'].str.lower().str.contains('antwerpen') == True]['antwerpen'] = 1
    data[data['address_cityName'].str.lower().str.contains('antwerpen') == False]['antwerpen'] = 0
    return data

df_clp = get_clp_places("https://ecgplacesmw.colruytgroup.com/ecgplacesmw/v3/nl/places/filter/clp-places")

# test cases
tc = unittest.TestCase('__init__')
tc.assertTrue(len(df_clp) > 200, "Data should be more than 200 records")
tc.assertEquals(len(df_clp.loc[
    (df_clp['geoCoordinates_latitude'] > 49) &
    (df_clp['geoCoordinates_latitude'] < 52)]),
    len(df_clp),"latitude should be between 49 and 52")
tc.assertEquals(len(df_clp.loc[
    (df_clp['geoCoordinates_longitude'] > 2) 
    & (df_clp['geoCoordinates_longitude'] < 7)]),
    len(df_clp),"longitude should be between 2 and 7")


def retrieve_model(file):
    cur_dir_path = os.path.abspath(os.getcwd())
    absolute_file_name = os.path.join(cur_dir_path,file)
    with open(absolute_file_name, 'rb') as file:  
        trained_model = pickle.load(file)
    return trained_model

lgbr_cars = retrieve_model("lgbr_cars.model")
tc.assertEqual(str(type(lgbr_cars)),"<class 'lightgbm.sklearn.LGBMRegressor'>", type(lgbr_cars))

model_test_input = [[3,1,190,-1,125000,5,3,1]]

def make_prediction(trained_model, single_input):
    predicted_value = trained_model.predict(single_input)[0]
    return predicted_value

predicted_value = make_prediction(lgbr_cars, model_test_input)
tc.assertAlmostEqual(predicted_value, 14026.35, places=2)