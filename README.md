# Hospital Management System – AI Assistant

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/) 
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) 
[![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/) 
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)


---

## Table of Contents
- [Project Overview](#-features)   
- [Features](#-features)  
- [Tech Stack](#-tech-stack)  
- [Installation](#-installation)  
- [Usage](#-usage)  
- [Database Schema](#-database-schema)  
- [Analytics & Insights](#-analytics--insights)  
- [AI Capabilities](#-ai-capabilities)  
- [Screenshots](#-screenshots)  
- [Future Enhancements](#-future-enhancements)  
- [Contributing](#-contributing)  
- [License](#-license)  

---

## Project Overview
Our hypothetical healthcare company aims to revolutionize patient care through AI-driven solutions while eliminating 40+ hours of weekly manual reporting. The goal is to deploy an intelligent AI automation platform that transforms raw healthcare data into actionable insights, predictive analytics, and automated business intelligence.

---

## Features

### AI-Powered Interface
- Natural Language Processing (NLP) for hospital queries  
- Intent Recognition (classify queries into categories)  
- Entity Extraction (auto-detect patient IDs, doctor IDs, treatments)  
- Contextual Responses with multi-turn dialogue support
<img width="1919" height="866" alt="Screenshot 2025-09-16 120654" src="https://github.com/user-attachments/assets/25df7469-d1ad-4563-a986-7a6bffd63526" />



### Comprehensive Data Management
- Patient Management (demographics & insurance)  
- Doctor Profiles (specialization & experience)  
- Appointment Scheduling (status, visit reason, follow-ups)  
- Treatments with Cost Tracking  
- Billing System (methods & payment status)  

### Advanced Analytics
- Financial Reports by treatment & payment method  
- Appointment Statistics (scheduled vs completed vs cancelled)  
- Patient Registration Trends  
- Doctor Performance & workload analysis  

### User Experience
- Interactive **chat interface**  
- **Quick action sidebar** for instant reports  
- Responsive design for desktop & mobile  
- **Real-time data responses**  

---

## 🛠 Tech Stack
| Component       | Technology |
|-----------------|------------|
| **Frontend**    | Streamlit |
| **Backend**     | Python 3.8+ |
| **Data**        | Pandas, NumPy |
| **NLP Engine**  | Custom Naive Bayes Classifier |
| **Database**    | MySQL |
| **Visualization** | Streamlit charts |

---

---

## Objectives
- Build a normalized relational **hospital database**  
- Implement an **AI-driven NLP query system**  
- Deliver **analytics for decision-making**  
- Provide a **user-friendly interface** via Streamlit  

---

## 3️Database Design
### Core Entities
- Patients  
- Doctors  
- Appointments  
- Treatments  
- Billing  
**Relationships:**  
- A Patient → can have multiple Appointments  
- An Appointment → links to a Doctor & Treatment  
- A Treatment → generates a Billing entry  

---

## AI Capabilities
- **NLP Engine** → Naive Bayes intent classifier  
- **Entity Recognition** → detects IDs & keywords  
- **Dialogue Management** → context-aware conversation  
- **Supported Intents:**  
  - Patient info  
  - Doctor info  
  - Appointment details  
  - Billing queries  
  - Financial analysis  
  - Statistics  
---
## Usage
- **Example Queries**
- **Patients** → "Show patient P001 details"

- **Doctors** → "Doctor D002 information"

- **Appointments** → "Show appointments for July"

- **Finance** → "Revenue analysis for treatments"

## Quick Actions

- **Use the sidebar for**
- **✔ Financial reports**
- **✔ Appointment statistics**
- **✔ Registration trends**
- **✔ Revenue analysis**

## Database Schema
**Key Tables**

- **Patients** → demographic, insurance info

- **Doctors** → specialization, contact, experience

- **Appointments** → scheduling, status

- **Treatments** → type, description, cost

- **Billing** → payment processing

- **Relational ER diagram:**
<img width="1200" height="744" alt="Screenshot 2025-09-12 180503" src="https://github.com/user-attachments/assets/2e3733fd-09e4-40c5-bfd9-865a0674821d" />

---

##  Analytics & Insights
### Q1:What is the trend of new patient and registrations over time?
 Identifies **trend of patient and registrations** 
```
SELECT DATE_FORMAT(registration_date, '%Y-%m') AS month,
       COUNT(*) AS new_patients
FROM Patients
GROUP BY month
ORDER BY month
limit 10;
```
<img width="954" height="237" alt="Screenshot 2025-09-12 174710" src="https://github.com/user-attachments/assets/f3e7be99-4f6b-4c9d-b1e8-99b8ad7f161e" />
---

### Q2: Doctor Workload
 Identifies **most-consulted doctors** for better scheduling.
 
```
SELECT d.doctor_id, d.first_name, d.last_name, d.specialization,
       COUNT(a.appointment_id) AS total_appointments
FROM Doctors d
LEFT JOIN Appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
ORDER BY total_appointments DESC;
```
<img width="945" height="273" alt="Screenshot 2025-09-12 175126" src="https://github.com/user-attachments/assets/8f08ac22-8e8e-4ab9-8f8f-8dcb38e587a3" />

### Q3: Treatment Revenue
 Shows **most profitable treatments** for hospital strategy. 
```
SELECT t.treatment_type, SUM(b.amount) AS total_revenue
FROM Treatments t
JOIN Billing b ON t.treatment_id = b.treatment_id
GROUP BY t.treatment_type
ORDER BY total_revenue DESC;
```
<img width="673" height="178" alt="Screenshot 2025-09-12 175519" src="https://github.com/user-attachments/assets/fb287291-153b-4127-a289-494c7097f1d9" />


### Q4: Billing Patterns
 Evaluates **payment methods & defaults**.
```
SELECT 
    payment_method,
    COUNT(*) AS total_bills,
    SUM(CASE WHEN payment_status = 'Paid' THEN 1 ELSE 0 END) AS paid_count,
    SUM(CASE WHEN payment_status = 'Pending' OR payment_status = 'Default' THEN 1 ELSE 0 END) AS unpaid_count,
    ROUND(SUM(CASE WHEN payment_status = 'Pending' OR payment_status = 'Default' THEN amount ELSE 0 END), 2) AS total_unpaid_amount,
    ROUND(AVG(amount), 2) AS avg_bill_amount
FROM Billing
GROUP BY payment_method
ORDER BY total_bills DESC;
```
<img width="769" height="209" alt="Screenshot 2025-09-12 180131" src="https://github.com/user-attachments/assets/446284e1-cf81-4b2f-b82b-950600ff003d" />


### Q5: Appointment Trends
 Tracks no-shows, cancellations, completion rates.
```
SELECT status, COUNT(*) AS total
FROM Appointments
GROUP BY status;
```
<img width="677" height="144" alt="Screenshot 2025-09-12 175729" src="https://github.com/user-attachments/assets/035aafe4-9da7-4f09-ad2c-1b47d6ed74c4" />

---

##  Results & Findings
- Hospital growth can be visualized using **patient registration trends**.  
- **Doctors with higher appointment loads** may need support staff.  
- Treatments vary in demand, highlighting **cost-effective services**.  
- Billing shows **clear payment preferences** (e.g., insurance > cash).  
- No-show analysis can reduce **resource wastage**.  

---

##  Conclusion
This system is not only a **data management tool** but also a **decision-support system**.  

- For **Administrators** → provides financial, staffing, and patient insights.  
- For **Doctors** → shows workload, treatment success trends.  
- For **Data Analysts** → offers structured datasets for deeper BI/ML.  

- Combines **Database + AI + Analytics** → delivering **real-world healthcare value**.  

---

##  Future Enhancements
- Integration with **Electronic Health Records (EHR)**  
- AI-driven **predictive analytics** (demand, patient inflow)  
- **Mobile-first app** for doctors/patients  
- **Voice assistants** for query handling  
- **Blockchain** for secure medical records

---
##  Acknowledgments

- **Streamlit team for the framework**

- **Pandas/Numpy community**

- **Healthcare professionals for domain expertise**

- **Open-source community**
---
## 👨‍💻 Author
**Abhijeet Kanse**  
- 📧 Email: abhijeetkanse@33gmail.com
- 🌐 [GitHub Profile](https://github.com/Abhijeet-Kanse)
- ⭐ If you like this project, give it a star on GitHub!
---
