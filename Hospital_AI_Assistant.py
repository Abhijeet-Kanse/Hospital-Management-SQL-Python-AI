import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime
import math
from collections import defaultdict

# Set page configuration
st.set_page_config(
    page_title="Hospital Management AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .stats-box {
        background-color: #e6f7ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stButton button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Create DataFrames from all the provided data
def create_dataframes():
    # Patients data (all 50 patients)
    patients_data = {
        'patient_id': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010',
                      'P011', 'P012', 'P013', 'P014', 'P015', 'P016', 'P017', 'P018', 'P019', 'P020',
                      'P021', 'P022', 'P023', 'P024', 'P025', 'P026', 'P027', 'P028', 'P029', 'P030',
                      'P031', 'P032', 'P033', 'P034', 'P035', 'P036', 'P037', 'P038', 'P039', 'P040',
                      'P041', 'P042', 'P043', 'P044', 'P045', 'P046', 'P047', 'P048', 'P049', 'P050'],
        'first_name': ['David', 'Emily', 'Laura', 'Michael', 'David', 'Linda', 'Alex', 'David', 'Laura', 'Michael',
                      'Emily', 'Laura', 'Laura', 'Alex', 'Sarah', 'Michael', 'Jane', 'Laura', 'Sarah', 'Jane',
                      'Michael', 'John', 'Linda', 'Sarah', 'Robert', 'John', 'Linda', 'Alex', 'David', 'Emily',
                      'Robert', 'Alex', 'Michael', 'Alex', 'David', 'Michael', 'Robert', 'David', 'Jane', 'Emily',
                      'Robert', 'Jane', 'Linda', 'Robert', 'Linda', 'Michael', 'Jane', 'Emily', 'David', 'Laura'],
        'last_name': ['Williams', 'Smith', 'Jones', 'Johnson', 'Wilson', 'Jones', 'Johnson', 'Davis', 'Davis', 'Taylor',
                     'Jones', 'Davis', 'Johnson', 'Taylor', 'Johnson', 'Taylor', 'Jones', 'Wilson', 'Miller', 'Moore',
                     'Wilson', 'Brown', 'Johnson', 'Brown', 'Wilson', 'Taylor', 'Moore', 'Moore', 'Smith', 'Moore',
                     'Miller', 'Moore', 'Wilson', 'Smith', 'Wilson', 'Wilson', 'Williams', 'Smith', 'Wilson', 'Williams',
                     'Williams', 'Smith', 'Brown', 'Taylor', 'Miller', 'Taylor', 'Moore', 'Miller', 'Moore', 'Wilson'],
        'gender': ['F', 'F', 'M', 'F', 'M', 'M', 'F', 'F', 'M', 'M',
                  'F', 'F', 'F', 'M', 'M', 'M', 'M', 'M', 'M', 'F',
                  'M', 'M', 'M', 'F', 'M', 'M', 'F', 'M', 'M', 'M',
                  'M', 'M', 'F', 'F', 'F', 'M', 'M', 'M', 'F', 'M',
                  'M', 'F', 'M', 'F', 'F', 'F', 'M', 'M', 'M', 'M'],
        'date_of_birth': ['04-06-1955', '12-10-1984', '21-08-1977', '20-02-1981', '23-06-1960', '16-06-1963', '08-06-1989', '05-07-1976', '11-12-1971', '13-10-2001',
                         '04-12-1966', '08-12-1991', '28-03-1990', '27-02-1968', '11-05-1964', '22-07-2000', '01-05-1991', '24-09-1979', '24-05-1975', '06-06-2003',
                         '01-03-2002', '10-05-1955', '22-02-1994', '04-11-1991', '14-08-1966', '28-11-2003', '29-06-1998', '13-04-1993', '15-05-2005', '23-12-1964',
                         '14-01-1987', '08-01-1981', '06-02-1970', '26-01-1950', '13-04-1993', '26-12-1997', '05-02-1999', '25-06-1991', '12-12-1950', '30-05-1972',
                         '19-06-1951', '22-08-1954', '25-03-1980', '11-03-1976', '25-04-1966', '01-09-1986', '13-12-1995', '24-03-1983', '26-11-1972', '27-12-1993'],
        'contact_number': [6939585183, 8228188767, 8397029847, 9019443432, 7734463155, 7561777264, 6278710077, 7090558393, 7060324619, 7081396733,
                          8990604070, 8135666049, 9059178882, 7292262512, 6636028516, 7223380592, 6158428240, 7145815738, 8618058864, 8158989953,
                          7765390555, 6221099573, 6141951830, 7196777444, 7482069727, 9900972256, 8724518272, 7028910482, 8923607677, 6622318721,
                          8280346676, 8102183595, 7923214041, 8374657733, 7039619487, 8545613046, 8886800195, 6347262390, 9271131338, 7587653815,
                          7020645498, 7040069008, 9127665406, 9449458981, 7579616535, 8019925828, 8715732851, 8720989381, 7712937941, 8301134730],
        'address': ['789 Pine Rd', '321 Maple Dr', '321 Maple Dr', '123 Elm St', '123 Elm St', '321 Maple Dr', '789 Pine Rd', '456 Oak Ave', '321 Maple Dr', '123 Elm St',
                   '789 Pine Rd', '321 Maple Dr', '321 Maple Dr', '789 Pine Rd', '321 Maple Dr', '789 Pine Rd', '456 Oak Ave', '789 Pine Rd', '789 Pine Rd', '789 Pine Rd',
                   '321 Maple Dr', '321 Maple Dr', '789 Pine Rd', '321 Maple Dr', '123 Elm St', '123 Elm St', '321 Maple Dr', '321 Maple Dr', '789 Pine Rd', '456 Oak Ave',
                   '321 Maple Dr', '123 Elm St', '789 Pine Rd', '321 Maple Dr', '123 Elm St', '123 Elm St', '456 Oak Ave', '789 Pine Rd', '789 Pine Rd', '456 Oak Ave',
                   '456 Oak Ave', '789 Pine Rd', '789 Pine Rd', '321 Maple Dr', '321 Maple Dr', '456 Oak Ave', '321 Maple Dr', '123 Elm St', '321 Maple Dr', '321 Maple Dr'],
        'registration_date': ['23-06-2022', '15-01-2022', '07-02-2022', '02-03-2021', '29-09-2021', '02-10-2022', '25-12-2021', '25-05-2021', '18-09-2022', '24-08-2022',
                             '27-09-2022', '27-04-2023', '23-12-2021', '12-12-2023', '25-09-2021', '23-07-2021', '26-09-2022', '23-09-2022', '24-06-2023', '03-04-2022',
                             '19-01-2022', '11-05-2021', '27-12-2021', '02-09-2021', '09-09-2021', '13-05-2021', '15-08-2021', '20-05-2023', '19-04-2023', '07-08-2021',
                             '28-06-2022', '02-10-2021', '06-09-2023', '18-06-2023', '09-07-2023', '04-10-2022', '30-09-2021', '19-04-2021', '09-03-2021', '16-10-2021',
                             '16-07-2022', '15-03-2022', '18-07-2022', '26-01-2023', '23-01-2021', '31-07-2021', '20-05-2022', '19-06-2023', '14-06-2023', '28-04-2023'],
        'insurance_provider': ['WellnessCorp', 'PulseSecure', 'PulseSecure', 'HealthIndia', 'MedCare Plus', 'HealthIndia', 'MedCare Plus', 'WellnessCorp', 'PulseSecure', 'WellnessCorp',
                              'MedCare Plus', 'MedCare Plus', 'WellnessCorp', 'MedCare Plus', 'WellnessCorp', 'PulseSecure', 'WellnessCorp', 'PulseSecure', 'WellnessCorp', 'MedCare Plus',
                              'WellnessCorp', 'MedCare Plus', 'WellnessCorp', 'WellnessCorp', 'HealthIndia', 'MedCare Plus', 'HealthIndia', 'MedCare Plus', 'HealthIndia', 'PulseSecure',
                              'WellnessCorp', 'MedCare Plus', 'MedCare Plus', 'WellnessCorp', 'MedCare Plus', 'MedCare Plus', 'HealthIndia', 'MedCare Plus', 'PulseSecure', 'PulseSecure',
                              'WellnessCorp', 'MedCare Plus', 'WellnessCorp', 'PulseSecure', 'MedCare Plus', 'MedCare Plus', 'WellnessCorp', 'PulseSecure', 'MedCare Plus', 'WellnessCorp'],
        'insurance_number': ['INS840674', 'INS354079', 'INS650929', 'INS789944', 'INS788105', 'INS613758', 'INS465890', 'INS545101', 'INS136631', 'INS866577',
                            'INS172991', 'INS104014', 'INS373237', 'INS118070', 'INS922209', 'INS156958', 'INS182074', 'INS635017', 'INS855073', 'INS276089',
                            'INS297392', 'INS258823', 'INS730152', 'INS493002', 'INS833429', 'INS598863', 'INS467654', 'INS679036', 'INS630089', 'INS250262',
                            'INS542905', 'INS335362', 'INS544209', 'INS653880', 'INS897079', 'INS764076', 'INS319963', 'INS580761', 'INS348710', 'INS320984',
                            'INS997059', 'INS956748', 'INS882355', 'INS364512', 'INS701863', 'INS368799', 'INS337549', 'INS694319', 'INS584299', 'INS712210'],
        'email': ['david.williams@mail.com', 'emily.smith@mail.com', 'laura.jones@mail.com', 'michael.johnson@mail.com', 'david.wilson@mail.com', 'linda.johnson@mail.com', 'alex.johnson@mail.com', 'david.davis@mail.com', 'laura.davis@mail.com', 'michael.taylor@mail.com',
                 'emily.jones@mail.com', 'laura.davis@mail.com', 'laura.johnson@mail.com', 'alex.taylor@mail.com', 'sarah.johnson@mail.com', 'michael.taylor@mail.com', 'jane.jones@mail.com', 'laura.wilson@mail.com', 'sarah.miller@mail.com', 'jane.moore@mail.com',
                 'michael.wilson@mail.com', 'john.brown@mail.com', 'linda.johnson@mail.com', 'sarah.brown@mail.com', 'robert.wilson@mail.com', 'john.taylor@mail.com', 'linda.moore@mail.com', 'alex.moore@mail.com', 'david.smith@mail.com', 'emily.moore@mail.com',
                 'robert.miller@mail.com', 'alex.moore@mail.com', 'michael.wilson@mail.com', 'alex.smith@mail.com', 'david.wilson@mail.com', 'michael.wilson@mail.com', 'robert.williams@mail.com', 'david.smith@mail.com', 'jane.wilson@mail.com', 'emily.williams@mail.com',
                 'robert.williams@mail.com', 'jane.smith@mail.com', 'linda.brown@mail.com', 'robert.taylor@mail.com', 'linda.miller@mail.com', 'michael.taylor@mail.com', 'jane.moore@mail.com', 'emily.miller@mail.com', 'david.moore@mail.com', 'laura.wilson@mail.com']
    }

    # Doctors data (all 10 doctors)
    doctors_data = {
        'doctor_id': ['D001', 'D002', 'D003', 'D004', 'D005', 'D006', 'D007', 'D008', 'D009', 'D010'],
        'first_name': ['David', 'Jane', 'Jane', 'David', 'Sarah', 'Alex', 'Robert', 'Linda', 'Sarah', 'Linda'],
        'last_name': ['Taylor', 'Davis', 'Smith', 'Jones', 'Taylor', 'Davis', 'Davis', 'Brown', 'Smith', 'Wilson'],
        'specialization': ['Dermatology', 'Pediatrics', 'Pediatrics', 'Pediatrics', 'Dermatology', 'Pediatrics', 'Oncology', 'Dermatology', 'Pediatrics', 'Oncology'],
        'phone_number': [8322010158, 9004382050, 8737740598, 6594221991, 9118538547, 6570137231, 8217493115, 9069162601, 7387087517, 6176383634],
        'years_experience': [17, 24, 19, 28, 26, 23, 26, 5, 26, 21],
        'hospital_branch': ['Westside Clinic', 'Eastside Clinic', 'Eastside Clinic', 'Central Hospital', 'Central Hospital', 'Central Hospital', 'Westside Clinic', 'Westside Clinic', 'Central Hospital', 'Eastside Clinic'],
        'email': ['dr.david.taylor@hospital.com', 'dr.jane.davis@hospital.com', 'dr.jane.smith@hospital.com', 'dr.david.jones@hospital.com', 'dr.sarah.taylor@hospital.com', 'dr.alex.davis@hospital.com', 'dr.robert.davis@hospital.com', 'dr.linda.brown@hospital.com', 'dr.sarah.smith@hospital.com', 'dr.linda.wilson@hospital.com']
    }

    # Create DataFrames
    patients_df = pd.DataFrame(patients_data)
    doctors_df = pd.DataFrame(doctors_data)

    # For the larger datasets, we'll create them from the provided text data
    # Let's create a function to parse the text data
    def parse_text_data(data_text, columns):
        lines = data_text.strip().split('\n')
        data = []
        for line in lines[1:]:  # Skip the header row
            values = line.split('\t')
            if len(values) == len(columns):
                data.append(values)
        return pd.DataFrame(data, columns=columns)

    # Parse appointments data
    appointments_text = """appointment_id	patient_id	doctor_id	appointment_date	appointment_time	reason_for_visit	status
A001	P034	D009	09-08-2023	15:15:00	Therapy	Scheduled
A002	P032	D004	09-06-2023	14:30:00	Therapy	No-show
A003	P048	D004	28-06-2023	08:00:00	Consultation	Cancelled
A004	P025	D006	01-09-2023	09:15:00	Consultation	Cancelled
A005	P040	D003	06-07-2023	12:45:00	Emergency	No-show
A006	P045	D006	19-06-2023	16:15:00	Checkup	Scheduled
A007	P001	D007	09-04-2023	10:30:00	Consultation	Scheduled
A008	P016	D010	24-05-2023	08:45:00	Consultation	Cancelled
A009	P039	D010	05-03-2023	13:45:00	Follow-up	Scheduled
A010	P005	D003	13-01-2023	15:30:00	Therapy	Completed
A011	P022	D007	12-11-2023	16:00:00	Checkup	No-show
A012	P029	D003	07-05-2023	10:00:00	Follow-up	Completed
A013	P003	D002	16-08-2023	12:00:00	Emergency	Scheduled
A014	P012	D010	25-05-2023	10:30:00	Emergency	Cancelled
A015	P026	D004	15-01-2023	17:15:00	Consultation	No-show
A016	P016	D008	30-06-2023	11:00:00	Consultation	Scheduled
A017	P037	D009	11-07-2023	17:00:00	Emergency	Scheduled
A018	P022	D007	14-11-2023	09:45:00	Consultation	Cancelled
A019	P029	D001	06-02-2023	15:30:00	Checkup	Cancelled
A020	P014	D003	05-12-2023	15:15:00	Consultation	Completed
A021	P028	D009	24-04-2023	10:00:00	Therapy	No-show
A022	P005	D001	14-11-2023	13:00:00	Consultation	No-show
A023	P047	D009	09-05-2023	14:30:00	Follow-up	Cancelled
A024	P049	D008	21-06-2023	08:00:00	Checkup	Completed
A025	P030	D001	25-02-2023	08:00:00	Follow-up	No-show
A026	P046	D006	17-03-2023	14:15:00	Follow-up	Cancelled
A027	P005	D005	14-11-2023	12:45:00	Therapy	Scheduled
A028	P012	D006	29-10-2023	15:30:00	Checkup	No-show
A029	P016	D010	25-06-2023	14:30:00	Checkup	Completed
A030	P026	D005	29-08-2023	13:15:00	Checkup	Completed
A031	P026	D006	04-04-2023	10:30:00	Checkup	Completed
A032	P048	D005	06-11-2023	10:45:00	Checkup	Scheduled
A033	P021	D005	23-09-2023	17:45:00	Therapy	No-show
A034	P039	D004	13-06-2023	11:30:00	Consultation	No-show
A035	P036	D003	18-04-2023	08:45:00	Follow-up	Scheduled
A036	P033	D003	08-01-2023	14:30:00	Checkup	No-show
A037	P030	D004	28-03-2023	11:00:00	Consultation	Scheduled
A038	P037	D009	23-02-2023	13:00:00	Consultation	Scheduled
A039	P023	D002	17-04-2023	08:00:00	Follow-up	Scheduled
A040	P010	D009	27-03-2023	12:30:00	Therapy	Completed
A041	P005	D001	01-01-2023	14:00:00	Emergency	No-show
A042	P036	D001	21-03-2023	11:15:00	Emergency	Scheduled
A043	P034	D005	29-03-2023	09:15:00	Consultation	No-show
A044	P031	D006	20-09-2023	12:30:00	Follow-up	Completed
A045	P010	D006	28-09-2023	17:00:00	Emergency	Scheduled
A046	P019	D003	20-12-2023	13:15:00	Consultation	Cancelled
A047	P032	D007	02-05-2023	11:00:00	Therapy	Completed
A048	P001	D009	16-01-2023	15:45:00	Emergency	Cancelled
A049	P005	D010	30-04-2023	15:30:00	Consultation	No-show
A050	P045	D008	16-08-2023	15:00:00	Consultation	No-show
A051	P004	D006	04-02-2023	11:45:00	Checkup	Completed
A052	P016	D008	12-07-2023	09:30:00	Therapy	No-show
A053	P024	D005	12-02-2023	10:30:00	Checkup	Cancelled
A054	P016	D008	16-12-2023	11:45:00	Follow-up	Scheduled
A055	P002	D010	06-10-2023	17:30:00	Checkup	Scheduled
A056	P049	D004	02-01-2023	12:45:00	Checkup	Scheduled
A057	P028	D010	15-04-2023	17:45:00	Emergency	Completed
A058	P032	D008	09-05-2023	13:15:00	Consultation	No-show
A059	P027	D010	09-03-2023	15:30:00	Therapy	Cancelled
A060	P020	D002	22-11-2023	17:15:00	Checkup	No-show
A061	P024	D005	15-01-2023	17:00:00	Therapy	No-show
A062	P012	D009	14-06-2023	15:15:00	Checkup	No-show
A063	P050	D004	29-06-2023	09:00:00	Follow-up	Scheduled
A064	P035	D006	31-05-2023	08:30:00	Checkup	Cancelled
A065	P033	D001	24-04-2023	15:45:00	Emergency	Cancelled
A066	P033	D009	10-05-2023	11:45:00	Consultation	No-show
A067	P043	D001	10-08-2023	11:00:00	Follow-up	Scheduled
A068	P037	D005	14-03-2023	15:00:00	Checkup	Scheduled
A069	P012	D004	29-03-2023	15:30:00	Therapy	Cancelled
A070	P003	D003	26-08-2023	17:00:00	Follow-up	Scheduled
A071	P001	D006	26-01-2023	17:00:00	Follow-up	Scheduled
A072	P033	D002	12-06-2023	13:30:00	Checkup	Scheduled
A073	P040	D003	24-12-2023	15:00:00	Follow-up	Completed
A074	P010	D005	23-07-2023	13:30:00	Therapy	No-show
A075	P043	D009	08-05-2023	14:00:00	Follow-up	Cancelled
A076	P044	D002	27-11-2023	12:00:00	Therapy	Cancelled
A077	P029	D010	14-12-2023	17:15:00	Checkup	Completed
A078	P013	D008	17-09-2023	11:15:00	Consultation	No-show
A079	P012	D002	26-12-2023	14:00:00	Follow-up	Cancelled
A080	P031	D005	26-06-2023	08:30:00	Consultation	Scheduled
A081	P046	D007	06-01-2023	13:30:00	Therapy	Cancelled
A082	P002	D008	20-01-2023	10:45:00	Follow-up	Scheduled
A083	P050	D001	07-11-2023	12:30:00	Emergency	Completed
A084	P035	D006	31-05-2023	16:00:00	Consultation	Scheduled
A085	P023	D001	18-02-2023	16:15:00	Follow-up	Cancelled
A086	P017	D002	29-10-2023	11:00:00	Consultation	Cancelled
A087	P026	D001	19-10-2023	12:15:00	Follow-up	Cancelled
A088	P008	D005	02-05-2023	16:30:00	Checkup	Completed
A089	P029	D010	14-02-2023	11:00:00	Consultation	Completed
A090	P026	D009	01-06-2023	17:30:00	Emergency	No-show
A091	P010	D006	11-06-2023	13:15:00	Emergency	Cancelled
A092	P026	D001	30-01-2023	14:15:00	Therapy	Scheduled
A093	P034	D001	09-04-2023	09:30:00	Follow-up	Completed
A094	P041	D002	08-04-2023	08:45:00	Consultation	Cancelled
A095	P007	D009	09-05-2023	10:15:00	Therapy	Cancelled
A096	P004	D003	07-07-2023	15:00:00	Consultation	Completed
A097	P050	D001	06-05-2023	14:45:00	Follow-up	No-show
A098	P045	D005	17-03-2023	13:00:00	Emergency	Completed
A099	P011	D007	04-07-2023	15:00:00	Checkup	Completed
A100	P029	D006	02-03-2023	08:00:00	Emergency	Scheduled
A101	P036	D001	21-09-2023	13:15:00	Therapy	Scheduled
A102	P025	D005	25-10-2023	09:00:00	Checkup	No-show
A103	P021	D005	24-01-2023	08:30:00	Therapy	Cancelled
A104	P036	D006	18-04-2023	08:45:00	Follow-up	Completed
A105	P010	D003	14-08-2023	16:00:00	Checkup	No-show
A106	P037	D005	29-10-2023	11:15:00	Therapy	Scheduled
A107	P009	D007	17-04-2023	13:45:00	Follow-up	Completed
A108	P024	D005	21-04-2023	15:00:00	Emergency	Cancelled
A109	P035	D005	29-07-2023	14:00:00	Follow-up	Scheduled
A110	P049	D005	19-07-2023	14:30:00	Consultation	Scheduled
A111	P035	D010	22-05-2023	15:30:00	Follow-up	Scheduled
A112	P048	D010	11-01-2023	08:00:00	Follow-up	No-show
A113	P036	D003	24-11-2023	15:30:00	Consultation	Cancelled
A114	P018	D001	08-08-2023	09:00:00	Therapy	Completed
A115	P049	D005	25-10-2023	10:30:00	Therapy	No-show
A116	P039	D009	07-07-2023	09:15:00	Follow-up	No-show
A117	P032	D001	20-06-2023	13:45:00	Consultation	No-show
A118	P024	D003	09-08-2023	08:15:00	Consultation	Scheduled
A119	P023	D004	18-12-2023	13:30:00	Emergency	Cancelled
A120	P032	D001	08-12-2023	11:00:00	Therapy	No-show
A121	P037	D001	07-04-2023	15:00:00	Checkup	Completed
A122	P012	D008	11-07-2023	14:30:00	Therapy	Cancelled
A123	P049	D002	28-02-2023	10:45:00	Therapy	Completed
A124	P013	D008	16-03-2023	17:15:00	Emergency	Cancelled
A125	P023	D007	18-02-2023	10:15:00	Checkup	Completed
A126	P025	D010	02-11-2023	09:45:00	Emergency	Scheduled
A127	P035	D010	13-11-2023	08:30:00	Checkup	No-show
A128	P041	D002	15-04-2023	14:45:00	Follow-up	Completed
A129	P030	D006	25-08-2023	09:30:00	Checkup	Cancelled
A130	P017	D006	23-02-2023	15:00:00	Emergency	No-show
A131	P049	D003	11-05-2023	16:30:00	Therapy	No-show
A132	P020	D002	26-07-2023	10:45:00	Checkup	Cancelled
A133	P048	D001	23-03-2023	14:30:00	Checkup	Completed
A134	P025	D006	17-10-2023	15:15:00	Consultation	Scheduled
A135	P022	D005	09-09-2023	16:30:00	Therapy	Scheduled
A136	P013	D009	13-05-2023	12:30:00	Follow-up	Completed
A137	P019	D001	25-10-2023	10:00:00	Emergency	No-show
A138	P049	D007	26-12-2023	15:15:00	Follow-up	No-show
A139	P036	D005	10-10-2023	10:45:00	Therapy	No-show
A140	P012	D005	05-02-2023	15:15:00	Checkup	No-show
A141	P041	D002	15-06-2023	15:15:00	Checkup	Completed
A142	P019	D003	01-11-2023	11:45:00	Therapy	No-show
A143	P012	D007	21-09-2023	12:15:00	Checkup	Cancelled
A144	P009	D006	16-08-2023	12:15:00	Checkup	No-show
A145	P007	D002	11-11-2023	14:45:00	Checkup	Scheduled
A146	P028	D006	05-01-2023	09:30:00	Emergency	No-show
A147	P014	D002	13-11-2023	17:30:00	Emergency	Completed
A148	P031	D002	06-12-2023	08:30:00	Consultation	Scheduled
A149	P019	D002	26-07-2023	12:30:00	Follow-up	Completed
A150	P047	D003	16-08-2023	10:45:00	Therapy	Completed
A151	P016	D002	28-01-2023	09:15:00	Therapy	Scheduled
A152	P005	D004	14-04-2023	08:30:00	Therapy	Completed
A153	P035	D009	08-07-2023	12:45:00	Consultation	Completed
A154	P012	D006	06-03-2023	17:30:00	Emergency	No-show
A155	P025	D001	03-01-2023	09:30:00	Consultation	Cancelled
A156	P021	D008	22-11-2023	14:30:00	Therapy	Completed
A157	P036	D007	12-05-2023	11:00:00	Follow-up	Completed
A158	P023	D010	12-07-2023	12:15:00	Checkup	Completed
A159	P016	D003	08-04-2023	16:15:00	Emergency	No-show
A160	P039	D001	17-12-2023	12:45:00	Emergency	Cancelled
A161	P045	D005	17-06-2023	10:45:00	Consultation	Scheduled
A162	P042	D004	01-01-2023	17:15:00	Emergency	No-show
A162	P039	D010	27-06-2023	15:00:00	Therapy	No-show
A163	P014	D008	28-07-2023	17:15:00	Therapy	Cancelled
A164	P031	D001	04-04-2023	15:30:00	Consultation	Cancelled
A165	P005	D010	12-01-2023	14:45:00	Therapy	No-show
A166	P035	D001	15-11-2023	08:15:00	Follow-up	Scheduled
A167	P023	D004	29-09-2023	10:00:00	Consultation	No-show
A168	P029	D008	24-07-2023	16:45:00	Follow-up	Cancelled
A169	P043	D005	03-03-2023	09:00:00	Checkup	Scheduled
A170	P011	D002	18-04-2023	16:30:00	Follow-up	Cancelled
A171	P018	D006	09-03-2023	16:15:00	Checkup	Scheduled
A172	P047	D005	04-06-2023	13:30:00	Checkup	Completed
A173	P012	D002	31-10-2023	11:15:00	Follow-up	Cancelled
A174	P009	D003	22-10-2023	17:00:00	Consultation	Cancelled
A175	P010	D009	26-04-2023	09:30:00	Therapy	No-show
A176	P044	D007	16-08-2023	12:30:00	Therapy	Cancelled
A177	P017	D007	17-01-2023	13:15:00	Checkup	Cancelled
A178	P038	D006	08-03-2023	12:15:00	Checkup	Completed
A179	P007	D008	07-01-2023	11:00:00	Consultation	Cancelled
A180	P046	D004	03-09-2023	13:15:00	Emergency	Completed
A181	P013	D008	12-04-2023	08:00:00	Follow-up	Completed
A182	P040	D004	03-02-2023	16:15:00	Checkup	Completed
A183	P042	D008	26-02-2023	17:45:00	Therapy	Completed
A184	P009	D009	21-03-2023	14:00:00	Consultation	Scheduled
A185	P050	D003	27-03-2023	17:15:00	Follow-up	No-show
A186	P027	D003	13-02-2023	12:30:00	Consultation	Scheduled
A187	P002	D002	12-04-2023	16:30:00	Follow-up	Cancelled
A188	P005	D010	05-10-2023	13:30:00	Follow-up	Scheduled
A189	P029	D003	16-11-2023	15:15:00	Checkup	Scheduled
A190	P037	D003	12-04-2023	16:00:00	Consultation	Cancelled
A191	P038	D005	31-08-2023	14:15:00	Consultation	Cancelled
A192	P019	D005	15-09-2023	08:15:00	Therapy	Cancelled
A193	P008	D002	06-04-2023	12:45:00	Therapy	Scheduled
A194	P048	D010	19-08-2023	17:15:00	Checkup	Scheduled
A195	P045	D006	26-10-2023	09:45:00	Checkup	Cancelled
A196	P001	D005	01-04-2023	13:30:00	Emergency	No-show
A197	P022	D006	15-05-2023	08:30:00	Therapy	No-show
A198	P017	D001	01-05-2023	12:45:00	Follow-up	Completed
A199	P007	D005	30-12-2023	10:15:00	Consultation	Cancelled
A200	P007	D005	30-12-2023	10:15:00	Consultation	Cancelled"""

    appointments_df = parse_text_data(appointments_text,
                                    ['appointment_id', 'patient_id', 'doctor_id', 'appointment_date',
                                     'appointment_time', 'reason_for_visit', 'status'])

    # Parse treatments data
    treatments_text = """treatment_id	appointment_id	treatment_type	description	cost	treatment_date
T001	A001	Chemotherapy	Basic screening	3941.97	09-08-2023
T002	A002	MRI	Advanced protocol	4158.44	09-06-2023
T003	A003	MRI	Standard procedure	3731.55	28-06-2023
T004	A004	MRI	Basic screening	4799.86	01-09-2023
T005	A005	ECG	Standard procedure	582.05	06-07-2023
T006	A006	Chemotherapy	Standard procedure	1381	19-06-2023
T007	A007	Chemotherapy	Advanced protocol	534.03	09-04-2023
T008	A008	Physiotherapy	Basic screening	3413.64	24-05-2023
T009	A009	Physiotherapy	Standard procedure	4541.14	05-03-2023
T010	A010	Physiotherapy	Standard procedure	1595.67	13-01-2023
T011	A011	MRI	Basic screening	4671.66	12-11-2023
T012	A012	Chemotherapy	Standard procedure	771.2	07-05-2023
T013	A013	MRI	Standard procedure	4704.96	16-08-2023
T014	A014	ECG	Basic screening	2082.3	25-05-2023
T015	A015	Physiotherapy	Basic screening	956.39	15-01-2023
T016	A016	MRI	Basic screening	2686.42	30-06-2023
T017	A017	MRI	Basic screening	1655.49	11-07-2023
T018	A018	ECG	Advanced protocol	1781.93	14-11-2023
T019	A019	X-Ray	Basic screening	1882.8	06-02-2023
T020	A020	Chemotherapy	Advanced protocol	4113.62	05-12-2023
T021	A021	X-Ray	Advanced protocol	2926.23	24-04-2023
T022	A022	Physiotherapy	Advanced protocol	1900.88	14-11-2023
T023	A023	MRI	Standard procedure	3246.5	09-05-2023
T024	A024	ECG	Advanced protocol	3722.68	21-06-2023
T025	A025	ECG	Advanced protocol	1726.81	25-02-2023
T026	A026	Chemotherapy	Standard procedure	2360.97	17-03-2023
T027	A027	X-Ray	Standard procedure	1048.49	14-11-2023
T028	A028	Chemotherapy	Standard procedure	1315.17	29-10-2023
T029	A029	MRI	Basic screening	3565.03	25-06-2023
T030	A030	Chemotherapy	Standard procedure	1316.47	29-08-2023
T031	A031	ECG	Standard procedure	2863.24	04-04-2023
T032	A032	ECG	Advanced protocol	3690.71	06-11-2023
T033	A033	Physiotherapy	Standard procedure	980.95	23-09-2023
T034	A034	Physiotherapy	Basic screening	3052.9	13-06-2023
T035	A035	MRI	Standard procedure	1654.53	18-04-2023
T036	A036	X-Ray	Basic screening	4833.17	08-01-2023
T037	A037	Chemotherapy	Standard procedure	2675.96	28-03-2023
T038	A038	MRI	Standard procedure	4126.97	23-02-2023
T039	A039	Physiotherapy	Standard procedure	2976.02	17-04-2023
T040	A040	Chemotherapy	Standard procedure	695.36	27-03-2023
T041	A041	Physiotherapy	Basic screening	3349.18	01-01-2023
T042	A042	Chemotherapy	Basic screening	4781.32	21-03-2023
T043	A043	X-Ray	Advanced protocol	3207.25	29-03-2023
T044	A044	MRI	Basic screening	4186.35	20-09-2023
T045	A045	Chemotherapy	Standard procedure	4478.93	28-09-2023
T046	A046	ECG	Advanced protocol	1526.36	20-12-2023
T047	A047	ECG	Advanced protocol	1454.2	02-05-2023
T048	A048	Chemotherapy	Advanced protocol	3249.41	16-01-2023
T049	A049	Chemotherapy	Standard procedure	2349.63	30-04-2023
T050	A050	Chemotherapy	Basic screening	4279.38	16-08-2023
T051	A051	ECG	Standard procedure	4550.1	04-02-2023
T052	A052	ECG	Advanced protocol	2090.4	12-07-2023
T053	A053	Chemotherapy	Standard procedure	1565.92	12-02-2023
T054	A054	Physiotherapy	Standard procedure	4012.36	16-12-2023
T055	A055	Physiotherapy	Basic screening	1736.63	06-10-2023
T056	A056	X-Ray	Basic screening	4201.76	02-01-2023
T057	A057	MRI	Advanced protocol	2406.82	15-04-2023
T058	A058	Physiotherapy	Standard procedure	3503.97	09-05-2023
T059	A059	ECG	Standard procedure	929.91	09-03-2023
T060	A060	Physiotherapy	Basic screening	3307.37	22-11-2023
T061	A061	X-Ray	Standard procedure	2532.95	15-01-2023
T062	A062	X-Ray	Standard procedure	3139.74	14-06-2023
T063	A063	MRI	Standard procedure	1256.06	29-06-2023
T064	A064	Physiotherapy	Basic screening	3815.93	31-05-2023
T065	A065	ECG	Advanced protocol	4382.59	24-04-2023
T066	A066	ECG	Advanced protocol	1475.33	10-05-2023
T067	A067	Chemotherapy	Standard procedure	930.72	10-08-2023
T068	A068	ECG	Advanced protocol	606.37	14-03-2023
T069	A069	MRI	Basic screening	3388.87	29-03-2023
T070	A070	MRI	Basic screening	3231.92	26-08-2023
T071	A071	ECG	Advanced protocol	2960.14	26-01-2023
T072	A072	ECG	Advanced protocol	1543.76	12-06-2023
T073	A073	Chemotherapy	Standard procedure	2259.08	24-12-2023
T074	A074	ECG	Advanced protocol	3175.14	23-07-2023
T075	A075	Chemotherapy	Standard procedure	2735.45	08-05-2023
T076	A076	Chemotherapy	Standard procedure	4945.03	27-11-2023
T077	A077	ECG	Basic screening	1113.98	14-12-2023
T078	A078	X-Ray	Basic screening	3628.15	17-09-2023
T079	A079	X-Ray	Basic screening	2319.43	26-12-2023
T080	A080	Chemotherapy	Basic screening	2426.9	26-06-2023
T081	A081	ECG	Advanced protocol	3729.19	06-01-2023
T082	A082	X-Ray	Basic screening	3615.96	20-01-2023
T083	A083	ECG	Advanced protocol	4960.65	07-11-2023
T084	A084	ECG	Basic screening	1077.77	31-05-2023
T085	A085	ECG	Advanced protocol	968.49	18-02-2023
T086	A086	Physiotherapy	Standard procedure	3759.52	29-10-2023
T087	A087	ECG	Advanced protocol	3102.74	19-10-2023
T088	A088	Physiotherapy	Advanced protocol	1733.72	02-05-2023
T089	A089	Chemotherapy	Basic screening	857.39	14-02-2023
T090	A090	X-Ray	Advanced protocol	885.46	01-06-2023
T091	A091	X-Ray	Standard procedure	4523.86	11-06-2023
T092	A092	X-Ray	Standard procedure	1363.4	30-01-2023
T093	A093	X-Ray	Basic screening	1955.17	09-04-2023
T094	A094	X-Ray	Standard procedure	1519.95	08-04-2023
T095	A095	X-Ray	Advanced protocol	2097.48	09-05-2023
T096	A096	X-Ray	Standard procedure	812.41	07-07-2023
T097	A097	Chemotherapy	Basic screening	2835.77	06-05-2023
T098	A098	ECG	Advanced protocol	804.26	17-03-2023
T099	A099	MRI	Basic screening	4101.6	04-07-2023
T100	A100	Physiotherapy	Advanced protocol	1551.7	02-03-2023
T101	A101	MRI	Standard procedure	2930.05	21-09-2023
T102	A102	MRI	Basic screening	4460.36	25-10-2023
T103	A103	ECG	Basic screening	3428.95	24-01-2023
T104	A104	ECG	Advanced protocol	2898.31	18-04-2023
T105	A105	ECG	Basic screening	1959.5	14-08-2023
T106	A106	X-Ray	Advanced protocol	1998.51	29-10-2023
T107	A107	Chemotherapy	Advanced protocol	3512.69	17-04-2023
T108	A108	X-Ray	Advanced protocol	4973.63	21-04-2023
T109	A109	Chemotherapy	Advanced protocol	3478.28	29-07-2023
T110	A110	Chemotherapy	Standard procedure	3010.03	19-07-2023
T111	A111	MRI	Advanced protocol	3787.93	22-05-2023
T112	A112	MRI	Basic screening	2593.43	11-01-2023
T113	A113	Chemotherapy	Standard procedure	770.64	24-11-2023
T114	A114	Chemotherapy	Basic screening	3030.34	08-08-2023
T115	A115	X-Ray	Standard procedure	4809.31	25-10-2023
T116	A116	X-Ray	Advanced protocol	1288.86	07-07-2023
T117	A117	MRI	Standard procedure	3605.02	20-06-2023
T118	A118	ECG	Standard procedure	1404.2	09-08-2023
T119	A119	Chemotherapy	Basic screening	2911.22	18-12-2023
T120	A120	X-Ray	Basic screening	935.04	08-12-2023
T121	A121	MRI	Advanced protocol	2526.67	07-04-2023
T122	A122	X-Ray	Standard procedure	3902.73	11-07-2023
T123	A123	Chemotherapy	Standard procedure	2064.07	28-02-2023
T124	A124	Chemotherapy	Standard procedure	3492.1	16-03-2023
T125	A125	Physiotherapy	Advanced protocol	4079.52	18-02-2023
T126	A126	ECG	Advanced protocol	4672.3	02-11-2023
T127	A127	Physiotherapy	Advanced protocol	1555.89	13-11-2023
T128	A128	MRI	Advanced protocol	2296.92	15-04-2023
T129	A129	X-Ray	Advanced protocol	1185.87	25-08-2023
T130	A130	MRI	Basic screening	4966.18	23-02-2023
T131	A131	Chemotherapy	Standard procedure	4671.5	11-05-2023
T132	A132	Physiotherapy	Standard procedure	2929.81	26-07-2023
T133	A133	Physiotherapy	Standard procedure	4289.15	23-03-2023
T134	A134	Physiotherapy	Standard procedure	2844.31	17-10-2023
T135	A135	MRI	Standard procedure	3306.14	09-09-2023
T136	A136	Chemotherapy	Standard procedure	901.06	13-05-2023
T137	A137	X-Ray	Standard procedure	3898.72	25-10-2023
T138	A138	X-Ray	Standard procedure	1074.71	26-12-2023
T139	A139	MRI	Basic screening	4217.3	10-10-2023
T140	A140	Physiotherapy	Standard procedure	4019.13	05-02-2023
T141	A141	ECG	Basic screening	3689.35	15-06-2023
T142	A142	MRI	Advanced protocol	662.72	01-11-2023
T143	A143	MRI	Standard procedure	1864.08	21-09-2023
T144	A144	Chemotherapy	Advanced protocol	1684.01	16-08-2023
T145	A145	X-Ray	Advanced protocol	2120.61	11-11-2023
T146	A146	MRI	Advanced protocol	894.39	05-01-2023
T147	A147	MRI	Basic screening	4716.31	13-11-2023
T148	A148	Physiotherapy	Advanced protocol	2992.11	06-12-2023
T149	A149	Physiotherapy	Advanced protocol	1874.86	26-07-2023
T150	A150	ECG	Advanced protocol	2286.42	16-08-2023
T151	A151	Chemotherapy	Standard procedure	2512.41	28-01-2023
T152	A152	ECG	Standard procedure	3202.67	14-04-2023
T153	A153	Physiotherapy	Basic screening	2820.56	08-07-2023
T154	A154	X-Ray	Basic screening	4637.26	06-03-2023
T155	A155	Physiotherapy	Standard procedure	2736.34	03-01-2023
T156	A156	Chemotherapy	Basic screening	4964.71	22-11-2023
T157	A157	Physiotherapy	Standard procedure	4331.41	12-05-2023
T158	A158	Chemotherapy	Advanced protocol	1438.3	12-07-2023
T159	A159	Chemotherapy	Advanced protocol	4687.68	08-04-2023
T160	A160	Chemotherapy	Basic screening	1023.65	17-12-2023
T161	A161	Chemotherapy	Standard procedure	4178.52	17-06-2023
T162	A162	Chemotherapy	Standard procedure	2212.8	01-01-2023
T163	A163	X-Ray	Basic screening	4450.88	27-06-2023
T164	A164	ECG	Standard procedure	4406.26	28-07-2023
T165	A165	MRI	Advanced protocol	4126.66	04-04-2023
T166	A166	ECG	Basic screening	4055.14	12-01-2023
T167	A167	Chemotherapy	Basic screening	1871.06	15-11-2023
T168	A168	X-Ray	Standard procedure	864.14	29-09-2023
T169	A169	Physiotherapy	Basic screening	2313.41	24-07-2023
T170	A170	X-Ray	Standard procedure	1280.86	03-03-2023
T171	A171	Chemotherapy	Standard procedure	3627.28	18-04-2023
T172	A172	X-Ray	Standard procedure	2057.45	09-03-2023
T173	A173	X-Ray	Standard procedure	4890.25	04-06-2023
T174	A174	Chemotherapy	Standard procedure	3384.37	31-10-2023
T175	A175	X-Ray	Basic screening	4201.16	22-10-2023
T176	A176	MRI	Advanced protocol	1096.36	26-04-2023
T177	A177	MRI	Advanced protocol	4379.07	16-08-2023
T178	A178	X-Ray	Basic screening	4652.41	17-01-2023
T179	A179	Physiotherapy	Basic screening	2691.78	08-03-2023
T180	A180	Chemotherapy	Advanced protocol	3228.14	07-01-2023
T181	A181	MRI	Advanced protocol	3941.64	03-09-2023
T182	A182	Physiotherapy	Advanced protocol	1286.77	12-04-2023
T183	A183	X-Ray	Advanced protocol	2761.55	03-02-2023
T184	A184	Physiotherapy	Advanced protocol	2293.98	26-02-2023
T185	A185	ECG	Standard procedure	1158.68	21-03-2023
T186	A186	MRI	Basic screening	2153.9	27-03-2023
T187	A187	X-Ray	Standard procedure	806.78	13-02-2023
T188	A188	Chemotherapy	Advanced protocol	616.15	12-04-2023
T189	A189	X-Ray	Advanced protocol	1108.25	05-10-2023
T190	A190	Chemotherapy	Advanced protocol	4834.02	16-11-2023
T191	A191	X-Ray	Standard procedure	2972.88	12-04-2023
T192	A192	Physiotherapy	Standard procedure	4846.2	31-08-2023
T193	A193	Physiotherapy	Advanced protocol	2446.24	15-09-2023
T194	A194	Physiotherapy	Standard procedure	1903.17	06-04-2023
T195	A195	ECG	Standard procedure	2777.64	19-08-2023
T196	A196	Chemotherapy	Advanced protocol	2477.8	26-10-2023
T197	A197	Physiotherapy	Standard procedure	975.49	01-04-2023
T198	A198	ECG	Basic screening	3383.72	15-05-2023
T199	A199	Chemotherapy	Basic screening	1472.17	01-05-2023
T200	A200	X-Ray	Basic screening	3288.15	30-12-2023"""

    treatments_df = parse_text_data(treatments_text,
                                  ['treatment_id', 'appointment_id', 'treatment_type',
                                   'description', 'cost', 'treatment_date'])

    # Parse billing data
    billing_text = """bill_id	patient_id	treatment_id	bill_date	amount	payment_method	payment_status
B001	P034	T001	09-08-2023	3941.97	Insurance	Pending
B002	P032	T002	09-06-2023	4158.44	Insurance	Paid
B003	P048	T003	28-06-2023	3731.55	Insurance	Paid
B004	P025	T004	01-09-2023	4799.86	Insurance	Failed
B005	P040	T005	06-07-2023	582.05	Credit Card	Pending
B006	P045	T006	19-06-2023	1381	Insurance	Pending
B007	P001	T007	09-04-2023	534.03	Cash	Failed
B008	P016	T008	24-05-2023	3413.64	Cash	Failed
B009	P039	T009	05-03-2023	4541.14	Credit Card	Paid
B010	P005	T010	13-01-2023	1595.67	Cash	Paid
B011	P022	T011	12-11-2023	4671.66	Cash	Failed
B012	P029	T012	07-05-2023	771.2	Insurance	Pending
B013	P003	T013	16-08-2023	4704.96	Cash	Paid
B014	P012	T014	25-05-2023	2082.3	Credit Card	Paid
B015	P026	T015	15-01-2023	956.39	Insurance	Pending
B016	P016	T016	30-06-2023	2686.42	Insurance	Paid
B017	P037	T017	11-07-2023	1655.49	Credit Card	Pending
B018	P022	T018	14-11-2023	1781.93	Insurance	Pending
B019	P029	T019	06-02-2023	1882.8	Insurance	Pending
B020	P014	T020	05-12-2023	4113.62	Credit Card	Failed
B021	P028	T021	24-04-2023	2926.23	Insurance	Failed
B022	P005	T022	14-11-2023	1900.88	Credit Card	Failed
B023	P047	T023	09-05-2023	3246.5	Credit Card	Pending
B024	P049	T024	21-06-2023	3722.68	Cash	Pending
B025	P030	T025	25-02-2023	1726.81	Cash	Failed
B026	P046	T026	17-03-2023	2360.97	Insurance	Paid
B027	P005	T027	14-11-2023	1048.49	Insurance	Pending
B028	P012	T028	29-10-2023	1315.17	Credit Card	Paid
B029	P016	T029	25-06-2023	3565.03	Insurance	Paid
B030	P026	T030	29-08-2023	1316.47	Credit Card	Pending
B031	P026	T031	04-04-2023	2863.24	Credit Card	Pending
B032	P048	T032	06-11-2023	3690.71	Insurance	Paid
B033	P021	T033	23-09-2023	980.95	Credit Card	Paid
B034	P039	T034	13-06-2023	3052.9	Cash	Failed
B035	P036	T035	18-04-2023	1654.53	Insurance	Failed
B036	P033	T036	08-01-2023	4833.17	Cash	Pending
B037	P030	T037	28-03-2023	2675.96	Insurance	Failed
B038	P037	T038	23-02-2023	4126.97	Credit Card	Failed
B039	P023	T039	17-04-2023	2976.02	Insurance	Failed
B040	P010	T040	27-03-2023	695.36	Cash	Failed
B041	P005	T041	01-01-2023	3349.18	Credit Card	Paid
B042	P036	T042	21-03-2023	4781.32	Insurance	Pending
B043	P034	T043	29-03-2023	3207.25	Insurance	Failed
B044	P031	T044	20-09-2023	4186.35	Insurance	Paid
B045	P010	T045	28-09-2023	4478.93	Cash	Paid
B046	P019	T046	20-12-2023	1526.36	Cash	Paid
B047	P032	T047	02-05-2023	1454.2	Insurance	Failed
B048	P001	T048	16-01-2023	3249.41	Credit Card	Failed
B049	P005	T049	30-04-2023	2349.63	Credit Card	Pending
B050	P045	T050	16-08-2023	4279.38	Cash	Failed
B051	P004	T051	04-02-2023	4550.1	Credit Card	Failed
B052	P016	T052	12-07-2023	2090.4	Cash	Paid
B053	P024	T053	12-02-2023	1565.92	Insurance	Pending
B054	P016	T054	16-12-2023	4012.36	Cash	Failed
B055	P002	T055	06-10-2023	1736.63	Cash	Failed
B056	P049	T056	02-01-2023	4201.76	Insurance	Paid
B057	P028	T057	15-04-2023	2406.82	Credit Card	Paid
B058	P032	T058	09-05-2023	3503.97	Cash	Failed
B059	P027	T059	09-03-2023	929.91	Cash	Pending
B060	P020	T060	22-11-2023	3307.37	Insurance	Pending
B061	P024	T061	15-01-2023	2532.95	Credit Card	Paid
B062	P012	T062	14-06-2023	3139.74	Cash	Paid
B063	P050	T063	29-06-2023	1256.06	Insurance	Failed
B064	P035	T064	31-05-2023	3815.93	Cash	Paid
B065	P033	T065	24-04-2023	4382.59	Insurance	Failed
B066	P033	T066	10-05-2023	1475.33	Credit Card	Pending
B067	P043	T067	10-08-2023	930.72	Credit Card	Pending
B068	P037	T068	14-03-2023	606.37	Credit Card	Failed
B069	P012	T069	29-03-2023	3388.87	Credit Card	Paid
B070	P003	T070	26-08-2023	3231.92	Cash	Pending
B071	P001	T071	26-01-2023	2960.14	Cash	Paid
B072	P033	T072	12-06-2023	1543.76	Credit Card	Pending
B073	P040	T073	24-12-2023	2259.08	Credit Card	Failed
B074	P010	T074	23-07-2023	3175.14	Credit Card	Failed
B075	P043	T075	08-05-2023	2735.45	Cash	Failed
B076	P044	T076	27-11-2023	4945.03	Credit Card	Pending
B077	P029	T077	14-12-2023	1113.98	Credit Card	Paid
B078	P013	T078	17-09-2023	3628.15	Credit Card	Paid
B079	P012	T079	26-12-2023	2319.43	Insurance	Paid
B080	P031	T080	26-06-2023	2426.9	Credit Card	Pending
B081	P046	T081	06-01-2023	3729.19	Insurance	Pending
B082	P002	T082	20-01-2023	3615.96	Insurance	Pending
B083	P050	T083	07-11-2023	4960.65	Credit Card	Pending
B084	P035	T084	31-05-2023	1077.77	Insurance	Pending
B085	P023	T085	18-02-2023	968.49	Credit Card	Paid
B086	P017	T086	29-10-2023	3759.52	Cash	Pending
B087	P026	T087	19-10-2023	3102.74	Cash	Pending
B088	P008	T088	02-05-2023	1733.72	Cash	Paid
B089	P029	T089	14-02-2023	857.39	Cash	Pending
B090	P026	T090	01-06-2023	885.46	Insurance	Paid
B091	P010	T091	11-06-2023	4523.86	Credit Card	Paid
B092	P026	T092	30-01-2023	1363.4	Credit Card	Failed
B093	P034	T093	09-04-2023	1955.17	Credit Card	Failed
B094	P041	T094	08-04-2023	1519.95	Cash	Failed
B095	P007	T095	09-05-2023	2097.48	Cash	Failed
B096	P004	T096	07-07-2023	812.41	Credit Card	Pending
B097	P050	T097	06-05-2023	2835.77	Cash	Failed
B098	P045	T098	17-03-2023	804.26	Credit Card	Paid
B099	P011	T099	04-07-2023	4101.6	Credit Card	Pending
B100	P029	T100	02-03-2023	1551.7	Credit Card	Failed
B101	P036	T101	21-09-2023	2930.05	Credit Card	Paid
B102	P025	T102	25-10-2023	4460.36	Credit Card	Pending
B103	P021	T103	24-01-2023	3428.95	Credit Card	Pending
B104	P036	T104	18-04-2023	2898.31	Credit Card	Failed
B105	P010	T105	14-08-2023	1959.5	Cash	Pending
B106	P037	T106	29-10-2023	1998.51	Credit Card	Paid
B107	P009	T107	17-04-2023	3512.69	Credit Card	Pending
B108	P024	T108	21-04-2023	4973.63	Cash	Paid
B109	P035	T109	29-07-2023	3478.28	Cash	Pending
B110	P049	T110	19-07-2023	3010.03	Cash	Failed
B111	P035	T111	22-05-2023	3787.93	Credit Card	Paid
B112	P048	T112	11-01-2023	2593.43	Insurance	Pending
B113	P036	T113	24-11-2023	770.64	Insurance	Pending
B114	P018	T114	08-08-2023	3030.34	Cash	Pending
B115	P049	T115	25-10-2023	4809.31	Insurance	Paid
B116	P039	T116	07-07-2023	1288.86	Cash	Paid
B117	P032	T117	20-06-2023	3605.02	Credit Card	Paid
B118	P024	T118	09-08-2023	1404.2	Insurance	Failed
B119	P023	T119	18-12-2023	2911.22	Credit Card	Failed
B120	P032	T120	08-12-2023	935.04	Insurance	Paid
B121	P037	T121	07-04-2023	2526.67	Credit Card	Pending
B122	P012	T122	11-07-2023	3902.73	Insurance	Failed
B123	P049	T123	28-02-2023	2064.07	Credit Card	Paid
B124	P013	T124	16-03-2023	3492.1	Credit Card	Pending
B125	P023	T125	18-02-2023	4079.52	Insurance	Failed
B126	P025	T126	02-11-2023	4672.3	Credit Card	Pending
B127	P035	T127	13-11-2023	1555.89	Credit Card	Pending
B128	P041	T128	15-04-2023	2296.92	Credit Card	Pending
B129	P030	T129	25-08-2023	1185.87	Insurance	Pending
B130	P017	T130	23-02-2023	4966.18	Insurance	Failed
B131	P049	T131	11-05-2023	4671.5	Credit Card	Failed
B132	P020	T132	26-07-2023	2929.81	Credit Card	Failed
B133	P048	T133	23-03-2023	4289.15	Insurance	Paid
B134	P025	T134	17-10-2023	2844.31	Insurance	Failed
B135	P022	T135	09-09-2023	3306.14	Credit Card	Pending
B136	P013	T136	13-05-2023	901.06	Credit Card	Failed
B137	P019	T137	25-10-2023	3898.72	Credit Card	Pending
B138	P049	T138	26-12-2023	1074.71	Cash	Paid
B139	P036	T139	10-10-2023	4217.3	Insurance	Pending
B140	P012	T140	05-02-2023	4019.13	Cash	Pending
B141	P041	T141	15-06-2023	3689.35	Insurance	Pending
B142	P019	T142	01-11-2023	662.72	Insurance	Paid
B143	P012	T143	21-09-2023	1864.08	Insurance	Failed
B144	P009	T144	16-08-2023	1684.01	Insurance	Failed
B145	P007	T145	11-11-2023	2120.61	Insurance	Paid
B146	P028	T146	05-01-2023	894.39	Insurance	Pending
B147	P014	T147	13-11-2023	4716.31	Insurance	Failed
B148	P031	T148	06-12-2023	2992.11	Cash	Paid
B149	P019	T149	26-07-2023	1874.86	Credit Card	Failed
B150	P047	T150	16-08-2023	2286.42	Credit Card	Paid
B151	P016	T151	28-01-2023	2512.41	Cash	Pending
B152	P005	T152	14-04-2023	3202.67	Cash	Failed
B153	P035	T153	08-07-2023	2820.56	Cash	Paid
B154	P012	T154	06-03-2023	4637.26	Cash	Failed
B155	P025	T155	03-01-2023	2736.34	Insurance	Failed
B156	P021	T156	22-11-2023	4964.71	Credit Card	Failed
B157	P036	T157	12-05-2023	4331.41	Insurance	Failed
B158	P023	T158	12-07-2023	1438.3	Credit Card	Paid
B159	P016	T159	08-04-2023	4687.68	Credit Card	Pending
B160	P039	T160	17-12-2023	1023.65	Cash	Paid
B161	P045	T161	17-06-2023	4178.52	Insurance	Paid
B162	P042	T162	01-01-2023	2212.8	Cash	Paid
B163	P039	T163	27-06-2023	4450.88	Insurance	Pending
B164	P014	T164	28-07-2023	4406.26	Credit Card	Failed
B165	P031	T165	04-04-2023	4126.66	Cash	Failed
B166	P005	T166	12-01-2023	4055.14	Cash	Failed
B167	P035	T167	15-11-2023	1871.06	Credit Card	Pending
B168	P023	T168	29-09-2023	864.14	Credit Card	Failed
B169	P029	T169	24-07-2023	2313.41	Credit Card	Pending
B170	P043	T170	03-03-2023	1280.86	Cash	Failed
B171	P011	T171	18-04-2023	3627.28	Insurance	Failed
B172	P018	T172	09-03-2023	2057.45	Cash	Paid
B173	P047	T173	04-06-2023	4890.25	Insurance	Pending
B174	P012	T174	31-10-2023	3384.37	Cash	Paid
B175	P009	T175	22-10-2023	4201.16	Cash	Paid
B176	P010	T176	26-04-2023	1096.36	Credit Card	Paid
B177	P044	T177	16-08-2023	4379.07	Insurance	Pending
B178	P017	T178	17-01-2023	4652.41	Cash	Pending
B179	P038	T179	08-03-2023	2691.78	Cash	Failed
B180	P007	T180	07-01-2023	3228.14	Credit Card	Paid
B181	P046	T181	03-09-2023	3941.64	Credit Card	Failed
B182	P013	T182	12-04-2023	1286.77	Insurance	Paid
B183	P040	T183	03-02-2023	2761.55	Cash	Pending
B184	P042	T184	26-02-2023	2293.98	Insurance	Pending
B185	P009	T185	21-03-2023	1158.68	Cash	Pending
B186	P050	T186	27-03-2023	2153.9	Insurance	Paid
B187	P027	T187	13-02-2023	806.78	Credit Card	Pending
B188	P002	T188	12-04-2023	616.15	Cash	Paid
B189	P005	T189	05-10-2023	1108.25	Insurance	Failed
B190	P029	T190	16-11-2023	4834.02	Credit Card	Paid
B191	P037	T191	12-04-2023	2972.88	Credit Card	Failed
B192	P038	T192	31-08-2023	4846.2	Insurance	Paid
B193	P019	T193	15-09-2023	2446.24	Cash	Failed
B194	P008	T194	06-04-2023	1903.17	Cash	Pending
B195	P048	T195	19-08-2023	2777.64	Credit Card	Failed
B196	P045	T196	26-10-2023	2477.8	Cash	Pending
B197	P001	T197	01-04-2023	975.49	Cash	Pending
B198	P022	T198	15-05-2023	3383.72	Cash	Failed
B199	P017	T199	01-05-2023	1472.17	Credit Card	Paid
B200	P007	T200	30-12-2023	3288.15	Insurance	Paid"""

    billing_df = parse_text_data(billing_text,
                               ['bill_id', 'patient_id', 'treatment_id',
                                'bill_date', 'amount', 'payment_method', 'payment_status'])

    # Convert numeric columns to appropriate types
    treatments_df['cost'] = pd.to_numeric(treatments_df['cost'])
    billing_df['amount'] = pd.to_numeric(billing_df['amount'])

    return patients_df, doctors_df, appointments_df, treatments_df, billing_df

