from flask import Flask, request, jsonify
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load the trained model
with open('DecisionTreeClassifier.pickle.dat', 'rb') as f:
    model = pickle.load(f)

# with open('haka.dat', 'rb') as f:
#     model = pickle.load(f)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data from the request
        input_data = request.json
        df = pd.DataFrame(input_data, columns=['Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
       'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic',
       'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over', 'Right_Click',
       'Web_Forwards'])

        # Make predictions
        predictions = model.predict(df)

        # Return the predictions as JSON
        return jsonify(predictions.tolist())
    except Exception as e:
        # Log the exception
        app.logger.error(f"Prediction error: {e}")
        # Return an error response
        return jsonify({"error": "An error occurred during prediction"}), 500


if __name__ == '__main__':
    app.run(debug=True)
