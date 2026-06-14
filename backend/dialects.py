import re

# Fallbacks for low-resource languages that map to a base language supported by Google Translate
DIALECT_FALLBACKS = {
    "Tulu": "kn",
    "Bhili": "hi",
    "Gondi": "hi",
    "Saurashtra": "ta",
    "Bundelkhandi": "hi",
    "Bhojpuri": "hi",
    "Hinglish": "en", # We process Hinglish via rules on top of English/Hindi
}

# Bundelkhandi mappings (English -> Bundelkhandi)
BUNDELKHANDI_DICT = {
    # 1. Greetings and Basic Expressions
    "hello": "राम-राम",
    "good morning": "राम-राम",
    "good evening": "राम-राम",
    "how are you": "तुम कैसे हो?",
    "i am fine": "हम ठीक हैं।",
    "thank you": "धन्यबाद।",
    "you're welcome": "कोई बात नइ।",
    "youre welcome": "कोई बात नइ।",
    "please": "कृपा करके",
    "sorry": "माफ करियो।",
    "excuse me": "सुनो ज़रा।",
    "yes": "हाँ",
    "no": "नइ",
    "okay": "ठीक है",
    "very good": "बहुत बढ़िया",
    "welcome": "स्वागत है",

    # 2. Family Words
    "father": "बाबू / बाप",
    "mother": "अम्मा / माई",
    "brother": "भैया",
    "sister": "बहिनी",
    "son": "बेटा",
    "daughter": "बिटिया",
    "grandfather": "दद्दा",
    "grandmother": "दद्दी",
    "husband": "मड़वा",
    "wife": "घरवाली",
    "family": "परिवार",

    # 3. Daily Actions
    "come": "आओ",
    "come here": "इत्ते आओ",
    "go": "जाओ",
    "go there": "उत्ते जाओ",
    "sit": "बैठो",
    "sit here": "इत्ते बैठो",
    "stand up": "खड़े हो जाओ",
    "eat": "खाओ",
    "drink": "पियो",
    "sleep": "सो जाओ",
    "wake up": "उठ जाओ",
    "run": "दौड़ो",
    "walk": "चलो",
    "listen": "सुनो",
    "speak": "बोलो",
    "wait": "रुको",

    # 4. Common Questions
    "what is your name": "तुम्हार नाम का है?",
    "where are you going": "तुम कहाँ जात हो?",
    "what are you doing": "तुम का करत हो?",
    "where do you live": "तुम कहाँ रहत हो?",
    "how old are you": "तुम्हारी उमर कित्ती है?",
    "who is this": "ई कौन है?",
    "why are you crying": "तुम काहे रोवत हो?",
    "when will you come": "तुम कब आओगे?",
    "can you help me": "का तुम हमाई मदद कर सकत हो?",
    "do you understand": "तुम समझे कि नइ?",

    # 5. Food and Kitchen
    "food": "खाना",
    "water": "पानी",
    "tea": "चाय",
    "milk": "दूध",
    "rice": "चावल",
    "wheat": "गेहूँ",
    "bread": "रोटी",
    "vegetables": "तरकारी",
    "salt": "नमक",
    "sugar": "चीनी",
    "eat food": "खाना खाओ",
    "drink water": "पानी पियो",
    "the food is tasty": "खाना बढ़िया है",

    # 6. Home Vocabulary
    "house": "घर",
    "room": "कमरा",
    "door": "दरवाजा",
    "window": "खिड़की",
    "bed": "बिछौना",
    "chair": "कुर्सी",
    "table": "मेज",
    "fan": "पंखा",
    "light": "बत्ती",
    "kitchen": "रसोई",

    # 7. Common Commands
    "open the door": "दरवाजा खोलो",
    "close the door": "दरवाजा बंद करो",
    "turn on the light": "बत्ती जला दो",
    "turn off the light": "बत्ती बुझा दो",
    "wash your hands": "हाथ धो लो",
    "do your work": "अपनो काम करो",
    "study properly": "ढंग से पढ़ो",
    "speak slowly": "धीरे बोलो",
    "come quickly": "जल्दी आओ",
    "be careful": "ध्यान से",

    # 8. Time and Days
    "today": "आज",
    "tomorrow": "कल",
    "yesterday": "कल",
    "morning": "सवेर",
    "afternoon": "दुपहर",
    "evening": "साँझ",
    "night": "रात",
    "now": "अब",
    "later": "बाद में",
    "early": "जल्दी",

    # 9. Numbers
    "one": "एक",
    "two": "दुई",
    "three": "तीन",
    "four": "चार",
    "five": "पाँच",
    "six": "छः",
    "seven": "सात",
    "eight": "आठ",
    "nine": "नौ",
    "ten": "दस",

    # 10. Health Sentences
    "i have a fever": "हमका बुखार है।",
    "i have a headache": "हमार सिर दुखत है।",
    "call the doctor": "डॉक्टर बुलाओ।",
    "take this medicine": "ई दवाई ले लो।",
    "drink more water": "ज्यादा पानी पियो।",
    "rest for some time": "थोड़ी देर आराम करो।",
    "are you feeling better": "अब ठीक लग रहो है?",

    # 11. Emergency Sentences
    "help me": "हमाई मदद करो!",
    "call the police": "पुलिस बुलाओ!",
    "call an ambulance": "एम्बुलेंस बुलाओ!",
    "there is a fire": "आग लग गई!",
    "i am in danger": "हम मुसीबत में हैं।",
    "save the child": "बच्चा बचाओ!",
    "stay calm": "घबराओ मत।",

    # 12. Agriculture Vocabulary
    "farmer": "किसान",
    "field": "खेत",
    "crop": "फसल",
    "water the field": "खेत में पानी दो",
    "harvest the crop": "फसल काटो",
    "seeds": "बीज",
    "fertilizer": "खाद",
    "tractor": "ट्रैक्टर",
    "rain": "बरसात",
    "plough": "हल",

    # 13. Emotional Expressions
    "i am happy": "हम खुश हैं।",
    "i am sad": "हम दुखी हैं।",
    "i am tired": "हम थक गए हैं।",
    "do not worry": "चिंता मत करो।",
    "congratulations": "बधाई हो!",
    "best wishes": "शुभकामनाएँ।",
    "i miss you": "तुमाई याद आवत है।",

    # 14. Important Pronouns
    "i": "हम",
    "you": "तुम",
    "he": "ऊ",
    "she": "ऊ",
    "we": "हम",
    "they": "ऊ लोग",
    "this": "ई",
    "that": "ऊ",
    "here": "इत्ते",
    "there": "उत्ते",

    # 15. Grammar Patterns
    "i am going home": "हम घर जात हैं।",
    "he is eating food": "ऊ खाना खावत है।",
    "she is sleeping": "ऊ सोवत है।",
    "we are working": "हम काम करत हैं।",
    "they are playing": "ऊ खेलत हैं।",

    # Preserving the old Hindi mappings just in case
    "इधर आओ": "इत्ते आओ",
    "यहाँ आओ": "इत्ते आओ",
    "तुम कहाँ जा रहे हो": "तुम कहाँ जात हो?",
    "यहाँ बैठो": "इत्ते बैठो",
    "तुम क्या कर रहे हो": "तुम का करत हो?",
    "मैं ठीक हूँ": "हम ठीक हैं।",
}

