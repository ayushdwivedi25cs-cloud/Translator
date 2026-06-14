import requests

with open("test.pdf", "wb") as f:
    # Let's create a minimal PDF
    from reportlab.pdfgen import canvas
    c = canvas.Canvas("dummy.pdf")
    c.drawString(100, 750, "Hello world, this is a test.")
    c.save()

with open("dummy.pdf", "rb") as f:
    files = {"file": ("dummy.pdf", f, "application/pdf")}
    data = {"source_lang": "English", "target_lang": "Hindi"}
    r = requests.post("http://localhost:8001/api/translate/pdf", files=files, data=data)

with open("output.pdf", "wb") as f:
    f.write(r.content)

print(r.status_code)
print(r.headers.get("content-type"))
