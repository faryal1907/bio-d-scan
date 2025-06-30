# PROJECT STRUCTURE

bio-d-sca/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── api.py
│   ├── requirements.txt
│   └── README.md
├── bio-d-scan (frontend)/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── BeeDataForm.js
│   │   │   └── BeeDataTable.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── .gitignore
└── README.md

in backend:
python -m uvicorn app.main:app --reload

to activate venv:
.\venv\Scripts\Activate.ps1

to test database connection:
python -c "from app.database import test_connection; import asyncio; asyncio.run(test_connection())"
