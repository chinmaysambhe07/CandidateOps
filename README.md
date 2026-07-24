# 🚀 CandidateOps

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/yourusername/CandidateOps/actions)

🤖 **Automated candidate tracking system for SAP Career portal** – streamline recruitment by fetching candidate data, updating Excel tracking sheets, and downloading attachments.

---

## 📋 Overview

CandidateOps is a production‑quality web crawling tool designed for HR professionals and hiring managers to automate the tedious process of tracking candidates from SAP Career portal. The application:

- 🔐 Authenticates to SAP Career portal using SSO credentials  
- 🎯 Navigates to specific job positions  
- 📥 Extracts candidate information and application data  
- 📊 Updates Excel tracking spreadsheets with new & updated candidate information  
- 📎 Downloads candidate resumes, cover letters, and other attachments  
- 📂 Organizes downloaded files in a structured folder system  
- 🔁 Monitors for new applications in continuous mode  
- 📝 Provides detailed logging and error handling  

---

## 🌟 Features

- **🔌 SAP Integration** – Abstract interface with mock/demonstration implementation (easy to replace with real Selenium/web‑scraping)
- **📈 Excel Management** – Automatic updates to candidate tracking spreadsheets using pandas/openpyxl
- **🗂️ File Organization** – Structured folder system for candidate documents
- **📥 Attachment Download** – Retrieve resumes, cover letters, and supporting documents
- **👀 Continuous Monitoring** – Watch for new applications and process them automatically
- **🛡️ Robust Error Handling** – Graceful recovery from network issues & data inconsistencies
- **📓 Comprehensive Logging** – Console + rotating file handlers with multiple log levels
- **⚙️ Configuration Driven** – Easy setup via `.env` + `config.yaml` (no hardcoded secrets)
- **🔖 Type Safe** – Full type hint coverage for improved reliability
- **🧪 Well Tested** – Unit & integration tests for core functionality
- **📖 Professional Documentation** – README, CHANGELOG, CONTRIBUTING, SECURITY, LICENSE, architecture diagrams

---

## 🏗️ Architecture

CandidateOps follows **Clean Architecture** with clear separation of concerns:

```
CandidateOps/
├── app/                    # CLI entry point & orchestrator
├── services/               # External integrations (SAP, Excel, File)
├── models/                 # Pure data structures (Candidate, Position, Application)
├── infrastructure/         # Technical concerns (config, logging)
├── utils/                  # Cross‑cutting helpers (exceptions, logging, helpers)
├── tests/                  # Test suite (pytest)
├── docs/                   # Architecture / diagrams (Mermaid)
├── config/                 # Example configuration files
├── scripts/                # Helper scripts (setup, demo)
└── assets/                 # Placeholder for screenshots, logos, etc.
```

### Key Components

- **🧩 SAP Service Layer** – `SAPClientInterface` defines the contract; `MockSAPClient` provides a working demo. Replace with a real Selenium‑based implementation for your SAP Career portal.
- **📊 Excel Handler** – Reads/writes candidate data to Excel using pandas/openpyxl.
- **📁 File Manager** – Creates candidate folders, saves attachments, and manages the file‑system layout.
- **🎛️ Orchestrator** – Coordinates the workflow: SAP authentication → position navigation → candidate processing → Excel updates → file management → monitoring.
- **🗃️ Data Models** – Strongly typed models for `Candidate`, `Position`, and `Application`.
- **⚙️ Configuration** – Pydantic‑based settings management loading from `.env` and `config.yaml`.
- **📝 Logging** – Structured logging with console and rotating file handlers.
- **🚨 Error Handling** – Custom exception types for meaningful error reporting.

---

## 📦 Installation

### Prerequisites

- ✅ Python **3.12** or higher  
- ✅ Google Chrome browser (for Selenium WebDriver – needed for a real SAP implementation)  
- ✅ ChromeDriver matching your Chrome version (automatically managed by `webdriver‑manager`)  

### Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/CandidateOps.git
   cd CandidateOps
   ```

2. **Create a virtual environment (highly recommended)**  
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS / Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**  
   - Copy the example environment file:  
     ```bash
     cp config/.env.example .env
     ```
   - Edit `.env` with your actual SAP credentials (see **Configuration** section below).

---

## ⚙️ Configuration

CandidateOps uses a layered configuration approach:

1. **Environment Variables** (`.env` file) – highest priority  
2. **Configuration File** (`config/config.yaml`) – default values  
3. **Hardcoded Defaults** – fallback values in code  

Copy `config/.env.example` → `.env` and fill in the required values:

```env
# ── Application ────────────────────────
APP_NAME=CandidateOps
VERSION=1.0.0
DEBUG=False

# ── Database (optional, for future extensions) ────────────────────────
DATABASE__URL=sqlite:///./candidate_ops.db
DATABASE__ECHO=False

