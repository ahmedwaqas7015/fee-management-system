# Setup Instructions - Fee Management System

## Prerequisites

- Python 3.8 or higher installed
- pip (Python package manager)
- A code editor (VS Code, PyCharm, etc.)

## Step-by-Step Setup

### 1. Check Python Installation

```bash
python --version
# Should show Python 3.8 or higher
```

If Python is not installed, download from https://www.python.org/

### 2. Navigate to Project Directory

```bash
cd /home/logixsy/learning/tasks/fms
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

**What is this?**
- Creates an isolated Python environment
- Keeps project dependencies separate
- Prevents conflicts with other projects

### 4. Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On Linux/Mac:**
```bash
source venv/bin/activate
```

**How to know it's activated?**
- You'll see `(venv)` at the start of your command prompt
- Example: `(venv) C:\Users\...`

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

**What does this do?**
- Installs all required Python packages
- Takes a few minutes (downloads packages)
- Creates a complete development environment

### 6. Initialize Database

**Option 1: Using Python script (Recommended)**
```bash
python init_db.py
```

**Option 2: Using Flask CLI**
```bash
# Set Flask app location
export FLASK_APP=run.py
flask init-db
```

**What does this do?**
- Creates the SQLite database file in `instance/fms.db`
- Creates all database tables
- Creates admin user:
  - Username: `admin`
  - Password: `admin123`

**Important:** Change the password after first login!

### 7. Run the Application

```bash
python run.py
```

**What happens?**
- Flask development server starts
- You'll see: `Running on http://127.0.0.1:5000`
- Application is now running!

### 8. Open in Browser

Open your web browser and go to:
```
http://127.0.0.1:5000
```

You should see the login page!

### 9. Login

Use the default credentials:
- **Username:** `admin`
- **Password:** `admin123`

After login, you'll see the dashboard.

---

## Troubleshooting

### Problem: "python: command not found"
**Solution:** Use `python3` instead of `python`

### Problem: "pip: command not found"
**Solution:** Install pip or use `python -m pip`

### Problem: "Module not found" errors
**Solution:** 
1. Make sure virtual environment is activated
2. Run `pip install -r requirements.txt` again

### Problem: "Port 5000 already in use"
**Solution:**
1. Find what's using port 5000: `lsof -i :5000` (Linux/Mac) or `netstat -ano | findstr :5000` (Windows)
2. Kill that process or change port in `run.py`

### Problem: "Database not found"
**Solution:** Run `flask init-db` to create the database

### Problem: "Template not found"
**Solution:** Check that all template files are in correct folders

---

## Development Workflow

### Daily Development

1. **Activate virtual environment**
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Make code changes**
   - Edit files in your code editor
   - Flask auto-reloads on changes (if debug=True)

3. **Test changes**
   - Refresh browser
   - Check for errors in terminal

4. **Deactivate when done** (optional)
   ```bash
   deactivate
   ```

---

## Project Structure Overview

```
fms/
├── app/              # Main application code
├── instance/         # Database file (created automatically)
├── logs/            # Log files (created automatically)
├── backups/         # Database backups
├── media/           # Uploaded files
├── config.py        # Configuration
├── run.py           # Start application
└── requirements.txt # Dependencies
```

---

## Next Steps

After setup is complete:
1. Read `PHASE1_TEACHING_GUIDE.md` to understand what we built
2. Explore the code structure
3. Try logging in and navigating
4. Ready for Phase 2: Database Models

---

## Getting Help

If you encounter issues:
1. Check error messages carefully
2. Read the troubleshooting section
3. Check Flask documentation
4. Review the teaching guide

**Happy coding!** 🚀
