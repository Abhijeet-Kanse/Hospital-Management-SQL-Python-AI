#--- Create Database ---
DROP DATABASE IF EXISTS Hospital_Management_System;
CREATE DATABASE IF NOT EXISTS Hospital_Management_System;
USE Hospital_Management_System;

#-- Patients Table
DROP TABLE IF EXISTS Patients;
CREATE TABLE Patients (
    patient_id VARCHAR(20) PRIMARY KEY,          -- e.g. P001, P000123
    first_name VARCHAR(50),                      -- First name
    last_name VARCHAR(50),                       -- Last name
    gender CHAR(1),                              -- M/F
    date_of_birth DATE,                          -- Stored as YYYY-MM-DD
    contact_number BIGINT,                       -- Phone number (up to 10-15 digits)
    address VARCHAR(255),                        -- Street address
    registration_date DATE,                      -- Stored as YYYY-MM-DD
    insurance_provider VARCHAR(100),             -- Company name
    insurance_number VARCHAR(50),                -- Policy number
    email VARCHAR(100)                           -- Email address
);

#-- Doctors Table
DROP TABLE IF EXISTS Doctors;
CREATE TABLE Doctors (
    doctor_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    specialization VARCHAR(100),
    phone_number BIGINT NOT NULL,
    years_experience INT NOT NULL,
    hospital_branch VARCHAR(150),
    email VARCHAR(200) UNIQUE
);

#-- Appointments Table
DROP TABLE IF EXISTS Appointments;
CREATE TABLE Appointments (
    appointment_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),
    doctor_id VARCHAR(50),
    appointment_date DATE,
    appointment_time TIME,
    reason_for_visit VARCHAR(200),
    status VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

#-- Treatments Table
DROP TABLE IF EXISTS Treatments;
CREATE TABLE Treatments (
    treatment_id VARCHAR(50) PRIMARY KEY,
    appointment_id VARCHAR(50),
    treatment_type VARCHAR(100),
    description VARCHAR(500),
    cost DECIMAL(10,2),
    treatment_date DATE,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(appointment_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

#-- Billing Table
DROP TABLE IF EXISTS Billing;
CREATE TABLE Billing (
    bill_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),
    treatment_id VARCHAR(50),
    bill_date DATE,
    amount DECIMAL(10,2),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (treatment_id) REFERENCES Treatments(treatment_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

SET FOREIGN_KEY_CHECKS = 0;
SET FOREIGN_KEY_CHECKS = 1;


select *  from Patients;
select *  from Doctors;
select *  from Appointments;
select *  from Treatments;
select * from Billing;

show tables ;


#What is the trend of patient registrations over time?-- 
SELECT DATE_FORMAT(registration_date, '%Y-%m') AS month,
       COUNT(*) AS new_patients
FROM Patients
GROUP BY month
ORDER BY month
limit 10;

#Which doctors have the highest number of appointments?
SELECT d.doctor_id, d.first_name, d.last_name, d.specialization,
       COUNT(a.appointment_id) AS total_appointments
FROM Doctors d
LEFT JOIN Appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
ORDER BY total_appointments DESC;

#What is the appointment no-show rate?
SELECT status, COUNT(*) AS total
FROM Appointments
GROUP BY status;

#Which treatments generate the most revenue?
SELECT t.treatment_type, SUM(b.amount) AS total_revenue
FROM Treatments t
JOIN Billing b ON t.treatment_id = b.treatment_id
GROUP BY t.treatment_type
ORDER BY total_revenue DESC;

#What is the average patient lifetime value (LTV)?
SELECT p.patient_id, p.first_name, p.last_name,
       SUM(b.amount) AS total_spent
FROM Patients p
LEFT JOIN Billing b ON p.patient_id = b.patient_id
GROUP BY p.patient_id, p.first_name, p.last_name
ORDER BY total_spent DESC
limit 10;

#Which insurance providers cover the most patients?
SELECT insurance_provider, COUNT(*) AS total_patients
FROM Patients
GROUP BY insurance_provider
ORDER BY total_patients DESC
limit 5;


#Which doctors have the highest number of appointments?
SELECT d.doctor_id,
       CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
       COUNT(a.appointment_id) AS total_appointments
FROM Doctors d
LEFT JOIN Appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, doctor_name
ORDER BY total_appointments DESC
LIMIT 5;

#What is the revenue trend per month?
SELECT DATE_FORMAT(bill_date, '%Y-%m') AS month,
       SUM(amount) AS total_revenue
FROM Billing
GROUP BY month
ORDER BY month
limit 5;

#Billing Patterns - Payment Methods & Defaults
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

-- Conclusion

-- The Hospital Management System (HMS) project successfully demonstrates how relational databases and SQL queries can be applied to manage, analyze, and optimize healthcare data.

-- Database Design & Relationships

-- The database schema included key entities such as Patients, Doctors, Appointments, Treatments, and Billing.

-- Proper use of Primary Keys, Foreign Keys, and cascading constraints (ON UPDATE CASCADE, ON DELETE CASCADE) ensured data integrity and maintained consistent relationships between tables.

-- Data Management & Chronology

-- Patient records, appointments, and billing entries were imported and stored chronologically, allowing meaningful time-based insights such as monthly new patient trends and revenue tracking.

-- Normalization reduced redundancy and made the data scalable and efficient for future hospital needs.

-- SQL Queries & Business Insights

-- Analytical queries provided actionable insights, for example:

-- Tracking monthly new patient registrations.

-- Identifying top doctors by appointment volume.

-- Analyzing most common treatments and procedures.

-- Generating billing and revenue reports to support financial planning.

-- Real-world Value

-- For hospital administrators → helps in resource allocation (doctors, staff, medicines).

-- For doctors → assists in understanding patient flow and treatment trends.

-- For management → provides data-driven decision-making for operational and financial strategies.

-- Future Scope

-- Integration with AI/ML models for predictive analytics (e.g., forecasting patient inflow).

-- Developing a user-friendly dashboard (Power BI / Tableau) for real-time visualization.

-- Adding NLP-based assistants for patient queries and appointment scheduling.

-- Implementing security measures (role-based access, encryption) for compliance with healthcare data regulations (HIPAA, etc.).

-- ✅ Final Note:
-- This project not only highlights technical expertise in SQL and database design but also shows the ability to derive practical business insights in the healthcare domain. It demonstrates how data-driven systems can significantly improve hospital efficiency, patient care, and financial performance.







