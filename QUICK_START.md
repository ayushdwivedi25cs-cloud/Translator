# 🎉 BhashaAI Translator - Quick Start Guide

## ✅ What's Ready

Your **BhashaAI Translator App** is now fully functional and running!

### Currently Running:
- ✅ **Backend Server**: http://localhost:8000 (FastAPI)
- ✅ **Frontend Server**: http://localhost:3000 (Modern Web UI)
- ✅ **Real-time Translation**: Instant translations as you type
- ✅ **30+ Languages Supported**: Indian + Foreign Languages

---

## 🚀 How to Use

### 1. **Open the App**
Navigate to: **http://localhost:3000**

### 2. **Text Translation** (📝 Tab - Default)
- **Select Languages**: Choose source and target languages
- **Type or Paste**: Enter text (up to 5000 characters)
- **Auto-Translate**: Translation appears in real-time!
- **Copy**: Click the green "Copy" button to copy translations
- **Swap**: Click the purple "🔄 Swap" button to reverse languages

### 3. **Document Translation** (📄 Tab)
- **Select Languages**: Choose source and target
- **Upload PDF**: Click to upload (max 10MB)
- **Auto-Download**: Translated PDF downloads automatically!

### 4. **View History** (📋 Tab)
- **Recent Translations**: View last 20 translations
- **Click to Restore**: Click any translation to restore it
- **Clear All**: Remove all history permanently

---

## 🌍 Supported Languages

### Indian Languages
| Language | Code | Script |
|----------|------|--------|
| Hindi | hi | हिंदी |
| Tamil | ta | தமிழ் |
| Telugu | te | తెలుగు |
| Kannada | kn | ಕನ್ನಡ |
| Malayalam | ml | മലയാളം |
| Marathi | mr | मराठी |
| Gujarati | gu | ગુજરાતી |
| Bengali | bn | বাংলা |
| Punjabi | pa | ਪੰਜਾਬੀ |
| Urdu | ur | اردو |
| Odia | or | ଓଡ଼ିଆ |
| Assamese | as | অসমীয়া |

### Foreign Languages
| Language | Code |
|----------|------|
| English | en |
| Spanish | es |
| French | fr |
| German | de |
| Portuguese | pt |
| Italian | it |
| Russian | ru |
| Chinese | zh-CN |
| Japanese | ja |
| Korean | ko |
| Arabic | ar |
| Dutch | nl |
| Thai | th |
| Vietnamese | vi |

---

## 🛠️ Terminal Commands

### To Start (Run these in separate terminals)

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python server.py
```

### Status
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

---

## ⚡ Key Features

✨ **Real-Time Translation**
- Translates as you type (500ms debounce)
- No need to press a button!

🔄 **Bidirectional**
- Swap languages instantly
- Translate back and forth

📋 **Translation History**
- Auto-saves last 20 translations
- Stored in browser (localStorage)

📄 **PDF Support**
- Extract text from PDFs
- Translate entire documents
- Download translated PDFs

🎨 **Beautiful UI**
- Modern gradient design
- Responsive (desktop & mobile)
- Smooth animations

⚡ **Fast & Reliable**
- Uses Google Translate API
- Rate limited (30 req/min)
- Error handling

---

## 🔧 API Endpoints

### Health Check
```
GET http://localhost:8000/
```

### Translate Text
```
POST http://localhost:8000/api/translate/text
Content-Type: application/json

{
  "text": "Hello",
  "source_lang": "English",
  "target_lang": "Hindi",
  "mode": "Professional"
}
```

### Translate PDF
```
POST http://localhost:8000/api/translate/pdf
Content-Type: multipart/form-data

file: (PDF file)
source_lang: English
target_lang: Hindi
```

---

## 📝 Example Translations

| English | Hindi | Tamil | Spanish |
|---------|-------|-------|---------|
| Hello | नमस्ते | வணக்கம் | Hola |
| Good Morning | शुभ प्रभात | காலை வணக்கம் | Buenos días |
| Thank You | धन्यवाद | நன்றி | Gracias |
| Goodbye | अलविदा | பிரிவிடை | Adiós |

---

## 🐛 Troubleshooting

### Translation not appearing?
- ✅ Check internet connection
- ✅ Verify backend is running
- ✅ Open browser console (F12) for errors

### PDF upload fails?
- ✅ Check file size (< 10MB)
- ✅ Ensure PDF has text (not just images)
- ✅ Verify supported languages

### "Rate limit exceeded"?
- ✅ Wait a minute before translating again
- ✅ Limit is 30 requests per minute per IP

### Port already in use?
- ✅ Change port in commands
- ✅ Or kill existing process

---

## 📊 Performance Tips

1. **Shorter text = Better quality** translations
2. **One paragraph at a time** works best
3. **Review translations** for context
4. **Clear history** occasionally for faster app
5. **Use swapping** to verify round-trip accuracy

---

## 🎓 What's Under The Hood

```
Architecture:

┌─────────────────────────────────────────┐
│         Frontend (HTML/JS)              │
│   - Real-time UI with auto-refresh     │
│   - LocalStorage for history           │
│   - Beautiful CSS animations           │
└─────────────────┬───────────────────────┘
                  │ HTTP/CORS
┌─────────────────▼───────────────────────┐
│        Backend (FastAPI/Python)         │
│   - Text/PDF translation endpoints     │
│   - Rate limiting middleware           │
│   - Error handling & validation        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Google Translate (Free API)        │
│   - Via deep-translator library        │
│   - No API key required!               │
└─────────────────────────────────────────┘
```

---

## 🚀 Next Steps

1. **Open browser**: http://localhost:3000
2. **Try typing**: Test with different languages
3. **Test features**: Try PDF upload, history, swap
4. **Share**: Bookmark or share the URL!

---

## 📞 Need Help?

- Check backend logs for errors
- Open browser console (F12) → Console tab
- Verify both servers are running
- Check `README.md` for detailed docs

---

## 🎯 Use Cases

✅ Learn new languages  
✅ Translate business documents  
✅ Break language barriers  
✅ Travel companion  
✅ Content translation  
✅ Customer service  
✅ Multi-language communication  

---

**Made with ❤️ for real-time translation excellence**

BhashaAI - Your Personal Translator | 2026

Last Updated: June 15, 2026
