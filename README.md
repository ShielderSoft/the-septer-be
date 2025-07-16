# The Septer Backend 🛡️

A sophisticated cyber forensics and log analysis platform powered by AI. The Septer backend provides secure authentication, file upload capabilities, and AI-powered log analysis using Google's Gemini API.

## 🔍 Overview

The Septer backend is designed for cybersecurity professionals to analyze logs and detect malicious activities. It features two user roles:
- **Hunters**: Analysts who upload logs and ask questions about potential security threats
- **Guardians**: Administrators who can view user statistics and manage the platform

## 🚀 Features

### Authentication & Security
- JWT-based authentication system
- AES-256 encryption for password storage
- Strong password requirements (8+ chars, uppercase, lowercase, digits, special characters)
- Role-based access control (Hunter/Guardian)

### Log Analysis
- Support for multiple log formats: `.txt`, `.log`, `.json`, `.sarif`
- File upload with size validation (configurable max size)
- AI-powered analysis using Google Gemini API
- Structured responses with insights, reasoning, supporting logs, and security fixes

### User Management
- User registration and login
- Gemini API key management per user
- Guardian dashboard with user statistics
- Conversation history tracking

### Data Models
- **Users**: Email, encrypted password, role, Gemini API key
- **Logs**: File metadata and storage paths
- **Conversations**: Q&A history with structured AI responses

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy with SQLite (configurable)
- **Authentication**: JWT with python-jose
- **Encryption**: AES-256-CBC with PBKDF2
- **AI Integration**: Google Generative AI (Gemini)
- **File Handling**: Python-multipart
- **Validation**: Pydantic with email validation

## 📁 Project Structure

```
the-septer-be/
├── main.py                 # FastAPI application entry point
├── add_guardian.py         # Utility script to add Guardian users
├── requirements.txt        # Python dependencies
├── septer.db              # SQLite database file
├── uploaded_logs/         # Directory for uploaded log files
├── api/                   # API route handlers
│   ├── auth.py           # Authentication endpoints
│   ├── guardian.py       # Guardian-specific endpoints
│   ├── hunter.py         # Hunter user management
│   └── logs.py           # Log upload and analysis
├── core/                  # Core application modules
│   ├── config.py         # Configuration settings
│   ├── db.py             # Database connection and session management
│   └── security.py       # JWT, encryption, and security utilities
├── models/                # SQLAlchemy data models
│   ├── user.py           # User model with roles
│   ├── log.py            # Log file metadata
│   └── conversation.py   # Q&A conversation history
├── schemas/               # Pydantic schemas for API validation
│   ├── user.py           # User-related schemas
│   ├── ai.py             # AI query and response schemas
│   └── log.py            # Log-related schemas
└── services/              # Business logic services
    ├── ai_handler.py     # Gemini AI integration
    ├── file_upload.py    # File handling utilities
    └── file_parser.py    # Log file parsing
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd the-septer-be
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   Create a `.env` file in the root directory:
   ```env
   DB_URL=sqlite:///septer.db
   JWT_SECRET=your-super-secret-jwt-key-here
   GEMINI_API_BASE=https://generativelanguage.googleapis.com
   MAX_FILE_SIZE_MB=10
   
   # AES Encryption Keys (generate secure hex values)
   SEPTER_AES_SECRET=your-aes-secret-passphrase
   SEPTER_AES_SALT=746869735f69735f73616c74  # hex encoded
   SEPTER_AES_IV_BASE=69765f626173655f63686172  # hex encoded
   ```

5. **Initialize database and create Guardian user**
   ```bash
   python add_guardian.py
   ```

### Running the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Authentication Endpoints

#### POST `/api/auth/login`
Login with email and password
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Hunter Endpoints

#### POST `/api/hunter/signup`
Register a new Hunter user
```json
{
  "email": "hunter@example.com",
  "password": "SecurePass123!",
  "role": "Hunter"
}
```

#### PUT `/api/hunter/add-api-key`
Add Gemini API key for the authenticated user
```json
{
  "api_key": "your-gemini-api-key"
}
```

### Guardian Endpoints

#### GET `/api/guardian/dashboard`
Get platform statistics and user details (Guardian only)

### Log Analysis Endpoints

#### POST `/api/logs/upload`
Upload a log file for analysis
- Form data with `log_type` (txt/log/json/sarif) and `file`

#### POST `/api/logs/ask`
Ask a question about an uploaded log
```json
{
  "log_id": "uuid-of-uploaded-log",
  "question": "Are there any signs of brute force attacks in this log?"
}
```

## 🔒 Security Features

### Password Security
- AES-256-CBC encryption with PBKDF2 key derivation
- 100,000 iterations for key strengthening
- Unique salt and IV for each encryption
- Strong password policy enforcement

### Authentication
- JWT tokens with configurable expiration
- Role-based access control
- Secure token validation for all protected endpoints

### File Security
- File size validation
- Secure file storage with UUID naming
- Support for multiple log formats with validation

## 🤖 AI Integration

The platform integrates with Google's Gemini AI to provide intelligent log analysis:

### Analysis Structure
- **🔍 Insights**: Key findings and potential threats
- **🧠 Reasoning**: Detailed analysis methodology
- **📄 Supporting Logs**: Specific log lines with explanations
- **🛠️ Fixes**: Recommended security measures and mitigations

### Supported Log Formats
- Text logs (`.txt`, `.log`)
- JSON structured logs (`.json`)
- SARIF security reports (`.sarif`)

## 🔧 Configuration

### Environment Variables
- `DB_URL`: Database connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `GEMINI_API_BASE`: Gemini API base URL
- `MAX_FILE_SIZE_MB`: Maximum file upload size
- `SEPTER_AES_*`: Encryption configuration

### Database Configuration
The application uses SQLAlchemy with SQLite by default but can be configured for PostgreSQL, MySQL, or other databases by updating the `DB_URL`.

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Set secure values for all secrets
2. **Database**: Use a production database (PostgreSQL recommended)
3. **CORS**: Update CORS origins to specific frontend domains
4. **File Storage**: Consider cloud storage for uploaded files
5. **SSL/TLS**: Use HTTPS in production
6. **Rate Limiting**: Implement API rate limiting
7. **Monitoring**: Add logging and monitoring tools

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/
```

## 📈 Monitoring & Logging

The application includes comprehensive error handling and can be integrated with monitoring solutions like:
- Prometheus for metrics
- ELK stack for logging
- Sentry for error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is proprietary software. All rights reserved.

## 🆘 Support

For support and questions, please contact the development team or create an issue in the repository.

---

**The Septer Backend** - Empowering cybersecurity professionals with AI-driven log analysis capabilities.