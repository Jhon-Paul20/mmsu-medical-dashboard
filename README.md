# MMSU Medical Dashboard

A web-based medical personnel dashboard for managing health records, built with Flask and modern web technologies.

![Dashboard Preview](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)

## Features

- 🔐 Secure login system
- 📊 Interactive data visualizations with Chart.js
- 🩺 Medical condition tracking
- 🔍 Advanced filtering and search
- 📁 CSV data import/export
- 📱 Responsive design
- 🎨 Modern dark-themed UI

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### Default Login Credentials

- **Username:** `admin`
- **Password:** `mmsu2024`

⚠️ **Important:** Change these credentials before deploying to production!

## Usage

### Uploading Data

The dashboard accepts CSV files with the following format:

```csv
name,gender,blood,department,conditions
John Doe,Male,O+,CHS,Diabetes|Hypertension
Jane Smith,Female,A+,COE,None
```

**CSV Columns:**
- `name` - Full name of the personnel
- `gender` - Male/Female
- `blood` - Blood type (e.g., O+, A-, AB+)
- `department` - Department code (CHS, COE, CBEA, CAS, CTE)
- `conditions` - Medical conditions separated by `|` (pipe character)

### Features Overview

1. **Dashboard View** - View statistics, charts, and personnel overview
2. **Filter by Condition** - Click on conditions in the sidebar to filter
3. **Search** - Search by name or department
4. **Personnel Details** - Click on any record to view detailed information
5. **CSV Upload** - Upload new data via the upload button

## Deployment

### Deploy to Python Anywhere

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files or clone from GitHub
3. Create a new web app (Flask)
4. Set up virtual environment:
```bash
mkvirtualenv --python=/usr/bin/python3.10 mmsu-env
pip install -r requirements.txt
```
5. Configure WSGI file to point to your app
6. Reload the web app

### Deploy to Heroku

1. Install Heroku CLI
2. Create a `Procfile`:
```
web: gunicorn app:app
```
3. Add gunicorn to requirements.txt
4. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Deploy to Render

1. Sign up at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`

## Security Recommendations

Before deploying to production:

1. **Change Admin Credentials** - Update username/password in `app.py`
2. **Use Environment Variables** - Store credentials in `.env` file:
```python
import os
from dotenv import load_dotenv

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
```
3. **Enable HTTPS** - Always use SSL certificates in production
4. **Database Security** - Consider using PostgreSQL instead of SQLite
5. **Rate Limiting** - Add Flask-Limiter to prevent brute force attacks

## Project Structure

```
mmsu-medical-dashboard/
├── app.py              # Flask backend application
├── index.html          # Main dashboard interface
├── login.html          # Login page
├── requirements.txt    # Python dependencies
├── mmsu.db            # SQLite database (auto-generated)
└── README.md          # This file
```

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Charts:** Chart.js
- **CSV Parsing:** PapaParse.js
- **Database:** SQLite
- **Fonts:** Google Fonts (Figtree, Instrument Serif)

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please contact the development team or create an issue in the repository.

---

**Made for MMSU Medical Department** 🏥
