# Dadi's Rasoi ❤️

**Preserve the recipes that live in someone's memory.**

*Built for Hacktoberfest 2026 — Weekend Challenge: Build for a Friend*

## 💡 The Problem
Family recipes frequently exist only in someone's memory or scattered voice messages.

## 🥘 The Solution
Dadi's Rasoi is a small, warm personal web application that converts those voice explanations into structured, searchable family recipes. 

## 🛠️ Local AI Architecture

Once the models are installed, the core AI pipeline can run without sending family voice recordings to a remote AI provider.

```text
Voice
  ↓
faster-whisper (Local Speech Recognition)
  ↓
Transcript
  ↓
Gemma via Ollama (Local LLM)
  ↓
Structured Recipe
  ↓
Pydantic validation
  ↓
SQLite (Local Cookbook)
```

## 🤔 Why Open AI?
- **Privacy:** Keep family data under your control. The local models ensure nothing leaves your laptop.
- **Model Flexibility:** Swap out the core extraction model as open-weight models evolve.
- **No Proprietary Lock-in:** Ensure the family cookbook isn't dependent on expensive APIs.

## 🚀 Running Locally

### 1. Python environment
Python 3.10+ is recommended.

### 2. Python dependencies
```bash
pip install -r requirements.txt
```

### 3. FFmpeg
Faster-Whisper requires FFmpeg to process audio files.
- Windows: Download via Chocolatey (`choco install ffmpeg`) or from the official site.
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### 4. Ollama
Install Ollama from [ollama.com](https://ollama.com).

### 5. Gemma
Since you already have `gemma3` models locally, Dadi's Rasoi is configured by default to use:
```bash
ollama run gemma3:4b
```

### 6. Environment Setup
Copy the environment template:
```bash
cp .env.example .env
```

### 7. Run Dadi's Rasoi
```bash
streamlit run app.py
```

## 🔒 Privacy
**Local AI:** Your family's recipes belong to you. Dadi's Rasoi is designed to keep your cookbook under your control. By using `faster-whisper` and `Ollama`, voice recordings and text stay entirely on your device.
