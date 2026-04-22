from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel ,Field,computed_field
from typing import Optional,Literal ,Annotated
import json

# load data
def load_data():
    with open('3_put/patients.json','r') as f:
        return json.load(f)
    
def save_data(new_data):
    with open('3_put/patients.json','w') as d:
         json.dump(new_data,d)

class Patient(BaseModel):
    name:str
    patient_id:Annotated[str ,Field(...,description='Enter the patient id',examples=['P001'])]
    age:Annotated[int,Field(...,lt=100,gt=0)]
    weight:Annotated[float,Field(...,gt=0.5,description='Weight only in kg')]
    height:Annotated[float,Field(...,gt=1,description='Height only in Metter')]
    gender:Literal['male','female']
    # phone:Annotated[int,Field(...,description = 'enter your contact Number ')]
    # email:Annotated[EmailStr,Field(...,description='enter your email here',examples=['abc@example.com'])]
    # blood_group:Literal['O+','O-','A+','B+','AB+','A-','AB-']
    city:Annotated[str,Field(description='your hometown')]

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

class Update_Patient(BaseModel):
    name:Optional[str] = Field(
                    default=None,
                    description='Enter the new/change name')
    city:Optional[str] = Field(
                    default=None,
                    description='Enter new city where you are living'
    )
    age:Optional[int] = Field(
                    default=None,
                    gt=0,lt=100,
                    description='updtae your age')
    gender:Optional[Literal['male','female']] = None
    height:Optional[float] = Field(
                        default=None,
                        gt=1,lt=8,
                        description='Update your height in meters'
                        )
    weight:Optional[float] = Field(
                        default=None,
                        gt=1,
                        description='Update your weights in kg'
    )
    # phone:Optional[int] = Field(
    #                     default=None,
    #                     # gt=1,lt=11,
    #                     description='Update your number'
    # )

app = FastAPI()

@app.put('/update/{patient_id}')
def update(patient_id:str,newPydantic_Patient:Update_Patient):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=401,detail='User not exist')
    # extract the patient which info will be update
    existing_patient_info = data[patient_id]

    # take pydantic obejct and convert into python object with exclude_unset true so it not take other field that was not updating 
    updated_patient_info = newPydantic_Patient.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    data[patient_id] = existing_patient_info

    # existing_patient_info -> pydantic object -> updated bmi + verdict

    existing_patient_info['patient_id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)
        
    # pydantic  object -> dict 
    existing_patient_info = patient_pydantic_object.model_dump(exclude='patient_id')

    #add this dict into data
    data[patient_id] = existing_patient_info

    save_data(data)


    return JSONResponse(status_code=200,content={'message':'updares succesfully'})
    