# Create dataframes
patients_df, doctors_df, appointments_df, treatments_df, billing_df = create_dataframes()

# ==============================================
# NLP Pipeline Components
# ==============================================

# 1. Preprocessing
def preprocess_text(text):
    """Clean and preprocess input text"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    return text.strip()

# 2. Intent Classification (Naive Bayes implementation)
class NaiveBayesIntentClassifier:
    def __init__(self):
        self.classes = {}
        self.vocab = set()
        self.class_word_counts = defaultdict(lambda: defaultdict(int))
        self.class_total_words = defaultdict(int)

    def train(self, training_data):
        """Train the classifier with sample data"""
        # Sample training data - intent: [example phrases]
        training_examples = {
            'patient_info': [
                'show patient information', 'get patient details', 'patient record',
                'info about patient', 'patient data', 'details for patient',
                'patient history', 'patient profile'
            ],
            'doctor_info': [
                'show doctor information', 'get doctor details', 'doctor record',
                'info about doctor', 'doctor data', 'doctor schedule',
                'doctor availability', 'doctor profile'
            ],
            'appointment_info': [
                'show appointments', 'get appointment details', 'appointment schedule',
                'info about appointments', 'appointment data', 'appointment history',
                'upcoming appointments', 'appointment status'
            ],
            'treatment_info': [
                'show treatments', 'get treatment details', 'treatment records',
                'info about treatments', 'treatment data', 'treatment history',
                'treatment cost', 'treatment types'
            ],
            'billing_info': [
                'show bills', 'get billing details', 'billing records',
                'info about bills', 'billing data', 'payment status',
                'outstanding payments', 'billing history'
            ],
            'general_query': [
                'hello', 'hi', 'help', 'what can you do', 'options',
                'how are you', 'greetings', 'help me'
            ],
            'financial_report': [
                'financial report', 'revenue report', 'income report',
                'payment report', 'revenue summary', 'financial summary',
                'revenue analysis', 'financial analysis'
            ],
            'appointment_stats': [
                'appointment statistics', 'appointment analysis', 'appointment summary',
                'appointment report', 'appointment trends', 'appointment insights'
            ]
        }

        # Build vocabulary and count words
        for intent, examples in training_examples.items():
            self.classes[intent] = len(examples)
            for example in examples:
                words = preprocess_text(example).split()
                for word in words:
                    self.vocab.add(word)
                    self.class_word_counts[intent][word] += 1
                    self.class_total_words[intent] += 1

    def predict(self, text):
        """Predict intent of the input text"""
        words = preprocess_text(text).split()
        best_intent = None
        best_score = float('-inf')

        total_examples = sum(self.classes.values())

        for intent in self.classes:
            # Prior probability
            score = math.log(self.classes[intent] / total_examples)

            # Likelihood for each word
            for word in words:
                word_count = self.class_word_counts[intent].get(word, 0) + 1  # Add-1 smoothing
                total_words = self.class_total_words[intent] + len(self.vocab)
                score += math.log(word_count / total_words)

            if score > best_score:
                best_score = score
                best_intent = intent

        return best_intent

# 3. Entity Recognition (Rule-based)
def extract_entities(text):
    """Extract entities from text using rule-based approach"""
    entities = {}
    text_lower = text.lower()

    # Extract patient IDs
    patient_matches = re.findall(r'p\d{3}', text_lower)
    if patient_matches:
        entities['patient_id'] = patient_matches[0].upper()

    # Extract doctor IDs
    doctor_matches = re.findall(r'd\d{3}', text_lower)
    if doctor_matches:
        entities['doctor_id'] = doctor_matches[0].upper()

    # Extract appointment IDs
    appointment_matches = re.findall(r'a\d{3}', text_lower)
    if appointment_matches:
        entities['appointment_id'] = appointment_matches[0].upper()

    # Extract treatment IDs
    treatment_matches = re.findall(r't\d{3}', text_lower)
    if treatment_matches:
        entities['treatment_id'] = treatment_matches[0].upper()

    # Extract bill IDs
    bill_matches = re.findall(r'b\d{3}', text_lower)
    if bill_matches:
        entities['bill_id'] = bill_matches[0].upper()

    # Extract treatment types
    treatment_types = ['chemotherapy', 'mri', 'ecg', 'x-ray', 'physiotherapy']
    for treatment in treatment_types:
        if treatment in text_lower:
            entities['treatment_type'] = treatment
            break

    # Extract payment status
    payment_statuses = ['paid', 'pending', 'failed']
    for status in payment_statuses:
        if status in text_lower:
            entities['payment_status'] = status
            break

    # Extract appointment status
    appointment_statuses = ['scheduled', 'completed', 'cancelled', 'no-show']
    for status in appointment_statuses:
        if status in text_lower:
            entities['appointment_status'] = status
            break

    # Extract dates
    date_matches = re.findall(r'\d{2}-\d{2}-\d{4}', text)
    if date_matches:
        entities['date'] = date_matches[0]

    # Extract months
    month_matches = re.findall(r'(january|february|march|april|may|june|july|august|september|october|november|december)', text_lower)
    if month_matches:
        entities['month'] = month_matches[0]

    return entities

# 4. Dialogue Manager
class DialogueManager:
    def __init__(self):
        self.context = {}

    def update_context(self, intent, entities):
        """Update dialogue context"""
        self.context.update(entities)
        self.context['last_intent'] = intent

    def get_response(self, intent, entities):
        """Generate response based on intent and entities"""
        self.update_context(intent, entities)

        if intent == 'general_query':
            return self._handle_general_query()
        elif intent == 'patient_info':
            return self._handle_patient_query(entities)
        elif intent == 'doctor_info':
            return self._handle_doctor_query(entities)
        elif intent == 'appointment_info':
            return self._handle_appointment_query(entities)
        elif intent == 'treatment_info':
            return self._handle_treatment_query(entities)
        elif intent == 'billing_info':
            return self._handle_billing_query(entities)
        elif intent == 'financial_report':
            return self._handle_financial_report()
        elif intent == 'appointment_stats':
            return self._handle_appointment_stats()
        else:
            return "I'm not sure how to help with that. Could you please rephrase your question?"

    def _handle_general_query(self):
        return """I'm a Hospital Management Assistant. I can help you with:
