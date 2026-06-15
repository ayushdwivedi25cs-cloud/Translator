from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import io
import time
import pdfplumber
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from deep_translator import GoogleTranslator
import os, textwrap
from dialects import DIALECT_FALLBACKS, process_bundelkhandi, process_hinglish, process_bhojpuri

app = FastAPI(title="BhashaAI API")

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic In-Memory Rate Limiting
# Note: In production, use Redis.
RATE_LIMIT_STORE = {}
MAX_REQUESTS_PER_MINUTE = 30

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()
    
    # Initialize or clean up old requests
    if client_ip not in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[client_ip] = []
    RATE_LIMIT_STORE[client_ip] = [req_time for req_time in RATE_LIMIT_STORE[client_ip] if now - req_time < 60]
    
    if len(RATE_LIMIT_STORE[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
        # Return 429 Too Many Requests
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Please try again later."})
        
    RATE_LIMIT_STORE[client_ip].append(now)
    response = await call_next(request)
    return response

# =====================================================================
# ML MODEL INTEGRATION (PLACEHOLDER FOR POST-TRAINING)
# =====================================================================
# Once you run finetune.py on a GPU cluster and generate the LoRA weights,
# you will uncomment and use the following code to load the model into memory.
"""
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from peft import PeftModel
import torch

BASE_MODEL = "ai4bharat/indictrans2-en-indic-1B"
ADAPTER_PATH = "./models/bundelkhandi_adapter" # Path to your trained weights

print("Loading IndicTrans2 Base Model...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
base_model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL, trust_remote_code=True, torch_dtype=torch.float16)

print("Applying Custom Dialect LoRA Adapters...")
ml_model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
ml_model.eval()

# To use in your endpoints:
# inputs = tokenizer("bnd: " + text, return_tensors="pt")
# outputs = ml_model.generate(**inputs, max_new_tokens=128)
# translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
"""
# =====================================================================

class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    mode: str = "Professional"

LANGUAGE_MAP = {
    # International Language
    "English": "en",
    
    # Major Indian Languages (Official Languages)
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Odia": "or",
    "Assamese": "as",
    
    # Other Major Indian Languages
    "Sanskrit": "sa",
    "Nepali": "ne",
    "Konkani": "kok",
    "Manipuri": "mni",
    "Sindhi": "sd",
    "Bodo": "brx",
    "Dogri": "doi",
    "Maithili": "mai",
    "Santali": "sat",
    
    # Hindi Dialects & Regional Variations
    "Bhojpuri": "hi",          # Eastern Hindi Dialect
    "Bundelkhandi": "hi",      # Central India Dialect
    "Awadhi": "hi",            # Eastern UP Dialect
    "Magahi": "hi",            # Bihar Dialect
    "Angika": "hi",            # Bihar/Jharkhand Dialect
    "Chhattisgarhi": "hi",     # Chhattisgarh Dialect
    "Bagheli": "hi",           # Madhya Pradesh Dialect
    
    # South Indian Dialects
    "Gondi": "ta",             # Gondi Language (Dravidian)
    "Tulu": "kn",              # Tulu Language (South Coastal)
    "Kodava": "kn",            # Kodava Language
    "Konkani-Devanagari": "kok",  # Konkani variant
    
    # Eastern Indian Dialects
    "Angika": "hi",
    "Bihari": "hi",
    "Magadhi": "hi",
    
    # Western Indian Dialects
    "Bhili": "gu",
    "Warli": "gu",
    
    # North Eastern Dialects
    "Khasi": "as",
    "Mizo": "as",
    "Nagamese": "as",
    "Tripuri": "as",
    
    # Island & Coastal Languages
    "Santhali": "sat",
    "Ho": "sat",
    
    # Additional Sanskrit-derived Languages
    "Pali": "sa",
    
    # Alternative spellings
    "Hinglish": "hi",
    "Oriya": "or",
    "Assamese": "as",
    "Meitei": "mni",
}

def translate_chunk(text: str, source_code: str, target_code: str, target_lang_name: str = "") -> str:
    """Translate a single chunk of text."""
    if not text.strip():
        return text
        
    # Hinglish processing
    if target_lang_name == "Hinglish":
        return process_hinglish(text)
        
    try:
        translated = GoogleTranslator(source=source_code, target=target_code).translate(text)
        
        # Bundelkhandi processing
        if target_lang_name == "Bundelkhandi":
            translated = process_bundelkhandi(text, translated)
            
        # Bhojpuri processing
        if target_lang_name == "Bhojpuri":
            translated = process_bhojpuri(text, translated)
            
        return translated
    except Exception as e:
        return f"[Translation error: {str(e)}]"

def translate_long_text(text: str, source_code: str, target_code: str, target_lang_name: str = "") -> str:
    """Split long text into safe chunks and translate each."""
    max_len = 4500
    if len(text) <= max_len:
        return translate_chunk(text, source_code, target_code, target_lang_name)
    
    # Split on paragraph boundaries first
    paragraphs = text.split("\n")
    chunks, current = [], ""
    for para in paragraphs:
        if len(current) + len(para) + 1 > max_len:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            current += "\n" + para if current else para
    if current:
        chunks.append(current.strip())
    
    translated_chunks = []
    for chunk in chunks:
        translated_chunks.append(translate_chunk(chunk, source_code, target_code, target_lang_name))
    return "\n\n".join(translated_chunks)

def build_translated_pdf(translated_text: str, original_filename: str, target_lang: str) -> bytes:
    """Build a PDF from translated text using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    
    font_name = "Helvetica"
    # Register Devanagari font
    font_path = os.path.join(os.path.dirname(__file__), "NotoSansDevanagari-Regular.ttf")
    if os.path.exists(font_path) and target_lang in ["Hindi", "Marathi", "Sanskrit", "Nepali"]:
        pdfmetrics.registerFont(TTFont('NotoSansDevanagari', font_path))
        font_name = 'NotoSansDevanagari'
    
    # Use a Unicode-capable built-in style
    body_style = ParagraphStyle(
        name="BhashaBody",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=12,
        leading=18,
        spaceAfter=8,
        wordWrap="CJK",  # handles Unicode scripts
    )
    title_style = ParagraphStyle(
        name="BhashaTitle",
        parent=styles["Heading1"],
        fontName=font_name,
        fontSize=14,
        spaceBefore=6,
        spaceAfter=10,
    )
    
    story = []
    story.append(Paragraph(f"BhashaAI Translation — {target_lang}", title_style))
    story.append(Paragraph(f"Source: {original_filename}", body_style))
    story.append(Spacer(1, 0.4*cm))
    
    for para in translated_text.split("\n"):
        para = para.strip()
        if para:
            # Escape HTML special chars for ReportLab
            para = para.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(para, body_style))
        else:
            story.append(Spacer(1, 0.3*cm))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.read()

@app.get("/")
def read_root():
    return {"message": "BhashaAI API is running"}

@app.post("/api/translate/text")
async def translate_text(request: TranslationRequest):
    """
    Endpoint for text translation using deep-translator.
    """
    source_code = LANGUAGE_MAP.get(request.source_lang, "auto")
    target_code = LANGUAGE_MAP.get(request.target_lang, "hi")
    
    try:
        # Pass target_lang_name to handle Hinglish and Bundelkhandi
        if request.target_lang == "Hinglish":
            translated = process_hinglish(request.text)
        else:
            translated = await asyncio.to_thread(
                translate_long_text,
                request.text,
                source_code,
                target_code,
                request.target_lang
            )
            
    except Exception as e:
        translated = f"Error during translation: {str(e)}"

    return {
        "source_text": request.text,
        "translated_text": translated,
        "source_lang": request.source_lang,
        "target_lang": request.target_lang
    }

@app.post("/api/translate/pdf")
async def translate_pdf(
    file: UploadFile = File(...),
    target_lang: str = Form("Hindi"),
    source_lang: str = Form("English"),
):
    """
    Real PDF translation: extract text → translate → build new PDF.
    """
    source_code = LANGUAGE_MAP.get(source_lang, "en")
    target_code = LANGUAGE_MAP.get(target_lang, "hi")

    # Read uploaded bytes and validate size (Max 10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    pdf_bytes = await file.read()
    
    if len(pdf_bytes) > MAX_FILE_SIZE:
        return {"status": "error", "message": "File size exceeds 10MB limit."}

    # Extract text using pdfplumber
    extracted_text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n\n"
    except Exception as e:
        return {"status": "error", "message": f"Could not read PDF: {str(e)}"}

    if not extracted_text.strip():
        return {"status": "error", "message": "No extractable text found in this PDF. It may be a scanned/image-only PDF."}

    # Translate the extracted text
    try:
        if target_lang == "Hinglish":
            translated_text = process_hinglish(extracted_text.strip())
        else:
            translated_text = await asyncio.to_thread(
                translate_long_text,
                extracted_text.strip(),
                source_code,
                target_code,
                target_lang
            )
                
    except Exception as e:
        return {"status": "error", "message": f"Translation failed: {str(e)}"}

    # Build translated PDF
    try:
        pdf_out = await asyncio.to_thread(
            build_translated_pdf,
            translated_text,
            file.filename or "document",
            target_lang
        )
    except Exception as e:
        return {"status": "error", "message": f"PDF generation failed: {str(e)}"}

    # Stream the PDF back
    base_name = (file.filename or "document").rsplit(".", 1)[0]
    download_name = f"{base_name}_{target_lang}_translated.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_out),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{download_name}"'}
    )

@app.get("/api/tts")
def text_to_speech(text: str, lang: str):
    """
    Proxy Google TTS requests to bypass CORS/referer blocks.
    """
    import urllib.request
    import urllib.parse
    from fastapi.responses import StreamingResponse

    google_lang_codes = {
        'English': 'en',
        'Hindi': 'hi',
        'Tamil': 'ta',
        'Telugu': 'te',
        'Kannada': 'kn',
        'Malayalam': 'ml',
        'Marathi': 'mr',
        'Gujarati': 'gu',
        'Bengali': 'bn',
        'Punjabi': 'pa',
        'Urdu': 'ur',
        'Odia': 'or',
        'Assamese': 'as',
        'Sanskrit': 'sa',
        'Nepali': 'ne',
        'Konkani': 'hi',
        'Manipuri': 'hi',
        'Sindhi': 'sd',
        'Bodo': 'hi',
        'Dogri': 'hi',
        'Maithili': 'hi',
        'Santali': 'hi',
        'Bhojpuri': 'hi',
        'Bundelkhandi': 'hi',
        'Awadhi': 'hi',
        'Magahi': 'hi',
        'Angika': 'hi',
        'Chhattisgarhi': 'hi',
        'Bagheli': 'hi',
        'Gondi': 'te',
        'Tulu': 'kn',
        'Hinglish': 'hi'
    }
    
    lang_code = google_lang_codes.get(lang, "hi")
    encoded_text = urllib.parse.quote(text)
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang_code}&client=tw-ob&q={encoded_text}"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'}
    )
    
    try:
        response = urllib.request.urlopen(req)
        def iterfile():
            while True:
                chunk = response.read(4096)
                if not chunk:
                    break
                yield chunk
        return StreamingResponse(iterfile(), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS Proxy Error: {str(e)}")

