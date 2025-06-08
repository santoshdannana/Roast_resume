# 🔥 Roast My Resume

A fun and savage resume roasting web app powered by Google's Gemini API. Upload your resume and get brutally honest (and hilarious) feedback in the voice of a comedian, grandma, roommate, and more.

> 👇 Try it live:  
[Roast my resume](https://santosh-roast.up.railway.app/)

---

## 🚀 Features

- Upload `.pdf` or `.docx` resumes
- Choose a roast persona: Comedian, Grandma, Roommate, etc.
- Set the intensity from *Mild* to *Nuclear*
- Get personalized, culturally-aware roast feedback
- Clean, comic-inspired UI
- Built with Flask + Gemini 1.5 API

---

## 🧰 Tech Stack

- Python (Flask)
- Google Generative AI (Gemini 1.5 Flash)
- PyMuPDF, python-docx for resume parsing
- HTML + CSS (Comic-style theme)
- Railway (for deployment)

---

## 🛠️ Setup Locally

### 1. Clone the project

```bash
git clone https://github.com/yourusername/resume-roast.git
cd resume-roast
```

### 2. Create `.env` file

Create a file named `.env` in the project root:

```
GEMINI_API_KEY=your_actual_google_gemini_api_key_here
```

⚠️ Never commit this file. It is already in `.gitignore`.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Visit `http://localhost:5000`

---

## 🧑‍💻 Deploying to Railway

1. Push your code to GitHub
2. Create a new Railway project from the repo
3. Go to **Settings → Environment Variables** and add:

```
GEMINI_API_KEY = your_google_api_key_here
```

4. Add a `Procfile`:

```
web: python app.py
```

5. Deploy and enjoy!

---

## 🔒 Security Notes

- `.env` and `firebase-key.json` are ignored via `.gitignore`
- API keys must be kept secret and stored via Railway’s dashboard in production

---

## 📄 License

MIT — use it, fork it, roast responsibly.
