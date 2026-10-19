
# AI Chat Application 💬

A beginner-friendly AI chatbot built using Python, Streamlit, and Google's Gemini API.

## Features

- Interactive chat interface
- AI-generated responses
- Conversation history
- Custom system instructions
- Adjustable temperature and response token limit
- Token usage display when available
- API error handling
- Secure API key management using environment variables

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI Python SDK
- python-dotenv

## Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-chat-app
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_actual_api_key
```

Replace the example value with your own API key.

### 5. Start the application

```bash
python -m streamlit run app.py
```

## Security

Never commit your `.env` file or publish your API key.

## Author

Developed as an LLM APIs and Application Development project.
