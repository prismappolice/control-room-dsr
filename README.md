# Control Room DSR Management System

A comprehensive web application for managing Daily Status Reports (DSR) across 28 districts and control room operations. Built with Flask, SQLAlchemy, and Bootstrap for a modern, responsive experience.

## Features

### 🏛️ Multi-District Management
- **28 Districts Support**: Individual login credentials for each district
- **Centralized Administration**: Single admin panel for all districts
- **Control Room Integration**: Separate interface for control room operations

### 📝 Comprehensive Reporting
- **16 Different Report Forms**: Covering all aspects of daily operations
  - Crime Report
  - CCTV Report  
  - Traffic Report
  - Law & Order
  - Cyber Crime Report
  - Women Safety
  - Narcotics Report
  - VIP Security
  - Missing Persons
  - Arms & Ammunition
  - Vehicle Theft
  - Public Grievances
  - Training Programs
  - Community Policing
  - Emergency Services
  - Special Operations

### 👥 User Authentication & Authorization
- **Three User Types**: Admin, District User, Control Room
- **Secure Login System**: Password-protected access
- **Role-based Permissions**: Different access levels for each user type

### 📊 Admin Dashboard Features
- **District Overview**: Visual grid of all 28 districts
- **Form Management**: Access to all 16 report forms
- **Search Functionality**: Date and district-wise DSR search
- **Excel Export**: Download reports in Excel format
- **Real-time Statistics**: Today's entries, total districts, active forms

### 🏢 District User Features
- **Form Entry Interface**: User-friendly form filling
- **Data Validation**: Client and server-side validation
- **Auto-save Functionality**: Prevent data loss
- **Edit/Delete Options**: Modify or remove entries
- **Date Selection**: Historical data entry support

### 🏗️ Control Room Operations
- **File Upload System**: Support for PDF, Excel, Word documents
- **Three Upload Categories**:
  - Periscope reports
  - VIP Engagements
  - 334PS RTM&E-Sakshya documents
- **Drag & Drop Interface**: Modern file upload experience
- **File Management**: View and download uploaded files

### 📈 Data Export & Analysis
- **Excel Generation**: Automated Excel report creation
- **Date-wise Filtering**: Filter reports by specific dates
- **District-wise Grouping**: Organize data by district
- **Comprehensive Formatting**: Professional Excel styling

## Technology Stack

### Backend
- **Flask 2.3.3**: Web framework
- **SQLAlchemy 2.0+**: Database ORM
- **Flask-Login 0.6.3**: User session management
- **Flask-WTF 1.2.1**: Form handling and CSRF protection
- **PostgreSQL**: Production-grade database

### Frontend
- **Bootstrap 5.1.3**: Responsive UI framework
- **Font Awesome 6.0.0**: Icon library
- **Custom CSS**: Modern styling and animations
- **JavaScript**: Dynamic interactions and form validation

### Data Processing
- **Pandas 2.1.4**: Data manipulation
- **OpenPyXL 3.1.2**: Excel file generation
- **JSON**: Data storage and API responses

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone/Download the Project**
   ```bash
   git clone https://github.com/prismappolice/control-room-dsr.git
   cd control-room-dsr
   ```

2. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/
   - Create database and user (see DEPLOYMENT.md for details)

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   python run.py
   ```

6. **Access the System**
   - Open your web browser
   - Navigate to: `http://localhost:5000`
   - Use the default credentials below

## Default Login Credentials

### Administrator
- **Username**: `admin`
- **Password**: `admin123`

### Control Room
- **Username**: `controlroom` 
- **Password**: `controlroom123`

### District Users
Each district has a username based on its name:
- **Format**: `{district_name_lowercase_with_underscores}`
- **Password**: `{district_name_lowercase_with_underscores}123`

**Examples**:
- Srikakulam: `srikakulam` / `srikakulam123`
- Visakhapatnam: `visakhapatnam` / `visakhapatnam123`
- East Godavari: `east_godavari` / `east_godavari123`

## Project Structure

