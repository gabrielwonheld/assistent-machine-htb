# Assistent - CTF Lab

Welcome to the Assistent CTF (Capture The Flag) laboratory! This is a deliberately vulnerable web application designed to practice various exploitation techniques.

## Features & Vulnerabilities

This lab includes the following intentional vulnerabilities:

1. **Mass Assignment**: The `/update-profile` endpoint is vulnerable to parameter injection, allowing you to escalate your account privileges (e.g., adding an `is_admin` field).
2. **SSTI / RCE (Server-Side Template Injection)**: Triggered by uploading a payload as a technical specification file (`ficha técnica`), which gets evaluated by the Jinja template engine leading to Remote Code Execution.
3. **Privilege Escalation (Python Library Hijacking)**: A backup script (`bkp.py`) is executed as the `root` user via a Cron job every 1 minute. You can exploit this through PATH hijacking by creating a malicious `zipfile.py` script in the same directory, escalating your privileges to `root`.

## How to Start the Lab

To initialize the laboratory and set up the vulnerabilities, follow these instructions:

### 1. Run the Setup Script
The project includes a `setup.sh` script that automatically configures the Python environment, installs the necessary dependencies, and sets up the vulnerable cron job for the privilege escalation vector.

Open your terminal, navigate to the project directory, make the script executable, and run it:

```bash
chmod +x setup.sh
./setup.sh
```

*Note: The script will prompt you for your `sudo` password to configure the cron job correctly.*

### 2. Start the Web Application
Once the setup is successfully completed and all dependencies are installed, you can start the vulnerable Flask web application by running:

```bash
python3 app.py
```

The application will start running on port 5000 and can be accessed in your browser at:
`http://localhost:5000` or `http://0.0.0.0:5000`

Good luck, and Happy Hacking!
