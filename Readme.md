# Instahyre Easy Apply Bot

## Overview
This is an automated bot designed to streamline the job application process on Instahyre. The bot helps job seekers save time by automating repetitive application tasks.

## Features
- Automatic login to Instahyre
- Search for jobs based on specified criteria
- Apply to jobs automatically
- Track applied jobs
- Handle application process

## Requirements
- Python 3.7+
- Selenium WebDriver
- Chrome Browser/Brave Browser
- ChromeDriver

## Installation
```bash
pip install selenium
pip install webdriver_manager
```

## Usage
1. Update your credentials in the config file
2. Run the script:
   for Instahyre Automation:
```bash
python instahyre.py
```
  for Flexiple Automation:
```bash
python flexiple.py
```

## Configuration
Create a `.env` file in the project root with your Instahyre credentials:

```plaintext
EMAIL=your_email@example.com
PASSWORD=your_password
```

The bot will automatically load these environment variables for authentication.

## Disclaimer
This bot is for educational purposes only. Use at your own risk and be aware of Instahyre's terms of service.

## Contributing
Feel free to fork, create pull requests, or report issues.

## License
MIT License