# Hinglish mappings
HINGLISH_PRESERVE = {
    "implementation", "authentication", "framework", "documentation",
    "algorithm", "database", "server", "machine learning", "cybersecurity",
    "api", "deployment", "compliance", "infrastructure", "project", "application"
}

HINGLISH_DICT = {
    "i": "main",
    "you": "tum",
    "we": "hum",
    "come": "aao",
    "go": "jao",
    "do": "karo",
    "before": "se pehle",
    "after": "ke baad",
    "with": "ke saath",
    "for": "ke liye",
    "is": "hai",
    "are": "hain",
    "was": "tha",
    "this": "yeh",
    "that": "woh",
    "what": "kya",
    "why": "kyun",
    "how": "kaise",
    "can you explain": "kya tum explain kar sakte ho",
    "has introduced": "ne introduce kiya hai",
    "a new": "ek naya",
    "please complete": "please complete kar lo",
    "submitting": "submit karne",
    "the": "" # often dropped in Hinglish
}

def process_bundelkhandi(text: str, base_translated: str) -> str:
    """Apply Bundelkhandi dictionary replacements on top of Hindi translation."""
    import re
    # Try direct English phrase match first
    text_lower = text.lower().strip().replace('?', '').replace('.', '').replace('!', '')
    if text_lower in BUNDELKHANDI_DICT:
        return BUNDELKHANDI_DICT[text_lower]
        
    # Try phrase-by-phrase replacement on the English text
    english_replaced = text.lower()
    phrases = sorted(BUNDELKHANDI_DICT.keys(), key=lambda x: len(x), reverse=True)
    for phrase in phrases:
        if phrase:  # Ensure not empty
            pattern = re.compile(r'\b' + re.escape(phrase) + r'\b')
            english_replaced = pattern.sub(BUNDELKHANDI_DICT[phrase], english_replaced)
            
    # If the text was fully translated by dictionary (no English letters left)
    if not re.search(r'[a-z]', english_replaced):
        return re.sub(r'\s+', ' ', english_replaced).strip()
        
    # Fallback: Apply standard replacements to the Hindi text
    result = base_translated
    for standard, bundel in BUNDELKHANDI_DICT.items():
        if standard in result:
            result = result.replace(standard, bundel)
            
    return result

