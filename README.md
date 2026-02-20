# MFT Courses Scraper & FAQ Chatbot

A Persian language web scraper and AI-powered chatbot system for MFTPlus courses with intelligent FAQ matching using machine learning.

## Project Overview

This project consists of two main components:

1. **Web Scraper** (`scraper.py`) - Collects course data from [MFTPlus](https://mftplus.com/) for various departments
2. **FAQ Chatbot Web App** (`app.py`) - Flask-based web application with intelligent FAQ matching using TF-IDF vectorization and cosine similarity

## Features

- 🔍 **Web Scraping**: Extracts course information from MFTPlus for multiple departments:
  - Health Sciences
  - Finance & Accounting
  - Engineering
  - IT & Communications
  - Management & Business

- 🤖 **Intelligent FAQ Matching**: Uses TF-IDF vectorization and cosine similarity to match user questions with FAQ answers
- 🌐 **Persian Text Support**: Full support for Persian/Farsi language with text normalization using Hazm
- 🎨 **Web Interface**: Flask-based web application with responsive HTML/CSS frontend
- 📊 **Course Integration**: Seamlessly integrates course data from scraped content

## Project Structure

```
├── scraper.py              # Web scraper for MFTPlus courses
├── app.py                  # Flask web application
├── model.py                # ML model and text processing
├── faq_dataset.json        # FAQ Q&A dataset
├── faq-df.py              # FAQ dataframe processing
├── mft_courses_it.csv     # Scraped IT courses data
├── static/
│   └── style.css          # CSS styling
└── templates/
    └── index.html         # Web interface
```

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Dependencies

Install required packages:

```bash
pip install flask pandas requests hazm scikit-learn
```

**Key Libraries:**
- `flask` - Web framework
- `pandas` - Data processing
- `requests` - HTTP requests for scraping
- `hazm` - Persian text processing and normalization
- `scikit-learn` - Machine learning (TF-IDF, cosine similarity)

## Usage

### 1. Scraping Course Data

Run the scraper to collect courses from a specific department:

```bash
python scraper.py
```

You'll be prompted to select a department:
```
Available Departments:
health             | دانش سلامت
finance            | علوم مالی و حسابداری
engineering        | علوم مهندسی
it                 | فناوری اطلاعات و ارتباطات
management         | مدیریت و کسب و کار

Enter the 'key' of department to filter: it
```

The scraper will save course data to `mft_courses_it.csv`

### 2. Running the Web Application

Start the Flask web server:

```bash
python app.py
```

Access the application at `http://localhost:5000`

### 3. FAQ Processing

Process FAQ data using:

```bash
python faq-df.py
```

## How It Works

### FAQ Matching Algorithm

1. **Text Normalization**: Persian text is normalized using Hazm library
2. **Vectorization**: Questions are converted to TF-IDF vectors
3. **Similarity Matching**: User queries are compared against FAQ questions using cosine similarity
4. **Threshold**: Matches with similarity > 0.2 are returned; otherwise, a default "not found" message is shown
5. **Course Integration**: Course data is searched for relevant titles in user queries

### Data Flow

```
User Query
    ↓
Text Normalization (Hazm)
    ↓
TF-IDF Vectorization
    ↓
Cosine Similarity Matching
    ↓
FAQ Answer or Course Info
```

## Files Description

| File | Purpose |
|------|---------|
| `scraper.py` | Fetches course data from MFTPlus API |
| `app.py` | Main Flask application with FAQ matching logic |
| `model.py` | ML model for text processing and similarity |
| `faq_dataset.json` | FAQ Q&A pairs in JSON format |
| `faq-df.py` | Processes FAQ data into dataframes |
| `mft_courses_it.csv` | CSV file with scraped course data |
| `static/style.css` | CSS styling for web interface |
| `templates/index.html` | HTML template for web UI |

## Configuration

The scraper uses the following base URL:
```
https://mftplus.com/ajax/default/calendar
```

Search parameters can be adjusted in `scraper.py`:
- `batch_size`: Number of courses per batch (default: 9)
- Similarity threshold in `app.py` for FAQ matching (default: 0.2)

## Example Data

### FAQ Dataset Structure
```json
[
  {
    "questions": ["سوال 1", "سوال 2"],
    "answer": "پاسخ"
  },
  ...
]
```

### Courses CSV Structure
```
title, duration, price, ...
دوره آموزشی, 40 ساعت, 500000, ...
```

## Requirements

- Active internet connection for web scraping
- Read/write access to create CSV files
- Port 5000 available for Flask server

## License

This project is part of Machine Learning course materials (ML12 - Exercise 03).

## Notes

- Ensure compatible versions of hazm and scikit-learn
- The FAQ matching threshold (0.2) can be adjusted based on accuracy needs
- Scraped data is subject to MFTPlus terms of service

## Troubleshooting

**ImportError for hazm/scikit-learn**: Reinstall dependencies
```bash
pip install --upgrade hazm scikit-learn
```

**Connection Error while scraping**: Check MFTPlus availability and internet connection

**Flask port already in use**: Change port in app.py or kill existing process

---

**Created**: February 2026  
**Course**: Machine Learning - MFT  
**Exercise**: 03 - Web Scraping & NLP