# ── SAP Settings (REQUIRED – customize for your SAP instance) ────────
SAP__BASE_URL=https://your-company.sap.com          # ← UPDATE THIS
SAP__LOGIN_ENDPOINT=/login
SAP__CAREER_ENDPOINT=/career
SAP__TIMEOUT=30
SAP__IMPLICIT_WAIT=10
# If using a service account:
# SAP__USERNAME=your_service_account
# SAP__PASSWORD=your_password_or_token

# ── Excel Settings ────────────────────────
EXCEL__TEMPLATE_PATH=./templates/candidate_template.xlsx
EXCEL__OUTPUT_PATH=./output/candidates_tracking.xlsx
EXCEL__SHEET_NAME=Candidates
EXCEL__ID_COLUMN=CandidateID

# ── File Settings ────────────────────────
FILE__BASE_OUTPUT_DIR=./candidates_data
FILE__ATTACHMENTS_DIR=attachments
FILE__MAX_FILENAME_LENGTH=255

# ── Logging Settings ─────────────────────
LOGGING__LEVEL=INFO
LOGGING__FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOGGING__DATE_FORMAT=%Y-%m-%d %H:%M:%S
LOGGING__CONSOLE_ENABLED=True
LOGGING__FILE_ENABLED=True
LOGGING__FILE_PATH=./logs/candidate_ops.log
LOGGING__MAX_BYTES=10485760   # 10 MB
LOGGING__BACKUP_COUNT=5

# ── Monitoring Settings ────────────────────
MONITORING__CHECK_INTERVAL=300          # 5 minutes
MONITORING__MAX_RUNTIME_HOURS=8
MONITORING__ENABLE_NOTIFICATIONS=False
```

> 🔐 **Never commit your real `.env` file** – it contains secrets. The repository already includes `.gitignore` to keep it local.

---

## 🚀 Usage

### ▶️ Single Processing Cycle
Process candidates once and exit:
```bash
python -m app.main --username hr_user --single-cycle
```

### 🔁 Continuous Monitoring
Run continuously to monitor for new applications:
```bash
python -m app.main --username hr_user --continuous
```

### 🎯 Position‑Specific Processing
Target specific job positions:
```bash
python -m app.main --username hr_user --positions POS001 POS002 --single-cycle
```

### ℹ️ Check Application Status
View current status without running:
```bash
python -m app.main --status
```

### 🏷️ Show Version
Display version information:
```bash
python -m app.main --version
```

---

## 📂 Folder Structure (Runtime)

After the first run you’ll see:

```
CandidateOps/
├── output/
│   └── candidates_tracking.xlsx          # Excel tracking sheet
├── candidates_data/
│   ├── John_Doe_CAND001/
│   │   ├── Resume.pdf
│   │   ├── CoverLetter.pdf
│   │   └── attachments/
│   │       ├── transcript.pdf
│   │       └── certificate.pdf
│   └── Jane_Smith_CAND002/
│       ...
└── logs/
    └andidate_ops.log                     # Rotating log file
```

---

## 🖼️ Screenshots (Placeholders)

![Application Flow](assets/screenshots/application_flow.png)
![Folder Structure](assets/screenshots/folder_structure.png)
![Excel Output](assets/screenshots/excel_output.png)

*Add real screenshots here after you run the demo.*

---

## 🔮 Future Improvements

- [ ] **Real SAP implementation** – Selenium/web‑scraping tailored to your SAP Career portal
- [ ] **GUI Dashboard** – Real‑time monitoring and control panel
- [ ] **Additional attachment types** – Transcripts, certificates, portfolios, etc.
- [ ] **Email / Slack notifications** – Alert on new high‑priority candidates
- [ ] **ATS integration** – Sync with popular Applicant Tracking Systems
- [ ] **Duplicate detection & merging** – Intelligent candidate deduplication
- [ ] **Advanced reporting & analytics** – Charts, KPIs, export options
- [ ] **Docker containerization** – One‑command deployment
- [ ] **REST API** – Allow external systems to trigger processing or fetch data
- [ ] **Multi‑ERP support** – Extend to Oracle, Workday, SuccessFactors, etc.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository  
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)  
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)  
4. Push to the branch (`git push origin feature/AmazingFeature`)  
5. Open a Pull Request  

Please make sure to update tests as appropriate and follow the existing code style.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [SAP](https://www.sap.com/) – for providing the Career portal platform  
- [Selenium](https://www.selenium.dev/) – web automation capabilities  
- [Pandas](https://pandas.pydata.org/) – data manipulation  
- [OpenPyXL](https://openpyxl.readthedocs.io/) – Excel file handling  
- [Pydantic](https://docs.pydantic.dev/) – settings management  
- The open‑source Python community for libraries and tools  

---

**⚠️ Disclaimer**: This is a demonstration implementation. For production use with actual SAP systems, replace the mock SAP client with a real Selenium/web‑scraping implementation tailored to your specific SAP Career portal configuration. Always test thoroughly in a non‑production environment before deploying to production systems.

Happy recruiting! 🎉
