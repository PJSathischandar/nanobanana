# Streamlit + Nano Banana Chat Image Generator

This project provides a simple Streamlit UI that integrates the nano banana library. Users can enter text in a chat interface, and the app will generate images based on the input using nano banana.

## Features
- Streamlit-based web UI
- Chat interface for user input
- Image generation using nano banana

## Setup
1. Install dependencies:
   ```sh
   pip install streamlit nano-banana
   ```

2. Set up your Gemini API key for Streamlit:
   - Create a file at `.streamlit/secrets.toml` in your project root (create the `.streamlit` folder if it doesn't exist).
   - Add the following content (replace with your actual API key):
     ```toml
     GEMINI_API_KEY = "your-api-key-here"
     ```

3. Run the app (from your virtual environment):
   ```sh
   .venv\Scripts\python.exe -m streamlit run app.py
   ```

## Usage
- Enter a prompt in the chat box and submit.
- The app will display the generated image below the chat.

---
*Replace this README with more details as needed.*
