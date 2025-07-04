from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",examples=['P001'])]
    name:Annotated[str,Field(...,description="Name of the patient")]
    city:Annotated[str,Field(...,description="City where the patient isd living")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(gt=0,description="Height of the patient in meters")]
    weight:Annotated[float,Field(gt=0,description="Weight of the patient in Kilograms")]
    
    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height)**2,2)
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Overweight'
        else:
            return 'obese'

class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None)]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None)]
    weight:Annotated[Optional[float],Field(default=None)]
    
def load_data():
    with open("patients.json","r") as f:
        data=json.load(f)
        
    return data

def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data,f)

@app.get("/")
def home():
    return {"message":"Patient Management System API."}

@app.get("/about")
def about():
    return {"message":"A fully functional API to manage patient records."}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id=Path(...,description="ID of the patient in database",example="P001")):
    data=load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description="Sort on the basis of height, weight or bmi"),
                  order:str=Query('asc',description="Sort in ascending or descending order")):
    
    if sort_by not in ['height','weight','bmi']:
        raise HTTPException(status_code=400,detail="Invalid field, select from ['height','weight','bmi'].")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid field, select form ['asc],'desc].")
    
    data=load_data()
    
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=(order=='desc'))
    
    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists.")
    else:
        patient
        data[patient.id]=patient.model_dump(exclude=['id'])
        save_data(data)
        
    return JSONResponse(status_code=201,content={"message":"Patient created sucessfully."})

@app.put("/edit/{patient_id}")
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    
    patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info.items():
        patient_info[key]=value
    
    patient_info['id']=patient_id
    patient_pydantic_object=Patient(**patient_info)
    
    patient_info=patient_pydantic_object.model_dump(exclude='id')
    
    data[patient_id]=patient_info
    save_data(data)
    
    return JSONResponse(status_code=200,content="Patient updated.")

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found.")
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200,content="Patient deleted")