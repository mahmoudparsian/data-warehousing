-- ---------------------------
-- source table: source_table
-- ---------------------------
CREATE TABLE source_table (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    country VARCHAR(20),
    salary INT
);

-- ---------------------------
-- source table: continents
-- ---------------------------
CREATE TABLE continents (
    continent VARCHAR(30),
    country   VARCHAR(20),
    PRIMARY KEY (country)
);

-- -------------------------------
-- target table: destination_table
-- -------------------------------
CREATE TABLE destination_table (
    id INT,
    name VARCHAR(50),
    age INT,
    country VARCHAR(20),
    salary INT,
    tax INT,
    continent VARCHAR(20)
);

-- -------------------------------
-- POPULATE continents table: 
-- -------------------------------
INSERT INTO continents (continent, country) 
VALUES
('North America', 'USA'),
('North America', 'CANADA'),
('North America', 'MEXICO'),
('Europe', 'GERMANY'),
('Europe', 'FRANCE'),
('Europe', 'ITALY'),
('Asia', 'JAPAN'),
('Asia', 'CHINA'),
('Asia', 'INDIA');

-- -------------------------------
-- POPULATE source_table:
-- -------------------------------
INSERT INTO source_table (name, age, country, salary) 
VALUES
-- =========================
-- USA (34 rows)
-- =========================
('Alice Johnson', 30, 'USA', 52000),
('George Smith', 40, 'USA', 82000),
('Charlie Brown', 35, 'USA', 71000),
('Chuck Wilson', 45, 'USA', 90000),
('Emily Davis', 29, 'USA', 48000),
('Michael Lee', 50, 'USA', 105000),
('Sarah Miller', 34, 'USA', 68000),
('Daniel Moore', 41, 'USA', 85000),
('Laura Taylor', NULL, 'USA', 62000),
('James Anderson', 38, 'USA', 76000),
('Sophia Thomas', 27, 'USA', 45000),
('Robert Jackson', 46, 'USA', 93000),
('Olivia White', 31, 'USA', 59000),
('William Harris', NULL, 'USA', 88000),
('Emma Martin', 36, 'USA', 72000),
('Ethan Thompson', 33, 'USA', 65000),
('Mia Garcia', 28, 'USA', NULL),
('Alexander Martinez', 42, 'USA', 91000),
('Isabella Robinson', 39, 'USA', 83000),
('Benjamin Clark', 44, 'USA', 95000),
('Amelia Rodriguez', 26, 'USA', 43000),
('Logan Lewis', 37, 'USA', 74000),
('Charlotte Walker', 32, 'USA', 61000),
('Henry Hall', 48, 'USA', 98000),
('Ava Allen', NULL, 'USA', 56000),
('Sebastian Young', 35, 'USA', 70000),
('Ella Hernandez', 29, 'USA', 52000),
('Matthew King', 52, 'USA', 110000),
('Grace Wright', 34, 'USA', 66000),
('Joseph Lopez', 41, 'USA', 87000),
('Lily Scott', 27, 'USA', 46000),
('David Green', 45, 'USA', NULL),
('Natalie Adams', 38, 'USA', 78000),
('Ryan Baker', 31, 'USA', 60000),

-- =========================
-- CANADA (33 rows)
-- =========================
('Bob Martin', NULL, 'CANADA', 60000),
('Betty Clark', NULL, 'CANADA', 50000),
('Barb Wilson', 50, 'CANADA', 42000),
('Babak Rahimi', 45, 'CANADA', 20000),
('Daniel Nguyen', 39, 'CANADA', 78000),
('Sophie Tremblay', 34, 'CANADA', 69000),
('Marc Dupont', 47, 'CANADA', 88000),
('Isabelle Moreau', 29, 'CANADA', 52000),
('Lucas Pelletier', 41, 'CANADA', 83000),
('Chantal Roy', 36, 'CANADA', 71000),
('Pierre Gagnon', 52, 'CANADA', 96000),
('Nina Patel', 31, 'CANADA', 64000),
('Arjun Singh', NULL, 'CANADA', 75000),
('Fatima Khan', 28, 'CANADA', 48000),
('Mohammed Ali', 44, 'CANADA', 89000),
('Olga Ivanova', 37, 'CANADA', 72000),
('Victor Chen', 35, 'CANADA', 68000),
('Hannah Brooks', 33, 'CANADA', 61000),
('Kevin OConnor', 49, 'CANADA', 92000),
('Julia Bennett', 27, 'CANADA', 46000),
('Andre Leblanc', 42, 'CANADA', 85000),
('Mei Lin', 30, 'CANADA', NULL),
('Ravi Sharma', 38, 'CANADA', 77000),
('Sarah McDonald', 45, 'CANADA', 88000),
('Tom Fraser', 51, 'CANADA', 97000),
('Anita Desai', 34, 'CANADA', 69000),
('Paul Johnson', 40, 'CANADA', 81000),
('Emily Wong', 29, 'CANADA', 54000),
('Carlos Mendez', NULL, 'CANADA', 62000),
('Laura Stein', 36, 'CANADA', 73000),
('George Petrov', 48, 'CANADA', 91000),
('Monica Rossi', 32, 'CANADA', 65000),
('Ahmed Hassan', 43, 'CANADA', NULL),

