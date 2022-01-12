# Pickle object reading 
import pickle 

# JSON object reading 
import json 

# OS traversal 
import os 

# Input dataframe
import pandas as pd 

# Array math 
import numpy as np 

def load_ml_model(model_dir='ml_model'):
    """
    Loads the model and the schema from the given path
    """
    model, type_dict, feature_list = {}, {}, []
    
    _model_path = os.path.join(model_dir, 'model.pkl')
    _input_schema_path = os.path.join(model_dir, 'input_schema.json')

    # Checking if the files exists and reading them 
    if os.path.exists(_model_path) and os.path.exists(_input_schema_path):
        with open(_model_path, 'rb') as f:
            model = pickle.load(f)
        with open(_input_schema_path, 'r') as f:
            input_schema = json.load(f)
    
    # Extracting the features
    features = input_schema.get('input_schema', {})
    features = features.get('columns', [])

    # Iterating over the list of dictionaries and changing the types.
    # numeric -> float 
    # boolean -> bool
    # The resulting dictionary will have a key value of the feature name and the value will be the type
    for feature in features:
        if feature.get('type') == 'numeric':
            feature['type'] = float
        elif feature.get('type') == 'boolean':
            feature['type'] = bool
        type_dict.update({feature.get('name'): feature.get('type')})
    
    # Extracting the correct ordering of the features for the ML input 
    feature_list = [x.get('name') for x in features]

    # Returning the model, type dictionary and the feature order
    return model, type_dict, feature_list

def predict(model, feature_dict: dict, X: pd.DataFrame) -> list:
    """
    Function that converts the feature_dict into a predictable format for the ml model

    Args:
        model: the machine learning model
        feature_dict: the dictionary of features
        X: the features used in prediction

    Returns:
        A list of predictions
    """
    # Converting the dictionary into a list of lists
    feature_list = list(feature_dict.values())

    # Ensuring that no columns are missing 
    if len(feature_list) != X.shape[1]:
        for col in X.columns:
            if col not in feature_list:
                X[col] = np.nan

    # Converting the X columns to correct types 
    for col in X.columns:
        if col in feature_list:
            try:
                X[col] = X[col].astype(feature_dict.get(col))
            except: 
                print(f"Cannot convert {col} to {feature_dict.get(col)}")
                # If we cannot convert it, we will set it to null. 
                X[col] = np.nan

    # Predicting the output
    prediction = model.predict(X[feature_list])

    return prediction