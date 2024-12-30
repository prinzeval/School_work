CREATE DATABASE Autoshop;

USE Autoshop;

CREATE TABLE Operations_Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    phone_num VARCHAR(30) UNIQUE,
    address VARCHAR(80)
);

CREATE TABLE Operations_Vehicle (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    make VARCHAR(10) NOT NULL,
    model VARCHAR(10) NOT NULL,
    year INT,
    colour VARCHAR(10),
    VIN VARCHAR(20) UNIQUE,
    plate_num VARCHAR(10) UNIQUE,
    mileage DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES Operations_Customer(customer_id) ON DELETE CASCADE
);

CREATE TABLE Operations_Technician (
    technician_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    specialty VARCHAR(100),
    hourly_rate DECIMAL(10,2) CHECK (hourly_rate >= 0)
);

CREATE TABLE Operations_Part (
    part_id INT AUTO_INCREMENT PRIMARY KEY,
    part_name VARCHAR(50) NOT NULL,
    part_num VARCHAR(15) UNIQUE,
    unit_price DECIMAL(10,2) CHECK (unit_price >= 0),
    stock_quantity INT CHECK (stock_quantity >= 0)
);

CREATE TABLE Operations_Job (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    technician_id INT,
    job_type VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    job_amount DECIMAL(10,2) CHECK (job_amount >= 0),
    hours INT CHECK (hours >= 0),
    status ENUM('In Progress', 'Completed') DEFAULT 'In Progress',
    FOREIGN KEY (vehicle_id) REFERENCES Operations_Vehicle(vehicle_id) ON DELETE CASCADE,
    FOREIGN KEY (technician_id) REFERENCES Operations_Technician(technician_id) ON DELETE CASCADE
);


CREATE TABLE Operations_JobPart (
    jobpart_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    part_id INT NOT NULL,
    quantity_part_used INT CHECK (quantity_part_used >= 0),
    part_amount DECIMAL(10,2) CHECK (part_amount >= 0),
    total_cost DECIMAL(10,2) CHECK (total_cost >= 0),
    FOREIGN KEY (job_id) REFERENCES Operations_Job(job_id) ON DELETE CASCADE,
    FOREIGN KEY (part_id) REFERENCES Operations_Part(part_id) ON DELETE CASCADE
);


CREATE TABLE Operations_Invoice (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    jobpart_id INT NOT NULL,
    issued_date DATE NOT NULL,
    sales_tax DECIMAL(10,2) CHECK (sales_tax >= 0),
    total_amount DECIMAL(10,2) CHECK (total_amount >= 0),
    payment_status VARCHAR(10) DEFAULT 'Unpaid',
    FOREIGN KEY (jobpart_id) REFERENCES Operations_JobPart(jobpart_id) ON DELETE CASCADE
);



CREATE TABLE Analytics_Date (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    day INT CHECK (day > 0 AND day < 32),
    month INT CHECK (month > 0 AND month < 13),
    year INT
);

