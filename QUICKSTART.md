# Quick Start Guide

## Installation Steps

1. **Install Python packages**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Configure Database**
   - Copy `.env.example` to `.env`
   - Edit `.env` with your MySQL credentials
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASS=your_password
   DB_NAME=hotel_db
   ```

3. **Create Database**
   Open MySQL and run:
   ```sql
   CREATE DATABASE hotel_db;
   ```

4. **Run Setup**
   ```powershell
   python setup.py
   ```
   This will:
   - Check dependencies
   - Test database connection
   - Create tables
   - Create admin user (username: admin, password: admin123)

5. **Start Application**
   ```powershell
   python -m app.main
   ```

## First Login
- Username: `admin`
- Password: `admin123`

**Important:** Change the admin password after first login!

## Testing
```powershell
pytest
```

## Troubleshooting

### Import Errors
If you see "Import could not be resolved" errors, run:
```powershell
pip install -r requirements.txt
```

### Database Connection Failed
- Ensure MySQL is running
- Check credentials in `.env` file
- Verify database exists

### Module Not Found
Run from the project root directory:
```powershell
python -m app.main
```
Not:
```powershell
python app/main.py
```
