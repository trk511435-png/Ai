from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import io
from PIL import Image

app = FastAPI()

# السماح للاتصال من أي موقع (مثل GitHub Pages الخاص بك)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "AI Server is running!"}

@app.post("/process-image")
async def process_image(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        # قراءة الصورة المرسلة من جهازك عبر الموقع
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        
        # -------------------------------------------------------------
        # هنا يتم تطبيق الذكاء الاصطناعي أو المعالجة بناءً على النص (prompt)
        # -------------------------------------------------------------
        # حالياً كمثال تجريبي، سنقوم بعكس ألوان الصورة أو تطبيق تعديل بسيط،
        # ويمكنك هنا ربط أي نموذج ذكاء اصطناعي تريده (مثل Stable Diffusion محلياً أو API خارجي).
        
        # مثال لتعديل تجريبي (تحويل الصورة إلى الأبيض والأسود إذا طلب المستخدم):
        if "أبيض وأسود" in prompt or "grayscale" in prompt.lower():
            img = img.convert("L")

        # حفظ النتيجة المؤقتة لإرجاعها
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="JPEG")
        output_buffer.seek(0)
        
        return {"message": "تم معالجة الصورة بنجاح بناءً على طلبك: " + prompt}
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
