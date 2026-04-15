import json
from fastapi import FastAPI ,Path ,HTTPException

app = FastAPI()

def load_data():
    with open('1_MiniProject/patients.json' ,'r') as f:
       return json.load(f) 

@app.get('/')
def home():
    return 'Welcome to the website '

@app.get('/contact')
def contact():
    return 'contact us on example.com'

@app.get('/view')
def view():
    data = load_data()
    return data 


# dyncamicaly access the data
@app.get('/view/{patient_id}')
def patient(patient_id:str = Path(...,description='ID of the patient in the DB',example='POO1')):
    data = load_data()
    for patient in data:
        if patient["patient_id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="patient data don't exist")
            