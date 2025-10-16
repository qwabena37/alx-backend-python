# Python Generators – 0x00

## 📌 Objective
This project sets up a MySQL database (`ALX_prodev`) with a `user_data` table and populates it using data from `user_data.csv`.  
It also prepares the environment for using **Python generators** to stream rows one by one from the database.

---

## 📂 Repository Structure
alx-backend-python/
└── python-generators-0x00/
├── 0-main.py
├── seed.py
├── user_data.csv
└── README.md

---

## ⚙️ Features
- Connect to MySQL server
- Create database `ALX_prodev` if it does not exist
- Create `user_data` table with the following fields:
  - `user_id` (UUID, Primary Key, Indexed)  
  - `name` (VARCHAR, NOT NULL)  
  - `email` (VARCHAR, NOT NULL)  
  - `age` (DECIMAL, NOT NULL)  
- Insert sample data from `user_data.csv` (avoiding duplicates)

---

## Usage
1. **Install dependencies**  
   ```bash
   pip freeze > requirements.txt
   ```

2. **Run the script***
   ```bash
   python 0-main.py
   ```
      