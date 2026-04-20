import json
from fastapi import FastAPI ,Path ,HTTPException, Query

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
    raise HTTPException(status_code=400, detail="patient data don't exist")
            
# using Query parameter 

@app.get('/sort')
def sort_patient(sort_by: str = Query(...,description='sort on the basis of age , gender or blood group'),order: str = Query('asc',description='sort in acs or desc order')):

    valid_fields = ['age','gender','blood_group']

    if sort_by.lower() not in valid_fields:
        raise HTTPException(status_code=400
                           ,detail=f'invalid input:plz select only from {valid_fields}'
                           )
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,
                            detail='Invalid order: select only from asc and desc ')
    
    data = load_data()
    # for patient in data:
    sort_order = True if order == 'desc' else False
    def get_value(patient):
             if sort_by == 'age':
                return patient['personal_info'].get('age', 0)
             elif sort_by == 'gender':
                return patient['personal_info'].get('gender', '')
             elif sort_by == 'blood_group':
                return patient['medical_info'].get('blood_group', '')
    sorted_data = sorted(data, key=get_value, reverse=sort_order)

    return sorted_data
    