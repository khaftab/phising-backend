from flask import Flask, request, jsonify
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
import json
from flask_cors import CORS
from featureExtraction import featureExtraction 
from validURLCheck import is_url_live

# Load the trained model
with open('XGBoostClassifier.pickle.dat', 'rb') as f:
    model = pickle.load(f)

# with open('haka.dat', 'rb') as f:
#     model = pickle.load(f)

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def predict():
    try:
        # Get the input data from the request
        data = request.get_json()
        url = data.get('url')  # Access the 'url' key from the JSON data
        print(url, "Submitted URL") 
        # Check if the the is valid or not
        loading_time = is_url_live(url)
        print(loading_time, "Loading Time")
        if not loading_time:
            return jsonify({"error": "Invalid URL"}), 403
        output = featureExtraction(url)
        print(output)
        df = pd.DataFrame([output], columns=['Have_At', 'URL_Length', 'URL_Depth', 'Redirection', 'Http_In_Domain',
       'Tiny_URL', 'Prefix/Suffix', 'DNS', 'Domain_Age', 'Domain_End', 'Subdomains_Count', 'iFrame', 'Fake_Status_Bar', 'Right_Click', 'Forwarding'])
        
        # Make predictions
        predictions = model.predict(df)

        data_dict = df.iloc[0].to_dict()
        data_dict['Label'] = 1 if predictions[0] == 1 else 0
        data_dict['Loading_Time'] = loading_time
        # Converting dictionary to JSON
        json_data = json.dumps(data_dict)

        print(json_data)

        # Return the predictions as JSON
        return json_data
    except Exception as e:
        # Log the exception
        app.logger.error(f"Prediction error: {e}")
        # Return an error response
        return jsonify({"error": "An error occurred during prediction"}), 500


if __name__ == '__main__':
    app.run(debug=True)