def process_hinglish(text: str) -> str:
    """
    Rule-based Hinglish translation: 
    Preserves technical terms, replaces common phrases with Romanised Hindi.
    """
    # Simple rule-based translation for Hinglish
    result = text
    
    # Process multi-word phrases first
    phrases = sorted(HINGLISH_DICT.keys(), key=lambda x: len(x.split()), reverse=True)
    
    for phrase in phrases:
        # Case insensitive replacement, word boundary
        pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
        replacement = HINGLISH_DICT[phrase]
        if replacement == "":
            # If removing a word like "the", ensure we don't leave double spaces
            result = pattern.sub(replacement, result)
            result = re.sub(r'\s+', ' ', result).strip()
        else:
            result = pattern.sub(replacement, result)
            
    return result

# ==========================================
# Bhojpuri Mappings (English -> Bhojpuri)
# ==========================================
BHOJPURI_DICT = {
    # 1. Greetings and Basic Expressions
    "hello": "प्रणाम / राम-राम",
    "good morning": "प्रणाम",
    "good evening": "प्रणाम",
    "good night": "शुभ रात्रि",
    "how are you": "का हाल बा?",
    "i am fine": "हम ठीक बानी।",
    "nice to meet you": "रउरा से मिल के खुशी भइल।",
    "what is your name": "रउरा के नाम का बा?",
    "my name is ayush": "हमार नाम आयुष बा।",
    "thank you": "धन्यवाद।",
    "you're welcome": "कवनो बात नइखे।",
    "youre welcome": "कवनो बात नइखे।",
    "please": "कृपया",
    "sorry": "माफ करीं।",
    "excuse me": "सुनीं जरा।",
    "yes": "हँ",
    "no": "ना",
    "okay": "ठीक बा",
    "very good": "बहुत बढ़िया",
    "welcome": "स्वागत बा",
    "see you later": "फेरु मिलब।",

    # 2. Family Words
    "father": "बाबूजी / पिता",
    "mother": "माई / माता",
    "brother": "भाई",
    "sister": "बहिन",
    "son": "बेटा",
    "daughter": "बेटी",
    "grandfather": "दादा",
    "grandmother": "दादी",
    "husband": "पति",
    "wife": "मेहरारू",
    "family": "परिवार",

    # 3. Daily Actions
    "come": "आवा",
    "come here": "एहिजा आवा",
    "go": "जा",
    "go there": "ओहिजा जा",
    "sit": "बइठा",
    "sit here": "एहिजा बइठा",
    "stand up": "खड़ा हो जा",
    "eat": "खा",
    "drink": "पिया",
    "sleep": "सूत जा",
    "wake up": "उठ जा",
    "run": "दौड़ा",
    "walk": "चला",
    "listen": "सुना",
    "speak": "बोला",
    "wait": "रुकs",
    "open": "खोला",
    "close": "बंद करा",

    # 4. Common Questions
    "where are you going": "तू कहाँ जात बाड़ऽ?",
    "what are you doing": "तू का करत बाड़ऽ?",
    "where do you live": "तू कहाँ रहत बाड़ऽ?",
    "how old are you": "रउरा के उमिर कतना बा?",
    "who is this": "ई के बा?",
    "why are you crying": "तू काहे रोवत बाड़ऽ?",
    "when will you come": "तू कब अइबऽ?",
    "can you help me": "का तू हमार मदद कर सकत बाड़ऽ?",
    "do you understand": "रउरा समझत बानी?",

    # 5. Food and Kitchen
    "food": "खाना",
    "water": "पानी",
    "tea": "चाय",
    "milk": "दूध",
    "rice": "भात",
    "wheat": "गेहूँ",
    "bread": "रोटी",
    "vegetables": "तरकारी",
    "salt": "नून",
    "sugar": "चीनी",
    "eat food": "खाना खा",
    "drink water": "पानी पिया",
    "the food is tasty": "खाना स्वादिष्ट बा।",

    # 6. Home Vocabulary
    "house": "घर",
    "room": "कमरा",
    "door": "दरवाजा",
    "window": "खिड़की",
    "bed": "खाट / बिस्तर",
    "chair": "कुर्सी",
    "table": "मेज",
    "fan": "पंखा",
    "light": "बत्ती",
    "kitchen": "रसोई",

    # 7. Common Commands
    "open the door": "दरवाजा खोला",
    "close the door": "दरवाजा बंद करा",
    "turn on the light": "बत्ती जला",
    "turn off the light": "बत्ती बुझा",
    "wash your hands": "हाथ धो लऽ",
    "do your work": "आपन काम करा",
    "study properly": "ढंग से पढ़ऽ",
    "speak slowly": "धीरे बोला",
    "come quickly": "जल्दी आवा",
    "be careful": "सावधान रहा",

    # 8. Time and Days
    "today": "आज",
    "tomorrow": "काल्ह",
    "yesterday": "काल्ह",
    "morning": "बिहान",
    "afternoon": "दुपहर",
    "evening": "साँझ",
    "night": "रात",
    "now": "अब",
    "later": "बाद में",
    "early": "जल्दी",

    # 9. Numbers
    "one": "एक",
    "two": "दू",
    "three": "तीन",
    "four": "चार",
    "five": "पाँच",
    "six": "छः",
    "seven": "सात",
    "eight": "आठ",
    "nine": "नौ",
    "ten": "दस",

    # 10. Health Sentences
    "i have a fever": "हमरा बुखार बा।",
    "i have a headache": "हमार सिर दुखत बा।",
    "call the doctor": "डॉक्टर के बोलावा।",
    "take this medicine": "ई दवाई ले लऽ।",
    "drink more water": "जादा पानी पिया।",
    "rest for some time": "थोड़ा आराम करा।",
    "are you feeling better": "अब ठीक लागत बा?",
    "go to the hospital": "अस्पताल जा।",
    "the patient is stable": "मरीज के हालत ठीक बा।",
    "take care of your health": "आपन स्वास्थ्य के ध्यान रखऽ।",

    # 11. Emergency Sentences
    "help me": "हमार मदद करा!",
    "call the police": "पुलिस के बोलावा!",
    "call an ambulance": "एम्बुलेंस बोलावा!",
    "there is a fire": "आग लग गइल बा!",
    "i am in danger": "हम खतरा में बानी।",
    "save the child": "बच्चा के बचावा!",
    "stay calm": "घबराईं मत।",
    "inform my family": "हमार परिवार के खबर दऽ।",
    "i need immediate help": "हमरा तुरंत मदद चाहीं।",
    "someone is injured": "केहू घायल बा।",

    # 12. Agriculture Vocabulary
    "farmer": "किसान",
    "field": "खेत",
    "crop": "फसल",
    "water the field": "खेत में पानी दऽ",
    "harvest the crop": "फसल काटऽ",
    "seeds": "बीया",
    "fertilizer": "खाद",
    "tractor": "ट्रैक्टर",
    "rain": "बरखा",
    "plough": "हल",
    "sell the produce": "उपज बेचऽ",
    "prepare the field": "खेत तैयार करा",

    # 13. Emotional Expressions
    "i am happy": "हम खुश बानी।",
    "i am sad": "हम दुखी बानी।",
    "i am tired": "हम थक गइल बानी।",
    "do not worry": "चिंता मत करा।",
    "congratulations": "बधाई हो!",
    "best wishes": "शुभकामना!",
    "i miss you": "रउरा के याद आवत बा।",
    "i am excited": "हम बहुत उत्साहित बानी।",
    "everything will be fine": "सब ठीक हो जाई।",
    "don't cry": "मत रोअ।",
    "dont cry": "मत रोअ।",

    # 14. Important Pronouns
    "i": "हम",
    "you": "तू",
    "he": "ऊ",
    "she": "ऊ",
    "we": "हमनी",
    "they": "ऊ लोग",
    "this": "ई",
    "that": "ऊ",
    "here": "एहिजा",
    "there": "ओहिजा",

    # 15. Grammar Patterns
    "i am going home": "हम घर जात बानी।",
    "he is eating food": "ऊ खाना खात बा।",
    "she is sleeping": "ऊ सूतल बा।",
    "we are working": "हमनी काम करत बानी।",
    "they are playing": "ऊ लोग खेलत बाड़ें।",
    "i have eaten": "हम खा लिहनी।",
    "i cannot go": "हम ना जा सकी।",

    # 16. Women's Safety
    "please share my location": "कृपया हमार लोकेशन भेज दीं।",
    "inform my family members": "हमार परिवार के खबर दीं।",
    "call the emergency number": "आपातकालीन नंबर पर फोन करीं।",
    "i am being followed": "केहू हमार पीछा करत बा।",
    "i feel unsafe": "हमरा सुरक्षित ना लागत बा।",
    "send an sos alert": "SOS संदेश भेजीं।",
    "contact the nearest police station": "नजदीकी थाना से संपर्क करीं।",
    "stay on the phone with me": "फोन मत काटीं।",
    "help is on the way": "मदद रास्ता में बा।",

    # 17. Negation Patterns
    "i am not going": "हम ना जात बानी।",
    "he is not eating": "ऊ ना खात बा।",
    "she cannot come": "ऊ ना आ सकी।",
    "we do not understand": "हमनी ना समझत बानी।",
    "they are not playing": "ऊ लोग ना खेलत बाड़ें।",

    # 18. Future Tense
    "i will come tomorrow": "हम काल्ह अइब।",
    "he will help you": "ऊ रउरा मदद करी।",
    "she will cook food": "ऊ खाना बनाई।",
    "we will visit you": "हमनी रउरा लगे अइब।",
    "they will arrive soon": "ऊ लोग जल्दी अइहे।",

    # 19. Past Tense
    "i went home": "हम घर गइल रहीं।",
    "he ate food": "ऊ खाना खइलस।",
    "she cooked food": "ऊ खाना बनवली।",
    "we worked hard": "हमनी मेहनत कईनी।",
    "they played cricket": "ऊ लोग क्रिकेट खेललें।",
}

def process_bhojpuri(text: str, base_translated: str) -> str:
    """Apply Bhojpuri dictionary replacements on top of Hindi translation."""
    import re
    # Try direct English phrase match first
    text_lower = text.lower().strip().replace('?', '').replace('.', '').replace('!', '')
    if text_lower in BHOJPURI_DICT:
        return BHOJPURI_DICT[text_lower]
        
    # Try phrase-by-phrase replacement on the English text
    english_replaced = text.lower()
    phrases = sorted(BHOJPURI_DICT.keys(), key=lambda x: len(x), reverse=True)
    for phrase in phrases:
        if phrase:
            pattern = re.compile(r'\b' + re.escape(phrase) + r'\b')
            english_replaced = pattern.sub(BHOJPURI_DICT[phrase], english_replaced)
            
    # If the text was fully translated by dictionary (no English letters left)
    if not re.search(r'[a-z]', english_replaced):
        return re.sub(r'\s+', ' ', english_replaced).strip()
        
    # Fallback: Apply standard replacements to the Hindi text
    result = base_translated
    for standard, bhojpuri in BHOJPURI_DICT.items():
        if standard in result:
            result = result.replace(standard, bhojpuri)
            
    return result
