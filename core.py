class Patient: 
    def __init__(self):
        self.patient_ID = None
        self.name = None
        self.age = None
        self.gender = None
        self.medical_history = []
        
    def new_patient (self, patient_ID, name, age, gender, medical_history):
        self.patient_ID = patient_ID
        self.name = name
        self.age = age
        self.gender = gender
        self.medical_history.append(medical_history)
        
    def patient_info_summary(self):
        return f"""Patient: {self.name}
                \nPatient ID : {self.patient_ID}
                \nAge: {self.age}
                \nGender: {self.gender}
                \nMedical History : {self.medical_history}"""