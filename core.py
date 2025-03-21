class Patient: 
    def __init__(self, patient_ID, name, age, gender, medical_history):
        self.patient_ID = patient_ID
        self.name = name
        self.age = age
        self.gender = gender
        self.medical_history = medical_history
        self.studies = [] #to store multiple studies of the patient
        
    def add_study (self, study):
        self.studies.append(study)
        
    def patient_info_summary(self):
        return f"Patient: {self.name}\nPatient ID : {self.patient_ID}\nAge: {self.age}\nGender: {self.gender}\nMedical History : {self.medical_history}\nNumber of studies: {len(self.studies)} "
    


class Study:
    def __init__(self, study_id, modality,patient):
        self.study_id = study_id
        self.patient = patient #link study to a particular patient
        self.modality = modality #not settled yet
        #images or the path to them

        
        patient.add_study(self) #add the study to the patient's record immediately it is created
        
        
    def get_study_details(self):    #Returns a  summary of the study details.
        return (f"Study ID: {self.study_id}\n"
                f"Patient: {self.patient.name} (ID: {self.patient.patient_ID})\n"
                f"Modality: {self.modality}")
                #number of images in the study 
                
# # Unit test
# patient_1 = Patient("BME221", "Gideon", 24, "Male", ["Brain Cancer", "Ischemic Stroke"])
# study_1 = Study("STUDY001", "MRI", patient_1)
# study_2 = Study("STUDY002", "MRI", patient_1)

# print(patient_1.patient_info_summary())
# print(study_2.get_study_details())
        

class Report: #generates reports for a specific study
    def __init__(self, study, findings, diagnosis):
        self.study = study #Link to a particular study
        self.findings = findings
        self.diagnosis = diagnosis #together with findings will be needed from the VLM
        self.recommendations = "" # Added recommendations attribute
    
    def generate_report_summary(self):
        return (f"--- Report for Study {self.study.study_id} ---\n"
                f"Patient: {self.study.patient.name} (ID: {self.study.patient.patient_ID})\n"
                f"Modality: {self.study.modality}\n"
                f"Findings: {self.findings}\n"
                f"Diagnosis: {self.diagnosis}\n"
                f"Recommendations: {self.recommendations}\n")
