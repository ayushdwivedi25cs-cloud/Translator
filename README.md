# 🌍 BhashaAI - Real-Time Translator App

A powerful, real-time translator supporting Indian languages and major foreign languages.

## Features

✅ **Real-Time Translation** - Get instant translations as you type  
✅ **Multiple Languages** - Indian languages (Hindi, Tamil, Telugu, etc.) + Foreign languages (Spanish, French, Chinese, etc.)  
✅ **PDF Translation** - Translate entire PDF documents  
✅ **Copy & Swap** - Easy copy-to-clipboard and language swapping  
✅ **Translation History** - Keep track of recent translations  
✅ **No API Keys Required** - Uses Google Translate (free tier)  
✅ **Fast & Responsive** - Clean, modern UI with smooth animations  

## Supported Languages

### Indian Languages
- Hindi (हिंदी)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Marathi (मराठी)
- Gujarati (ગુજરાતી)
- Bengali (বাংলা)
- Punjabi (ਪੰਜਾਬੀ)
- Urdu (اردو)
- Odia (ଓଡ଼ିଆ)
- Assamese (অসমীয়া)

### Foreign Languages
- English
- Spanish (Español)
- French (Français)
- German (Deutsch)
- Portuguese (Português)
- Italian (Italiano)
- Russian (Русский)
- Chinese (中文)
- Japanese (日本語)
- Korean (한국어)
- Arabic (العربية)
- Dutch (Nederlands)
- Thai (ไทย)
- Vietnamese (Tiếng Việt)
- Indonesian (Bahasa Indonesia)

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Backend Setup

1. **Install dependencies:**
```bash
cd backend
pip install fastapi uvicorn pdfplumber reportlab deep-translator python-multipart pydantic
```

2. **Start the backend server:**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Start the frontend server** (in a new terminal):
```bash
cd frontend
python server.py
```

Frontend will be available at: `http://localhost:3000`

### Open the Application

Open your browser and navigate to:
```
http://localhost:3000
```

## Usage Guide

### 📝 Text Translation
1. Select source and target languages
2. Type or paste text in the left panel
3. Translation appears in real-time in the right panel
4. Click "Copy" to copy translated text
5. Click "Swap" to switch languages

### 📄 Document Translation
1. Go to the "Documents" tab
2. Select source and target languages
3. Click the upload area and select a PDF file
4. The translated PDF will download automatically

### 📋 Translation History
1. Go to the "History" tab
2. Click any previous translation to restore it
3. Clear all history with the "Clear History" button

## API Endpoints

### Text Translation
**POST** `/api/translate/text`
```json
{
  "text": "Hello, how are you?",
  "source_lang": "English",
  "target_lang": "Hindi",
  "mode": "Professional"
}
```

### PDF Translation
**POST** `/api/translate/pdf`
```
file: (PDF file)
source_lang: English
target_lang: Hindi
```

### Health Check
**GET** `/` - Returns API status

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Limitations

- Text limit: 5000 characters per translation
- PDF limit: 10MB file size
- Rate limit: 30 requests per minute per IP
- No offline mode (requires internet for translation)

## Architecture

```
┌─────────────────────────────────────────┐
│         Browser (Frontend)              │
│    http://localhost:3000                │
│  - HTML/CSS/JavaScript UI              │
│  - Real-time translation input         │
│  - Translation history storage         │
└─────────────────┬───────────────────────┘
                  │ HTTP/CORS
┌─────────────────▼───────────────────────┐
│        FastAPI Backend                  │
│    http://localhost:8000                │
│  - Text translation endpoint            │
│  - PDF translation endpoint             │
│  - Rate limiting middleware             │
│  - Error handling                       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Google Translate API               │
│  - Deep-translator library              │
│  - Language detection                   │
│  - Text chunking                        │
└─────────────────────────────────────────┘
```

## Technology Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** FastAPI, Python
- **Translation Engine:** Google Translate (deep-translator)
- **PDF Processing:** pdfplumber, reportlab
- **Server:** Uvicorn (ASGI)
- **CORS:** Enabled for local development

## Troubleshooting

### Backend not starting?
- Ensure all Python packages are installed
- Check if port 8000 is not in use
- Run: `python -m pip list` to verify packages

### Frontend not loading?
- Ensure backend is running first
- Check if port 3000 is not in use
- Clear browser cache and refresh

### Translation errors?
- Check internet connection (Google Translate requires internet)
- Verify language codes are correct
- Check backend logs for errors

### PDF upload fails?
- Ensure file is valid PDF (not image-based)
- Check file size is under 10MB
- Verify PDF has extractable text

## Performance Tips

1. Use shorter sentences for better translation quality
2. Translate one paragraph at a time for longer texts
3. Review translations for context accuracy
4. Clear history periodically to free up browser storage

## Future Enhancements

- [ ] Offline translation mode
- [ ] Audio input/output
- [ ] Document batch processing
- [ ] Custom glossary support
- [ ] Translation quality scoring
- [ ] Mobile app version
- [ ] Dark mode theme
- [ ] Multi-language comparison view

## License

This project is open-source and available for personal and commercial use.

## Support

For issues or questions, please check the backend logs or browser console for error messages.

---

**Made with ❤️ for breaking language barriers**

BhashaAI - Your Personal Language Translator | 2026
