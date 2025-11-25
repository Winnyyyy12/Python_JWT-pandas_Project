# Python JWT-Pandas Project  
A modern backend project powered by Python, JWT authentication, and Pandas for workbook automation and data processing.

---

## 🌟 Overview  
This project brings together clean API design, secure login flow and workbook-based project estimation tools.

**Core focuses:**
- JWT-based authentication  
- Modular API routers  
- XLSX handling using Pandas  
- Structured, scalable backend architecture

---

## 📂 Project Structure  
.
├── auth/ # JWT handling and auth dependencies
├── routers/ # All REST API routers (auth, projects, logs, templates, etc.)
├── sheets/ # Excel sheet logic (deliverables, cost, timeline, SOW summary)
├── templates/ # XLSX workbook templates
├── utils/ # Logging, Excel utilities, CRUD helpers
├── database.py # DB session/engine
├── database_url.py # Database configuration
├── models.py # ORM data models
├── main.py # App entry file
├── requirements.txt # Python dependencies
└── Sample estimation XLSX files (.xlsx)

yaml
Copy code

---

## 🚀 Getting Started

### 1️⃣ Clone the repo
bash
git clone https://github.com/Winnyyyy12/Python_JWT-pandas_Project.git
cd Python_JWT-pandas_Project
### 2️⃣ Create a virtual environment
bash
Copy code
python -m venv venv
Activate it:

#### Windows

bash
Copy code
.\venv\Scripts\activate
Linux/Mac

bash
Copy code
source venv/bin/activate
### 3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
### 4️⃣ Configure the database
Edit database_url.py:

python
Copy code
DATABASE_URL = "postgresql://user:password@host:port/dbname"
### 5️⃣ Run the application
bash
Copy code
python main.py
Now open your browser or Postman and hit:

bash
Copy code
/auth/login
/projects
/logs
### 🔐 Authentication Flow
User logs in via /auth/login

Server returns a JWT token

Protected routes require:

makefile
Copy code
Authorization: Bearer <token>
Middleware verifies token on each request

User context is injected into route handlers

### 📊 Excel & Pandas Workflow
The app automates reading and writing XLSX project estimation sheets.

Templates stored in templates/

Logic lives in sheets/

#### Examples include:

sheets/sow_summary.py

sheets/resource_timeline_plan.py

sheets/infra_cost.py

#### Typical workflow:

Load template workbook

Process data with Pandas

Generate summaries, cost estimations, deliverables, etc.

Export results

### ✨ Features
JWT authentication

Organized REST API design

Automated Excel processing

Error logging & utilities built in

Easy to extend with new modules

### 📅 Future Improvements
User role system

Async backend (FastAPI or aio stack)

React/Vue frontend

Docker & CI/CD support

Full test suite (unit + integration)

### 🙋 Contributing
Pull requests are welcome!

Please:

Follow existing project structure

Use snake_case

Prefer modular additions

Add tests for new utilities

### 📝 Notes
Built for Python 3.13

If cross-platform contributors appear, standardize CRLF/LF via .gitattributes

Avoid committing large output XLSX files when possible

