from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,EmailStr,Field,computed_field
from typing import Literal ,List ,Annotated,Optional
import json


app = FastAPI()

def load_data():
    with open('2_post/patients.json' ,'r') as f:
       return json.load(f) 
    
def save_data(new_data):
    data = load_data()
    data.append(new_data)
    with open('2_post/patients.json','w') as d:
         json.dump(data,d,indent=4)

class Patient(BaseModel):
    name:str
    patient_id:Annotated[str ,Field(...,description='Enter the patient id',examples=['P001'])]
    age:Annotated[int,Field(...,lt=100,gt=0)]
    weight:Annotated[float,Field(...,gt=0.5,description='Weight only in kg')]
    height:Annotated[float,Field(...,gt=1,description='Height only in Metter')]
    gender:Literal['male','female']
    dob:Annotated[str,Field(...,description='enter your Date of birth')]
    phone:Annotated[int,Field(...,description = 'enter your contact Number ')]
    email:Annotated[EmailStr,Field(...,description='enter your email here',examples=['abc@example.com'])]
    address:Optional[str] = Field(
        default=None,
        description='enter you current address'
    )
    blood_group:Literal['O+','O-','A+','B+','AB+','A-','AB-']
    allergies:List[str]
    chronic_conditions:List[str]

    @computed_field
    @property
    def bmi(self) -> float:
         bmi = round(self.weight / (self.height **2),2)
         return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 20:
            return 'under weight'
        elif 20 < self.bmi < 30:
            return 'normal'
        else:
            return 'obesed'
         
@app.post('/create')
def newPatient(patient:Patient):

    # load existing data

    data = load_data()
    # check if the patient already exist 
    for p in data:
        if p['patient_id'] == patient.patient_id:
            raise HTTPException(status_code=400,detail='patient already exist')
    # new patient add to database
    new_patient = patient.model_dump() # pydantic obeject into python dcict for purpose to store in database

    # save into json file
    save_data(new_patient)
    return JSONResponse(status_code=201,
                        content={f'{new_patient}':'Patient created successfully'})

