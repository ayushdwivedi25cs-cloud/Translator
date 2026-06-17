import re

file_path = r"c:\Users\Aarambh Arun\OneDrive\Documents\Translator\frontend\index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the file-target-lang select
old_pattern = r'<select id="file-target-lang">\s*<option value="Hindi" selected>Hindi \(हिंदी\)</option>\s*<option value="Tamil">Tamil \(തമിഴ്\)</option>\s*<option value="Telugu">Telugu \(తెలుగు\)</option>\s*<option value="Kannada">Kannada \(ಕನ್ನಡ\)</option>\s*<option value="Malayalam">Malayalam \(മലയാളം\)</option>\s*</select>'

new_select = '''<select id="file-target-lang">
                            <optgroup label="International">
                                <option value="English">English</option>
                            </optgroup>
                            <optgroup label="Major Languages">
                                <option value="Hindi" selected>Hindi (हिंदी)</option>
                                <option value="Tamil">Tamil (தமிழ்)</option>
                                <option value="Telugu">Telugu (తెలుగు)</option>
                                <option value="Kannada">Kannada (ಕನ್ನಡ)</option>
                                <option value="Malayalam">Malayalam (മലയാളം)</option>
                                <option value="Marathi">Marathi (मराठी)</option>
                                <option value="Gujarati">Gujarati (ગુજરાતી)</option>
                                <option value="Bengali">Bengali (বাংলা)</option>
                                <option value="Punjabi">Punjabi (ਪੰਜਾਬੀ)</option>
                                <option value="Urdu">Urdu (اردو)</option>
                                <option value="Odia">Odia (ଓଡ଼ିଆ)</option>
                                <option value="Assamese">Assamese (असमीय)</option>
                            </optgroup>
                            <optgroup label="Other Languages">
                                <option value="Sanskrit">Sanskrit (संस्कृत)</option>
                                <option value="Nepali">Nepali (नेपाली)</option>
                                <option value="Konkani">Konkani (कोंकणी)</option>
                                <option value="Manipuri">Manipuri (ମଣିପୁରୀ)</option>
                                <option value="Sindhi">Sindhi (سنڌي)</option>
                                <option value="Bodo">Bodo (बड़ो)</option>
                                <option value="Dogri">Dogri (डोगरी)</option>
                                <option value="Maithili">Maithili (मैथिली)</option>
                                <option value="Santali">Santali (ᱥᱟᱱᱛᱟᱞᱤ)</option>
                            </optgroup>
                            <optgroup label="Dialects">
                                <option value="Bhojpuri">Bhojpuri (भोजपुरी)</option>
                                <option value="Bundelkhandi">Bundelkhandi (बुंदेलखंडी)</option>
                                <option value="Awadhi">Awadhi (अवधी)</option>
                                <option value="Magahi">Magahi (मगही)</option>
                                <option value="Angika">Angika (अंगिका)</option>
                                <option value="Chhattisgarhi">Chhattisgarhi (छत्तीसगढ़ी)</option>
                                <option value="Bagheli">Bagheli (बघेली)</option>
                                <option value="Gondi">Gondi (गोंडी)</option>
                                <option value="Tulu">Tulu (ತುಳು)</option>
                            </optgroup>
                        </select>'''

content = re.sub(old_pattern, new_select, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Documents section updated with English and all languages!")
