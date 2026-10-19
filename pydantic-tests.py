from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    computed_field,
    field_validator,
    model_validator,
)


class ContactInfo(BaseModel):
    email:EmailStr
    location:str

    @field_validator('email')
    @classmethod
    def email_validate(cls,email):
        valid_domains =['hdfc.com','icici.com']
        domain_name = email.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError("not valid domain")
        return email

class Patient(BaseModel):
    name:str
    age:int = Field(gt=0,lt=140,strict=True)
    weight:float
    height:float
    married:bool
    allergies:Optional[list[str]] = None  # noqa: UP045
    contacts:ContactInfo
    @model_validator(mode='after')
    def emergency(self):
        if self.age>60 and 'emergency' not in self.contacts:
            raise ValueError("patients older than 60 must have emergency contacts")
        return self

    @computed_field
    @property
    def bmi(self) -> float:
        bmi =self.weight/(self.height)**2
        return bmi
        


def insert_patient_data(patient:Patient):
    return patient.name,patient.age

patient1_info = Patient(name="eren", age=17, weight=57.54,height=1.72, married=False, contacts={"email": "eren7654g@icici.com", "location": "shiganshina"})

print(patient1_info.name)
print(patient1_info.contacts.email)
print(patient1_info.height)
print(patient1_info.weight)
print(patient1_info.bmi)
