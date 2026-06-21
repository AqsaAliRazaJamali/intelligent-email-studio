# ✉️ Intelligent Email Studio

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-4285F4?logo=google&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?logoColor=white)
![AI Powered](https://img.shields.io/badge/AI-Powered-blueviolet)
![License](https://img.shields.io/badge/License-MIT-green)

An AI-powered communication workspace designed to streamline professional email workflows through intelligent automation, contextual understanding, and polished content generation.

Built using Google's Gemini 2.5 Flash and Groq-powered Llama 3.1 failover routing, the platform helps users analyze incoming emails, draft professional responses, and generate context-aware replies efficiently.

---

## 🚀 Features

### 📁 Analyze Framework
Transforms raw, unstructured emails into a clean and organized metadata dashboard by extracting:

- Email Category
- Priority Level
- Action Items
- Assigned Tasks
- Suggested Follow-ups & Reminders

---

### ✍️ Draft Composer
Generates professional email drafts from simple prompts or contextual intent using multiple communication tones such as:

- Professional
- Formal
- Friendly
- Persuasive
- Concise

---

### 🔄 Smart Thread Reply
Analyzes ongoing conversation threads and generates contextual, human-like replies that maintain conversation flow naturally.

---

## 🎯 Benefits

- Save time managing emails
- Generate polished communication instantly
- Organize unstructured inbox content
- Improve productivity with AI-assisted workflows
- Maintain professional communication quality

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive frontend UI |
| Google Gemini 2.5 Flash | Primary AI model |
| Groq Llama 3.1 | Failover AI routing |
| TOML Secrets Vault | Secure API key management |

---

## 🧠 AI Architecture

The application uses a resilient dual-model AI workflow:

1. **Gemini 2.5 Flash** handles primary generation and analysis tasks.
2. If unavailable, the system automatically switches to **Groq Llama 3.1** for uninterrupted operation.

This architecture improves reliability, response continuity, and overall user experience.

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <https://intelligent-email-studio.streamlit.app/>
cd intelligent-email-studio
```

---

### 2️⃣ Install Dependencies

Ensure Python is installed, then run:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.streamlit/secrets.toml` file in the project root directory:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will launch locally in your browser.

---


## 👩‍💻 Author

Aqsa Jamali

Computer Science Student passionate about AI-powered applications, intelligent systems, and modern web experiences.

---

## 📄 License

This project is licensed under the MIT License.
