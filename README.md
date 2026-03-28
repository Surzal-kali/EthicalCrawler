# Dev Forward
Initializing EthicalCrawler...
Session ID: EC-20260328-0413
Temp directory: /tmp/ethicalcrawler_EC-20260328-0413/

============================================================
ETHICAL OPERATOR CONSENT REQUIRED
============================================================

I acknowledge that this session will be logged for transparency.
All actions will target only systems I own or have permission to test.

Type 'CONSENT' to continue, anything else to exit: CON
SENT

Consent logged to: /consent/session_EC-20260328-0413.json

============================================================
BOOT SEQUENCE COMPLETE
============================================================
  os_name: Windows
  os_version: 10.0.26200
  architecture: AMD64
  processor: Intel64 Family 6 Model 151 Stepping 2, GenuineIntel
This program may not be optimized for the following specs. Proceed with caution.

The Crawler is completely ethical and legal.
DEV NOTES:

this is my god's honest attempt at making:

1. A legal and ethical white-box automated pen test.  

2 An overly amibitiouis Python Basics final

Enjoy the show
*****************


# EthicalCrawler
![Status](https://img.shields.io/badge/status-work_in_progress-yellow)

## Overview

EthicalCrawler is a work-in-progress white-box penetration testing and OSINT (Open-Source Intelligence) tool designed for security researchers. Its goal is to scan its own environment and the host machine to identify potential security weaknesses and provide actionable advice for hardening the system.

**Note:** This project is in its early stages of development. The features described below are the end goal, and not all may be implemented yet.

## Planned Features

*   **System Environment Scanning:** Analyze the host machine for misconfigurations, vulnerabilities, and security best-practice deviations.
*   **OSINT Gathering:** Collect public information relevant to the security posture of the environment.
*   **Actionable Advice:** Provide clear, context-aware recommendations for system hardening.
*   **Reporting:** Generate reports of findings (planned support for PDF and CSV).

## Getting Started

### Prerequisites

*   Python 3.10+
*   `git` for cloning the repository.
*   `wkhtmltopdf` (for PDF report generation via `pdfkit`). You can find installation instructions [here](https://wkhtmltopdf.org/downloads.html).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Surzal-kali/EthicalCrawler.git
    cd EthicalCrawler
    ```

2.  **Install the required Python libraries.** It is recommended to use a virtual environment.
    ```bash
    # Create and activate a virtual environment (optional but recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    # Install dependencies
    pip install -r requirements.txt
    ```

### `requirements.txt`

You will need to create a `requirements.txt` file with the following content for the `pip install` command to work:
```
pdfkit
psutil
```
*(Note: The other imported modules like `os`, `socket`, `json`, etc., are part of the Python standard library and do not need to be installed separately.)*

### Usage

To run the main program, execute the `VanessaPFinal.py` script:

```bash
python VanessaPFinal.py
```

## Contributing

This project is currently under active development. If you are interested in contributing, please feel free to fork the repository and submit a pull request. You can also open an issue to report bugs or suggest features.