-- =========================
-- MEXICO (33 rows)
-- =========================
('Jeb Carter', NULL, 'MEXICO', 30000),
('Jason Morales', NULL, 'MEXICO', 50000),
('David Ramirez', 28, 'MEXICO', NULL),
('Rafael Ortega', 38, 'MEXICO', NULL),
('Luis Hernandez', 41, 'MEXICO', 62000),
('Ana Lopez', 29, 'MEXICO', 45000),
('Carlos Gutierrez', 35, 'MEXICO', 57000),
('Maria Sanchez', 33, 'MEXICO', 52000),
('Jorge Alvarez', 47, 'MEXICO', 74000),
('Patricia Flores', 39, 'MEXICO', 61000),
('Miguel Torres', 51, 'MEXICO', 82000),
('Lucia Rios', 27, 'MEXICO', 43000),
('Fernando Castillo', 44, 'MEXICO', 78000),
('Carmen Vega', NULL, 'MEXICO', 49000),
('Oscar Mendoza', 36, 'MEXICO', 56000),
('Daniela Cruz', 31, 'MEXICO', 53000),
('Ricardo Navarro', 48, 'MEXICO', 80000),
('Sofia Pineda', 26, 'MEXICO', 41000),
('Antonio Reyes', 42, 'MEXICO', 69000),
('Paola Jimenez', 34, 'MEXICO', 58000),
('Hector Salazar', 45, 'MEXICO', 76000),
('Veronica Luna', 37, 'MEXICO', 60000),
('Eduardo Fuentes', 50, 'MEXICO', 83000),
('Martha Delgado', 32, 'MEXICO', 54000),
('Raul Ibarra', 40, 'MEXICO', 67000),
('Claudia Romero', NULL, 'MEXICO', 52000),
('Julio Vargas', 28, 'MEXICO', 46000),
('Natalia Acosta', 35, 'MEXICO', 59000),
('Pablo Cortes', 46, 'MEXICO', 77000),
('Adriana Molina', 30, 'MEXICO', NULL),
('Roberto Nunez', 52, 'MEXICO', 85000),
('Silvia Bravo', 34, 'MEXICO', 56000),
('Ivan Soto', 41, 'MEXICO', 71000),

-- =========================
-- INDIA (10 rows)
-- =========================
('Amit Sharma', 34, 'INDIA', 42000),
('Priya Patel', 29, 'INDIA', 38000),
('Rahul Verma', 41, 'INDIA', 55000),
('Neha Gupta', 27, 'INDIA', 36000),
('Sanjay Mehta', 45, 'INDIA', 62000),
('Anita Iyer', 38, 'INDIA', 48000),
('Vikram Singh', NULL, 'INDIA', 51000),
('Pooja Nair', 31, 'INDIA', NULL),
('Rohit Khanna', 36, 'INDIA', 47000),
('Kavita Rao', 42, 'INDIA', 58000),

-- =========================
-- GERMANY (15 rows)
-- =========================
('Hans Müller', 45, 'GERMANY', 72000),
('Anna Schmidt', 34, 'GERMANY', 58000),
('Thomas Weber', 50, 'GERMANY', 85000),
('Julia Fischer', 29, 'GERMANY', 52000),
('Markus Becker', 41, 'GERMANY', 69000),
('Sabine Hoffmann', 38, 'GERMANY', 64000),
('Stefan Klein', NULL, 'GERMANY', 76000),
('Laura Wagner', 33, 'GERMANY', 59000),
('Michael Braun', 47, 'GERMANY', 81000),
('Claudia Richter', 35, 'GERMANY', 61000),
('Andreas Neumann', 52, 'GERMANY', 90000),
('Katrin Wolf', 28, 'GERMANY', 50000),
('Peter König', 44, 'GERMANY', NULL),
('Monika Schulte', 39, 'GERMANY', 67000),
('Daniel Vogt', 31, 'GERMANY', 56000),

-- =========================
-- CHINA (18 rows)
-- =========================
('Li Wei', 34, 'CHINA', 52000),
('Wang Fang', 29, 'CHINA', 46000),
('Zhang Yong', 41, 'CHINA', 68000),
('Liu Yan', 27, 'CHINA', 43000),
('Chen Ming', 38, 'CHINA', 60000),
('Yang Jie', 45, 'CHINA', 75000),
('Zhao Lin', NULL, 'CHINA', 58000),
('Huang Qiang', 36, 'CHINA', 62000),
('Wu Xia', 31, 'CHINA', 49000),
('Zhou Peng', 48, 'CHINA', 80000),
('Xu Na', 26, 'CHINA', 42000),
('Sun Tao', 52, 'CHINA', 83000),
('Ma Li', 35, 'CHINA', NULL),
('He Jun', 39, 'CHINA', 67000),
('Gao Rui', 44, 'CHINA', 72000),
('Lin Hong', 33, 'CHINA', 54000),
('Deng Lei', NULL, 'CHINA', 61000),
('Cai Ying', 28, 'CHINA', 45000);
