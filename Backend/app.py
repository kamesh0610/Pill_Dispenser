from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb+srv://kameshoffical06:kamesh1906@doctor.k2n8v.mongodb.net/?retryWrites=true&w=majority&appName=Doctor", server_api=ServerApi('1'))
try:
    client._connect()
except Exception as e:
    print("Error",e)
db = client["pillDispenser"]
collection = db["prescriptions"]

@app.route('/get-prescription', methods=['POST'])
def get_prescription():
    data = request.get_json()
    patient_id = data.get('patientId')
    
    if not patient_id:
        return jsonify({"error": "Patient ID is required"}), 400

    # Assuming "patientId" is stored as a string in the DB
    prescription = collection.find_one(filter={"codeId": patient_id}, projection={"_id": 0})  # exclude _id
    if prescription and "medicines" in prescription:
        for med in prescription["medicines"]:
            med.pop("_id", None)  # safely remove _id if it exists
    if not prescription:
        return jsonify({"error": "No prescription found for this patient ID"}), 404

    return prescription

if __name__ == '__main__':
    app.run(debug=True)
