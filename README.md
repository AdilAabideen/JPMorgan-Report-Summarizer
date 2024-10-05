# JPMorgan-Report-Summarizer

## Overview

The JPMorgan Report Summarizer is a web application that allows users to select sections from JPMorgan’s annual reports and receive AI-generated summaries. The application is built with a Next.js frontend and a Flask backend, utilizing OpenAI’s GPT models to generate concise and informative summaries.

## Features

	•	Interactive UI: Browse and search through the table of contents of JPMorgan’s annual reports.
	•	AI-Powered Summaries: Generate summaries using OpenAI’s GPT-3.5 Turbo or GPT-4 models.
	•	Responsive Design: Optimized for both desktop and mobile devices.
	•	Search Functionality: Quickly find specific topics within the reports.
	•	Hover Animations: Enhanced user experience with Framer Motion animations.

## Technology Stack

	•	Frontend: Next.js, React, Tailwind CSS, Framer Motion
	•	Backend: Flask, Python, OpenAI API
	•	AI Integration: OpenAI’s GPT models
	•	PDF Processing: pdfplumber
	•	Environment Management: dotenv

## Prerequisites

	•	Node.js (v14.x or later)
	•	Python (v3.7 or later)
	•	pip (Python package manager)
	•	OpenAI API Key: Required to access OpenAI’s GPT models.

## Installation

1. Clone the Repository

```bash
git clone https://github.com/yourusername/jpmorgan-report-summarizer.git
cd jpmorgan-report-summarizer
```
## 2. Set Up the Backend (Flask)

### a. Navigate to the Backend Directory

```bash
cd backend
```

### b. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### c. Install Python Dependencies

```bash
pip install -r requirements.txt
```
### d. Set Up Environment Variables

Create a .env file in the backend/ directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```
Note: Replace your_openai_api_key_here with your actual OpenAI API key. Do not share or commit this key.

### e. Prepare PDF Data

Ensure the PDF files (Part_1.pdf, part_2.pdf, part_3.pdf) are placed inside the pdfData/ directory.

## 3. Set Up the Frontend (Next.js)

### a. Navigate to the Frontend Directory

```bash
cd ../frontend
```

b. Install Node Dependencies

```bash
npm install
```
### c. Set Up Environment Variables

Create a .env.local file in the frontend/ directory:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## 4. Running the Application

### a. Start the Backend Server

In the backend/ directory (ensure your virtual environment is activated):
```bash
cd ../backend
python server.py
```
The Flask server will run on http://localhost:8080.

### b. Start the Frontend Server

In a new terminal, navigate to the frontend/ directory:
```bash
cd frontend
npm run dev
```

The Next.js application will run on http://localhost:3000.

## Usage

	1.	Open your browser and navigate to http://localhost:3000.
	2.	Browse through the table of contents displayed on the homepage.
	3.	Use the search bar to find specific topics.
	4.	Click on a topic card to navigate to the summary page.
	5.	The application will fetch and display the AI-generated summary for the selected topic.

## Project Structure

```bash
jpmorgan-report-summarizer/
├── backend/
│   ├── app.py
│   ├── server.py
│   ├── summarization.py
│   ├── requirements.txt
│   ├── pdfData/
│   │   ├── Part_1.pdf
│   │   ├── part_2.pdf
│   │   └── part_3.pdf
│   └── .env
├── frontend/
│   ├── components/
│   │   ├── Card.js
│   │   └── ...
│   ├── pages/
│   │   ├── index.js
│   │   ├── summarizer/
│   │   │   └── [slug].js
│   │   └── ...
│   ├── public/
│   ├── styles/
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.local
├── README.md
└── .gitignore
```

## API Endpoints

### Backend (Flask)

	•	GET /api/home: Returns a simple welcome message.
	•	GET /api/summarize/<int:topic_index>/<int:topic_part>: Summarizes a report section based on the provided topic_index and topic_part.
	•	POST /api/bot: Accepts a prompt and returns an AI-generated response.

## Environment Variables

### Backend (backend/.env)

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Front End 

```bash
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## Dependencies

### Backend (requirements.txt)

	•	flask
	•	flask_cors
	•	openai
	•	pdfplumber
	•	python-dotenv
	•	langchain
	•	chromadb

Install using:
```bash
pip install -r requirements.txt
```
### Frontend (package.json)

	•	next
	•	react
	•	react-dom
	•	axios
	•	framer-motion
	•	tailwindcss
	•	@headlessui/react

Install using:
```bash
npm install
```
## Important Notes

	•	API Keys: Keep your OpenAI API key secure. Do not expose it in client-side code or commit it to version control.
	•	.gitignore: Ensure that sensitive files like .env are included in .gitignore.
	•	CORS: The Flask backend uses flask_cors to handle Cross-Origin Resource Sharing.
	•	Version Compatibility: Ensure that the versions of packages used are compatible with each other.

## Potential Issues and Solutions

	•	CORS Errors: If you encounter CORS issues, make sure the frontend is making requests to the correct backend URL and that flask_cors is properly configured.
	•	Module Import Errors: Ensure all modules are installed in your virtual environment and that you’re using the correct versions.
	•	OpenAI Rate Limits: Be mindful of OpenAI’s API rate limits to avoid errors due to excessive requests.

## Contributing

Contributions are welcome! Please follow these steps:

	1.	Fork the repository.
	2.	Create a new branch: git checkout -b feature/your-feature-name.
	3.	Commit your changes: git commit -m 'Add some feature'.
	4.	Push to the branch: git push origin feature/your-feature-name.
	5.	Submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments

	•	OpenAI for providing the GPT models.
	•	JPMorgan Chase & Co. for the annual reports.
	•	Community Contributors for their support and feedback.

## Contact

For any questions or issues, please open an issue on the repository or contact the maintainer.

Disclaimer: This project is for educational purposes. Ensure you comply with OpenAI’s policies and JPMorgan Chase & Co.’s terms when using their content.