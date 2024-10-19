# Compliance Checker

## Overview
The Compliance Checker is a web application that analyzes a company's website against a specified policy using OpenAI's API.

## Features
- Fetches content from specified URLs.
- Analyzes compliance with policies using OpenAI's language model.
- Provides a detailed compliance report in JSON format.
- User-friendly web interface for ease of use.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **Web Scraping:** Beautiful Soup
- **API Integration:** OpenAI
- **Environment Management:** dotenv

## Hosted Frontend
The frontend page is hosted at http://35.154.37.45:8000/

## Backend API
The backend API is built using Flask and performs the compliance check by fetching content from the provided URLs and analyzing it with OpenAI's language model.

## Installation
To run the backend API:
1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Set up your `.env` file with your OpenAI API key.
4. Run the Flask application using `python app.py`.

## Usage
1. Enter the URLs for the company website and the policy document.
2. Click "Check Compliance" to analyze the compliance status.
3. Review the compliance report displayed on the web page.