- Patient information (e.g., 'show patient P001 details')
- Doctor information (e.g., 'get doctor D002 info')
- Appointment details (e.g., 'show appointments for July')
- Treatment records (e.g., 'show MRI treatments')
- Billing information (e.g., 'get billing details for P005')
- Financial reports (e.g., 'show revenue report')
- Appointment statistics (e.g., 'appointment analysis')

What would you like to know?"""

    def _handle_patient_query(self, entities):
        patient_id = entities.get('patient_id')
        if patient_id:
            patient_data = patients_df[patients_df['patient_id'] == patient_id]
            if not patient_data.empty:
                # Get appointments for this patient
                patient_appointments = appointments_df[appointments_df['patient_id'] == patient_id]
                # Get treatments for this patient
                patient_treatments = treatments_df.merge(
                    appointments_df[appointments_df['patient_id'] == patient_id],
                    on='appointment_id'
                )
                # Get bills for this patient
                patient_bills = billing_df[billing_df['patient_id'] == patient_id]

                response = f"Patient Information:\n{patient_data.to_string(index=False)}\n\n"
                response += f"Appointments for this patient: {len(patient_appointments)}\n"
                response += f"Treatments for this patient: {len(patient_treatments)}\n"
                response += f"Bills for this patient: {len(patient_bills)}"
                return response
            else:
                return f"Patient {patient_id} not found."
        else:
            return "Please specify a patient ID (e.g., P001, P002)."

    def _handle_doctor_query(self, entities):
        doctor_id = entities.get('doctor_id')
        if doctor_id:
            doctor_data = doctors_df[doctors_df['doctor_id'] == doctor_id]
            if not doctor_data.empty:
                # Get appointments for this doctor
                doctor_appointments = appointments_df[appointments_df['doctor_id'] == doctor_id]
                # Calculate statistics
                completed = len(doctor_appointments[doctor_appointments['status'] == 'Completed'])
                scheduled = len(doctor_appointments[doctor_appointments['status'] == 'Scheduled'])
                cancelled = len(doctor_appointments[doctor_appointments['status'] == 'Cancelled'])
                no_show = len(doctor_appointments[doctor_appointments['status'] == 'No-show'])

                response = f"Doctor Information:\n{doctor_data.to_string(index=False)}\n\n"
                response += f"Appointment Statistics:\n"
                response += f"  Total: {len(doctor_appointments)}\n"
                response += f"  Completed: {completed}\n"
                response += f"  Scheduled: {scheduled}\n"
                response += f"  Cancelled: {cancelled}\n"
                response += f"  No-show: {no_show}"
                return response
            else:
                return f"Doctor {doctor_id} not found."
        else:
            return "Please specify a doctor ID (e.g., D001, D002)."

    def _handle_appointment_query(self, entities):
        patient_id = entities.get('patient_id')
        doctor_id = entities.get('doctor_id')
        status = entities.get('appointment_status')

        if patient_id:
            appointment_data = appointments_df[appointments_df['patient_id'] == patient_id]
            if not appointment_data.empty:
                return f"Appointments for Patient {patient_id}:\n{appointment_data.to_string(index=False)}"
            else:
                return f"No appointments found for patient {patient_id}."
        elif doctor_id:
            appointment_data = appointments_df[appointments_df['doctor_id'] == doctor_id]
            if not appointment_data.empty:
                return f"Appointments for Doctor {doctor_id}:\n{appointment_data.to_string(index=False)}"
            else:
                return f"No appointments found for doctor {doctor_id}."
        elif status:
            appointment_data = appointments_df[appointments_df['status'].str.lower() == status.lower()]
            if not appointment_data.empty:
                return f"Appointments with status '{status}':\n{appointment_data.to_string(index=False)}"
            else:
                return f"No appointments found with status '{status}'."
        else:
            return "Recent Appointments:\n" + appointments_df.head(10).to_string(index=False)

    def _handle_treatment_query(self, entities):
        treatment_type = entities.get('treatment_type')
        patient_id = entities.get('patient_id')

        if treatment_type:
            treatment_data = treatments_df[treatments_df['treatment_type'].str.lower() == treatment_type.lower()]
            if not treatment_data.empty:
                return f"{treatment_type.capitalize()} Treatments:\n{treatment_data.to_string(index=False)}"
            else:
                return f"No {treatment_type} treatments found."
        elif patient_id:
            # Get appointments for this patient
            patient_appointments = appointments_df[appointments_df['patient_id'] == patient_id]
            # Get treatments for these appointments
            treatment_data = treatments_df.merge(
                patient_appointments,
                on='appointment_id'
            )
            if not treatment_data.empty:
                return f"Treatments for Patient {patient_id}:\n{treatment_data.to_string(index=False)}"
            else:
                return f"No treatments found for patient {patient_id}."
        else:
            return "Recent Treatments:\n" + treatments_df.head(10).to_string(index=False)

    def _handle_billing_query(self, entities):
        patient_id = entities.get('patient_id')
        status = entities.get('payment_status')

        if patient_id:
            billing_data = billing_df[billing_df['patient_id'] == patient_id]
            if not billing_data.empty:
                total_amount = billing_data['amount'].sum()
                paid_amount = billing_data[billing_data['payment_status'] == 'Paid']['amount'].sum()
                pending_amount = billing_data[billing_data['payment_status'] == 'Pending']['amount'].sum()

                response = f"Billing for Patient {patient_id}:\n{billing_data.to_string(index=False)}\n\n"
                response += f"Financial Summary:\n"
                response += f"  Total Amount: ${total_amount:.2f}\n"
                response += f"  Paid: ${paid_amount:.2f}\n"
                response += f"  Pending: ${pending_amount:.2f}"
                return response
            else:
                return f"No billing records found for patient {patient_id}."
        elif status:
            billing_data = billing_df[billing_df['payment_status'].str.lower() == status.lower()]
            if not billing_data.empty:
                total_amount = billing_data['amount'].sum()
                response = f"Bills with status '{status}':\n{billing_data.to_string(index=False)}\n\n"
                response += f"Total amount: ${total_amount:.2f}"
                return response
            else:
                return f"No bills found with status '{status}'."
        else:
            return "Recent Billing Records:\n" + billing_df.head(10).to_string(index=False)

    def _handle_financial_report(self):
        """Generate a financial report"""
        total_revenue = billing_df[billing_df['payment_status'] == 'Paid']['amount'].sum()
        pending_payments = billing_df[billing_df['payment_status'] == 'Pending']['amount'].sum()
        failed_payments = billing_df[billing_df['payment_status'] == 'Failed']['amount'].sum()

        # Revenue by payment method
        revenue_by_method = billing_df[billing_df['payment_status'] == 'Paid'].groupby('payment_method')['amount'].sum()

        # Revenue by treatment type
        revenue_by_treatment = billing_df.merge(treatments_df, on='treatment_id')
        revenue_by_treatment = revenue_by_treatment[revenue_by_treatment['payment_status'] == 'Paid']
        revenue_by_treatment = revenue_by_treatment.groupby('treatment_type')['amount'].sum()

        response = "Financial Report:\n"
        response += "=" * 50 + "\n"
        response += f"Total Revenue: ${total_revenue:.2f}\n"
        response += f"Pending Payments: ${pending_payments:.2f}\n"
        response += f"Failed Payments: ${failed_payments:.2f}\n\n"

        response += "Revenue by Payment Method:\n"
        for method, amount in revenue_by_method.items():
            response += f"  {method}: ${amount:.2f}\n"

        response += "\nRevenue by Treatment Type:\n"
        for treatment, amount in revenue_by_treatment.items():
            response += f"  {treatment}: ${amount:.2f}\n"

        return response

    def _handle_appointment_stats(self):
        """Generate appointment statistics"""
        total_appointments = len(appointments_df)
        completed = len(appointments_df[appointments_df['status'] == 'Completed'])
        scheduled = len(appointments_df[appointments_df['status'] == 'Scheduled'])
        cancelled = len(appointments_df[appointments_df['status'] == 'Cancelled'])
        no_show = len(appointments_df[appointments_df['status'] == 'No-show'])

        # Appointments by reason
        appointments_by_reason = appointments_df.groupby('reason_for_visit').size()

        # Appointments by doctor
        appointments_by_doctor = appointments_df.merge(doctors_df, on='doctor_id')
        appointments_by_doctor = appointments_by_doctor.groupby(['doctor_id', 'first_name', 'last_name']).size()

        response = "Appointment Statistics:\n"
        response += "=" * 50 + "\n"
        response += f"Total Appointments: {total_appointments}\n"
        response += f"Completed: {completed}\n"
        response += f"Scheduled: {scheduled}\n"
        response += f"Cancelled: {cancelled}\n"
        response += f"No-show: {no_show}\n\n"

        response += "Appointments by Reason:\n"
        for reason, count in appointments_by_reason.items():
            response += f"  {reason}: {count}\n"

        response += "\nAppointments by Doctor:\n"
        for (doc_id, first_name, last_name), count in appointments_by_doctor.items():
            response += f"  {first_name} {last_name} ({doc_id}): {count}\n"

        return response

# 5. Response Generation
def generate_response(user_input):
    """Main function to process user input and generate response"""
    # Preprocessing
    cleaned_input = preprocess_text(user_input)

    # Intent Classification
    intent_classifier = NaiveBayesIntentClassifier()
    intent_classifier.train({})  # Train with sample data

    intent = intent_classifier.predict(user_input)

    # Entity Recognition
    entities = extract_entities(user_input)

    # Dialogue Management
    dialogue_manager = DialogueManager()
    response = dialogue_manager.get_response(intent, entities)

    return response

# ==============================================
# Streamlit App
# ==============================================

def main():
    # Header
    st.markdown("<h1 class='main-header'>🏥 HOSPITAL MANAGEMENT SYSTEM - AI ASSISTANT</h1>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info("This AI assistant helps you query hospital management data including patient records, doctor information, appointments, treatments, and billing.")
        
        st.header("Quick Actions")
        if st.button("Show Financial Report"):
            dialogue_manager = DialogueManager()
            st.text_area("Financial Report", dialogue_manager._handle_financial_report(), height=300)
            
        if st.button("Show Appointment Statistics"):
            dialogue_manager = DialogueManager()
            st.text_area("Appointment Statistics", dialogue_manager._handle_appointment_stats(), height=300)
        
        st.header("Data Overview")
        st.markdown(f"""
        <div class="stats-box">
            <b>Patients:</b> {len(patients_df)} records<br>
            <b>Doctors:</b> {len(doctors_df)} records<br>
            <b>Appointments:</b> {len(appointments_df)} records<br>
            <b>Treatments:</b> {len(treatments_df)} records<br>
            <b>Billing:</b> {len(billing_df)} records
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    st.markdown("### 💬 Chat with the AI Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("Ask a question about hospital data..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        response = generate_response(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Example queries
    st.markdown("---")
    st.markdown("### 💡 Example Queries")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Show patient P001 details"):
            st.session_state.messages.append({"role": "user", "content": "Show patient P001 details"})
            response = generate_response("Show patient P001 details")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
            
    with col2:
        if st.button("Doctor D002 information"):
            st.session_state.messages.append({"role": "user", "content": "Doctor D002 information"})
            response = generate_response("Doctor D002 information")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()cd "C:\Users\abhij\OneDrive\Desktop\sql medical project"; python hospital_ai_assistant.py

            
    with col3:
        if st.button("Appointment statistics"):
            st.session_state.messages.append({"role": "user", "content": "Appointment statistics"})
            response = generate_response("Appointment statistics")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

if __name__ == "__main__":
    main()