CREATE TABLE Analytics_Sales (
    sales_id INT AUTO_INCREMENT PRIMARY KEY,
    revenue DECIMAL(20, 2) NOT NULL,
    cost DECIMAL(20, 2) NOT NULL,
    profit DECIMAL(20, 2) GENERATED ALWAYS AS (revenue - cost) STORED,
    duration INT NOT NULL,
    date_id INT NOT NULL,
    job_id INT NOT NULL,
    part_id INT,
    customer_id INT,
    technician_id INT,
    jobpart_id INT,
    FOREIGN KEY (date_id) REFERENCES Analytics_Date(date_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES Operations_Job(job_id) ON DELETE CASCADE,
    FOREIGN KEY (part_id) REFERENCES Operations_Part(part_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Operations_Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (technician_id) REFERENCES Operations_Technician(technician_id) ON DELETE CASCADE,
    FOREIGN KEY (jobpart_id) REFERENCES Operations_JobPart(jobpart_id) ON DELETE CASCADE
);

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Store hashed passwords
    role ENUM('Admin', 'Technician') NOT NULL
);


show tables;

--DATA INSERTS

INSERT INTO Operations_Customer (customer_id, name, email, phone_num, address)
VALUES 
 (1, 'John Doe', 'john.doe@example.com', '1234567890', '123 Main St'),
(2, 'Jane Smith', 'jane.smith@example.com', '0987654321', '456 Oak Ave'),
(3, 'Bob Brown', 'bob.brown@example.com', '1122334455', '789 Pine Ln' ),
(4, 'Alice Green', 'alice.green@example.com', '6677889900', '321 Maple Dr'),
(5, 'Eve White', 'eve.white@example.com', '4433221100', '654 Birch Rd');

INSERT INTO Operations_Vehicle (vehicle_id, customer_id, make, model, year, colour, VIN, plate_num, mileage)
VALUES 
(1, 1, 'Toyota', 'Camry', 2015, 'Red', 'VIN1234567890', 'ABC123', 75000),
(2, 2, 'Honda', 'Civic', 2018, 'Blue', 'VIN0987654321', 'XYZ456', 45000),
(3, 3, 'Ford', 'Focus', 2017, 'Black', 'VIN1122334455', 'DEF789', 60000),
(4, 4, 'Nissan', 'Altima', 2019, 'White', 'VIN6677889900', 'GHI012', 30000),
(5, 5, 'Chevrolet', 'Malibu', 2020, 'Gray', 'VIN4433221100', 'JKL345', 20000);

INSERT INTO Operations_Technician (technician_id, name, specialty, hourly_rate)
VALUES 
(1, 'Sam Wilson', 'Engine Repair', 50.00),
(2, 'Tom Hardy', 'Transmission', 55.00),
(3, 'Lucy Liu', 'Paint & Bodywork', 60.00),
(4, 'Chris Evans', 'Suspension', 45.00),
(5, 'Tony Stark', 'Electrical Systems', 70.00);

INSERT INTO Operations_Part (part_id, part_name, part_num, unit_price, stock_quantity)
VALUES 
(1, 'Brake Pads', 'BP123', 25.50, 100),
(2, 'Oil Filter', 'OF456', 10.75, 200),
(3, 'Battery', 'BT789', 120.00, 50),
(4, 'Air Filter', 'AF012', 15.00, 150),
(5, 'Spark Plugs', 'SP345', 30.00, 75);

INSERT INTO Operations_Job (job_id, vehicle_id, technician_id, job_type, start_date, end_date, job_amount, hours)
VALUES 
(1, 1, 1, 'Brake Replacement', '2024-12-01', '2024-12-02', 150.00, 3),
(2, 2, 2, 'Oil Change', '2024-12-03', NULL, 50.00, 1),
(3, 3, 3, 'Battery Replacement', '2024-12-04', '2024-12-04', 180.00, 2),
(4, 4, 4, 'Suspension Adjustment', '2024-12-05', '2024-12-06', 250.00, 4),
(5, 5, 5, 'Electrical Diagnostics', '2024-12-07', NULL, 300.00, 5);

INSERT INTO Operations_JobPart (jobpart_id, job_id, part_id, quantity_part_used, part_amount, total_cost)
VALUES 
(1, 1, 1, 2, 50.00, 200.00),
(2, 2, 2, 1, 10.75, 60.75),
(3, 3, 3, 1, 120.00, 300.00),
(4, 4, 4, 2, 30.00, 350.00),
(5, 5, 5, 4, 120.00, 420.00);

INSERT INTO Operations_Invoice (invoice_id, jobpart_id, issued_date, sales_tax, total_amount, payment_status)
VALUES 
(01, 1, '2024-12-02', 10.00, 210.00, 'Paid'),
(02, 2, '2024-12-03', 5.00, 65.75, 'Unpaid'),
(03, 3, '2024-12-04', 15.00, 315.00, 'Paid'),
(04, 4, '2024-12-06', 20.00, 370.00, 'Unpaid'),
(05, 5, '2024-12-07', 25.00, 445.00, 'Paid');

INSERT INTO Analytics_Date (date_id, date, day, month, year)
VALUES 
(2, '2024-12-02', 2, 12, 2024),
(3, '2024-12-03', 3, 12, 2024),
(4, '2024-12-04', 4, 12, 2024),
(5, '2024-12-05', 5, 12, 2024),
(6, '2024-12-06', 6, 12, 2024);


INSERT INTO Analytics_Sales (sales_id, revenue, cost, duration, date_id, job_id, part_id, customer_id, technician_id, jobpart_id)
VALUES 
(1, 210.00, 100.00, 3, 2, 1, 1, 1, 1, 1),
(2, 65.75, 30.00, 1, 3, 2, 2, 2, 2, 2),
(3, 315.00, 150.00, 2, 4, 3, 3, 3, 3, 3),
(4, 370.00, 200.00, 4, 5, 4, 4, 4, 4, 4),
(5, 445.00, 220.00, 5, 6, 5, 5, 5, 5, 5);

SELECT * FROM Operations_Customer;
SELECT * FROM Operations_Vehicle;
SELECT * FROM Operations_Technician;
SELECT * FROM Operations_Part;
SELECT * FROM Operations_Job;
SELECT * FROM Operations_JobPart;
SELECT * FROM Operations_Invoice;
SELECT * FROM Analytics_Date;
SELECT * FROM Analytics_Sales;


-- DELETE FROM Operations_Customer WHERE customer_id =  1;

-- ALTER TABLE analytics_sales
-- ADD CONSTRAINT fk_customer
-- FOREIGN KEY (CustomerID)
-- REFERENCES customer_table(CustomerID)
-- ON DELETE CASCADE
-- ON UPDATE CASCADE;

-- ALTER TABLE analytics_sales
-- ADD CONSTRAINT fk_product
-- FOREIGN KEY (ProductID)
-- REFERENCES products(ProductID)
-- ON DELETE SET NULL
-- ON UPDATE CASCADE;

------------------------------------------------------------------------------
--BACKEND QUERIES
------------------------------------------------------------------------------


--customer_enqiries v1
WITH name_plate_num(Customer_Name, Plate_Number) AS
    (SELECT DISTINCT C.name,  V.plate_num
    FROM operations_customer AS C
    JOIN operations_vehicle AS V ON C.customer_id = V.customer_id),
mech_job(Enquiry_date, Problem_Description, Technician_Assigned, Plate_Number) AS
    (SELECT J.start_date, J.job_type, T.name,  V.plate_num
    FROM operations_job AS J
    JOIN Operations_Technician AS T ON J.technician_id = T.technician_id
    JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id)
SELECT Customer_Name, NPN.Plate_Number AS Plate_Number, Enquiry_date, Problem_Description, Technician_Assigned
FROM name_plate_num AS NPN
JOIN mech_job AS MJ ON NPN.Plate_Number = MJ.Plate_Number;

--customer_enqiries v2
SELECT C.name AS Customer_Name, V.plate_num AS Plate_Number, J.start_date AS Enquiry_Date, J.job_type AS Problem_Description, T.name AS Mechanic
FROM operations_customer AS C
JOIN operations_vehicle AS V ON C.customer_id = V.customer_id
JOIN operations_job AS J ON V.vehicle_id = J.vehicle_id
JOIN Operations_Technician AS T on J.technician_id = T.technician_id;

--customer_invoice
SELECT C.name AS Customer_Name, P.part_name AS Part_Used, JP.quantity_part_used AS Number_of_Parts_Used, JP.part_amount AS Part_Amount, J.job_amount AS Job_Amount, JP.total_cost AS Total_Cost 
FROM operations_jobpart AS JP
JOIN operations_job AS J ON J.job_id = JP.job_id
JOIN operations_part AS P ON P.part_id = JP.part_id
JOIN operations_vehicle AS V ON V.vehicle_id = J.vehicle_id
JOIN operations_customer AS C ON C.customer_id = V.customer_id;

--DROPING part_num NOT NECESSARY
ALTER TABLE operations_part
DROP COLUMN part_num;

--Job queries
SELECT C.name AS Customer_Name, V.make AS Make, V.plate_num AS Plate_Number, J.job_type AS Problem_Description, J.start_date AS Start_date, J.hours AS Hours, J.job_amount AS Job_Amount
FROM operations_job  AS J
JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
JOIN operations_customer AS C ON V.customer_id = C.customer_id
WHERE J.status = 'In progress';

SELECT C.name AS Customer_Name, V.make AS Make, V.plate_num AS Plate_Number, J.job_type AS Problem_Description, J.start_date AS Start_date, J.end_date AS End_date, J.hours AS Hours, J.job_amount AS Job_Amount
FROM operations_job  AS J
JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
JOIN operations_customer AS C ON V.customer_id = C.customer_id
WHERE J.status = 'Completed';

UPDATE operations_job AS J
    JOIN operations_customer AS C ON J.customer_id = C.customer_id
    JOIN operations_vehicle AS V ON V.vehicle_id = J.vehicle_id
SET technician_id = (
        SELECT technician_id
        FROM operations_technician
        WHERE name = %s
        LIMIT 1
    )
WHERE C.name = %s
    AND V.plate_num = %s
    AND J.job_type = %s;

UPDATE operations_job AS J
    JOIN operations_technician AS T ON J.technician_id = T.technician_id
    JOIN operations_vehicle AS V ON V.vehicle_id = J.vehicle_id
SET J.status = %s, J.end_date = %s
WHERE V.plate_num = %s
      AND J.job_type = %s
      AND T.name = %s;

INSERT INTO Operations_Job(vehicle_id, job_type, start_date) VALUES
( (SELECT vehicle_id
    FROM Operations_Vehicle
    WHERE plate_num = %s), %s, %s );

INSERT INTO Operations_Vehicle (customer_id, make, model, year, colour, VIN, plate_num, mileage, image) VALUES 
((SELECT customer_id
    FROM operations_customer
    WHERE customer_name = %s), %s, %s, %s, %s, %s, %s, %s, %s);    

INSERT INTO Operations_Invoice (invoice_id, jobpart_id, issued_date, sales_tax) VALUES
(%s, %s, %s, %s);

UPDATE operations_invoice SET payment_status = %s WHERE invoice_id = %s;

SELECT I.invoice_id, C.name AS Customer_Name, C.address AS Address, I.issued_date AS Issued_Date, V.make AS Make, V.model AS Model,
V.year AS Year, V.colour AS Colour, V.VIN, V.plate_num AS Plate_Number, V.mileage AS Mileage, J.job_type AS Job_Performed,
JP.quantity_part_used AS No_of_Parts_Used, JP.part_amount AS Part_Price, J.job_amount AS Labour, I.sales_tax AS Sales_Tax, 
I.total_amount AS Total_amount, I.payment_status AS Payment_Status
FROM operations_invoice  AS I
JOIN operations_jobpart AS JP ON I.jobpart_id = JP.jobpart_id
JOIN operations_job AS J ON JP.job_id = J.job_id
JOIN operations_part AS P ON JP.part_id = P.part_id
JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
JOIN operations_customer AS C ON V.customer_id = C.customer_id;

SELECT I.invoice_id, C.name AS Customer_Name, C.address AS Address, I.issued_date AS Issued_Date, V.make AS Make, V.model AS Model,
V.year AS Year, V.colour AS Colour, V.VIN, V.plate_num AS Plate_Number, V.mileage AS Mileage, J.job_type AS Job_Performed,
JP.quantity_part_used AS No_of_Parts_Used, JP.part_amount AS Part_Price, J.job_amount AS Labour, I.sales_tax AS Sales_Tax, 
I.total_amount AS Total_amount, I.payment_status AS Payment_Status
FROM operations_invoice  AS I
JOIN operations_jobpart AS JP ON I.jobpart_id = JP.jobpart_id
JOIN operations_job AS J ON JP.job_id = J.job_id
JOIN operations_part AS P ON JP.part_id = P.part_id
JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
JOIN operations_customer AS C ON V.customer_id = C.customer_id
WHERE I.payment_status = "Unpaid";

SELECT I.invoice_id, C.name AS Customer_Name, C.address AS Address, I.issued_date AS Issued_Date, V.make AS Make, V.model AS Model,
V.year AS Year, V.colour AS Colour, V.VIN, V.plate_num AS Plate_Number, V.mileage AS Mileage, J.job_type AS Job_Performed,
JP.quantity_part_used AS No_of_Parts_Used, JP.part_amount AS Part_Price, J.job_amount AS Labour, I.sales_tax AS Sales_Tax, 
I.total_amount AS Total_amount, I.payment_status AS Payment_Status
FROM operations_invoice  AS I
JOIN operations_jobpart AS JP ON I.jobpart_id = JP.jobpart_id
JOIN operations_job AS J ON JP.job_id = J.job_id
JOIN operations_part AS P ON JP.part_id = P.part_id
JOIN operations_vehicle AS V ON J.vehicle_id = V.vehicle_id
JOIN operations_customer AS C ON V.customer_id = C.customer_id
WHERE I.payment_status = "paid";