```
control room DSR/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models and form configurations
│   ├── routes.py                # Application routes and logic
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Custom styles
│   │   └── js/
│   │       └── script.js        # JavaScript functionality
│   ├── templates/
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Landing page
│   │   ├── login.html           # Login page
│   │   ├── admin/
│   │   │   ├── dashboard.html   # Admin dashboard
│   │   │   ├── district_view.html # District-specific view
│   │   │   └── form_view.html   # Form-specific view
│   │   └── district/
│   │       ├── dashboard.html   # District dashboard
│   │       ├── form_entry.html  # Form entry interface
│   │       ├── controlroom_dashboard.html # Control room dashboard
│   │       └── upload.html      # File upload interface
│   └── uploads/                 # Uploaded files storage
├── .github/
│   └── copilot-instructions.md  # Project instructions
├── .vscode/
│   └── tasks.json              # VS Code tasks
├── requirements.txt            # Python dependencies
├── run.py                     # Application entry point
└── README.md                  # This file
```

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password`: Hashed password
- `user_type`: admin/district/controlroom
- `district_name`: District name (for district users)
- `is_active`: Account status
- `created_at`: Account creation timestamp

### DSREntry Table
- `id`: Primary key
- `district_name`: District name
- `form_type`: Type of report form
- `date`: Report date
- `data`: JSON data of form fields
- `user_id`: Foreign key to users
- `created_at`: Entry creation timestamp
- `updated_at`: Last modification timestamp

### ControlRoomUpload Table
- `id`: Primary key
- `date`: Upload date
- `upload_type`: periscope/vip_engagements/ps_rtm
- `filename`: System filename
- `original_filename`: Original filename
- `file_path`: Full file path
- `user_id`: Foreign key to users
- `uploaded_at`: Upload timestamp

## API Endpoints

### Authentication
- `GET /` - Landing page
- `GET/POST /auth/login` - Login page
- `GET /auth/logout` - Logout

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/district/<district_name>` - District view
- `GET /admin/form/<form_type>` - Form view
- `GET /admin/search` - DSR search API
- `GET /admin/download_dsr/<district>/<date>` - Excel download

### District Routes
- `GET /district/dashboard` - District dashboard
- `GET /district/controlroom_dashboard` - Control room dashboard
- `GET/POST /district/form/<form_type>` - Form entry
- `GET/POST /district/upload` - File upload
- `GET /district/delete_entry/<entry_id>` - Delete entry

## Form Configurations

Each of the 16 forms is configured with specific fields:

### Crime Report
- Total Cases Registered
- Cases Solved
- Arrests Made
- Property Recovered (Value)
- Remarks

### CCTV Report
- Total CCTV Cameras
- Working Cameras
- Non-Working Cameras
- Cameras Requiring Maintenance
- Remarks

### Traffic Report
- Road Accidents
- Fatalities
- Injuries
- Challans Issued
- Fine Collected (Amount)
- Remarks

*[Similar configurations for all 16 forms]*

## Security Features

- **Password Hashing**: Werkzeug security for password protection
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Session Management**: Flask-Login secure sessions
- **File Upload Security**: Secure filename handling and type validation
- **SQL Injection Protection**: SQLAlchemy ORM parameterized queries
- **XSS Prevention**: Jinja2 template auto-escaping

## Customization Options

### Adding New Districts
1. Update the `DISTRICTS` list in `models.py`
2. Create user account via admin or database
3. System automatically supports new district

### Adding New Forms
1. Add form configuration to `FORM_CONFIGS` in `models.py`
2. Define field types and labels
3. Form automatically appears in all interfaces

### Cloud Deployment
For cloud deployment instructions, see `DEPLOYMENT.md`:
- Render (Free tier available)
- Railway.app
- DigitalOcean
- AWS/Azure/GCP

### File Upload Configuration
- **Supported Formats**: PDF, Excel (.xlsx, .xls), Word (.docx, .doc)
- **File Size Limit**: 16MB (configurable in `__init__.py`)
- **Storage Location**: `app/uploads/` directory

## Development Guidelines

### Running in Development Mode
The application runs in debug mode by default when using `python run.py`. This enables:
- Automatic code reloading
- Detailed error messages
- Interactive debugger

### Production Deployment
For production deployment:
1. Set `debug=False` in `run.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure a reverse proxy (Nginx, Apache)
4. Set up proper database (MySQL, PostgreSQL)
5. Configure environment variables for sensitive data

### Contributing
1. Follow PEP 8 coding standards
2. Add comments for complex logic
3. Test all new features thoroughly
4. Update documentation for changes

## Troubleshooting

### Common Issues

**Database Errors**:
- Check PostgreSQL service is running
- Verify database credentials in .env file
- Ensure database exists and user has proper permissions

**Import Errors**:
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility

**Port Issues**:
- If port 5000 is busy, modify the port in `run.py`
- Use `python run.py` and check terminal output for the correct URL

**File Upload Issues**:
- Ensure `app/uploads/` directory exists and is writable
- Check file size limits and formats

### Getting Help
- Check the Flask documentation: https://flask.palletsprojects.com/
- Review SQLAlchemy docs: https://docs.sqlalchemy.org/
- Bootstrap documentation: https://getbootstrap.com/docs/

## License

This project is developed for internal use by the Police Department. All rights reserved.

## Version History

- **v1.0.0** (2025-11-04): Initial release
  - Complete DSR management system
  - 28 districts support
  - 16 report forms
  - Admin and district user interfaces
  - Control room file upload functionality
  - Excel export capabilities

---

**Note**: This system is designed to be deployed internally within the department's network. Ensure proper security measures are in place before deployment.