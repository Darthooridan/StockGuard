# StockGuard API 📦

A robust REST API for warehouse inventory management.
Designed to handle stock tracking, product management, and automated alerts for low inventory.

## 🚀 About the Project
As a Logistics Team Leader with years of experience in warehouse operations, I noticed that efficient inventory tracking is key to avoiding bottlenecks. I built **StockGuard** to simulate a backend system that solves real-world logistics problems:
- Preventing stockouts (low stock alerts).
- Ensuring data integrity (strict input validation).
- Managing product lifecycle (CRUD operations).

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI (High performance, easy to document)
* **Database:** SQLite (SQLAlchemy ORM)
* **Validation:** Pydantic models
* **Testing:** Manual testing via Swagger UI

## ⚙️ Features
* **Product Management:** Create, Read, Update, Delete (CRUD) items.
* **Data Persistence:** SQLite database integration ensures data is saved securely.
* **Input Validation:** Prevents bad data entry (e.g., negative prices or missing names).
* **Interactive Documentation:** Auto-generated Swagger UI.

## 📦 How to Run
1. Clone the repository:
    Bash
    git clone [https://github.com/Darthooridan/StockGuard.git](https://github.com/Darthooridan/StockGuard.git)
2. Create virtual environment:

    Bash

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:

    Bash

    pip install fastapi "uvicorn[standard]" sqlalchemy
4. Run the server:

    Bash

    uvicorn main:app --reload
5. Open documentation: Go to http://127.0.0.1:8000/docs