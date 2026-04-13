# Reading Tracker

A web application for uploading and reading EPUB books in the browser, built with Django.

## Features

- Upload EPUB files and read them directly in the browser
- Chapter navigation via sidebar or Next / Back buttons
- User registration and login
- Reading list — tracks which books a user has read

## Tech Stack

- **Backend:** Django 5.0.1, SQLite
- **Frontend:** Vanilla JS, CSS (Montserrat font)
- **Auth:** Custom user model with email-based login
- **EPUB parsing:** Custom parser (based on [Lector](https://github.com/BasioMeusPuga/Lector)) using `zipfile`, `xmltodict`, `BeautifulSoup`

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mistmake/reading-tracker.git
cd reading-tracker
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp Reading_tracker/.env.example Reading_tracker/.env
```

```
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_FROM=your-email@gmail.com
```

### 5. Apply migrations and run

```bash
cd Reading_tracker
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Project Structure

```
Reading_tracker/
├── Reading_tracker/   # Project settings and URL config
├── main/              # Homepage, file upload
├── book/              # Book model, EPUB reader, file parser
└── user/              # Custom user model, auth views
```

## Author

Dmitrii Liakhov — [GitHub](https://github.com/mistmake) · [LinkedIn](https://www.linkedin.com/in/dmitrii-liahov-3828a23b7)
