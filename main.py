from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io
from PIL import Image, ImageEnhance, ImageOps

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Real AI Image Processing Server is running!"}

@app.post("/process-image")
async def process_image(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        # قراءة الصورة المرفوعة
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        
        prompt_lower = prompt.lower()
        
        # تنفيذ التعديلات بناءً على كتابتك في الموقع
        if "أبيض وأسود" in prompt or "grayscale" in prompt_lower:
            img = ImageOps.grayscale(img).convert("RGB")
            
        elif "عكس" in prompt or "inhibit" in prompt_lower or "negative" in prompt_lower:
            img = ImageOps.invert(img)
            
        elif "تفتيح" in prompt or "bright" in prompt_lower:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.5) # زيادة السطوع بنسبة 50%
            
        elif "تغميق" in prompt or "dark" in prompt_lower:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.5)
            
        elif "تباين" in prompt or "contrast" in prompt_lower:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            
        elif "تدوير" in prompt or "rotate" in prompt_lower:
            img = img.rotate(90, expand=True)
            
        elif "قلب" in prompt or "mirror" in prompt_lower:
            img = ImageOps.mirror(img)
            
        else:
            # إذا كتب أي أمر آخر، سنقوم بزيادة تشبع الألوان كافتراضي للتعديل
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.8)

        # حفظ الصورة المعدلة وإرجاعها مباشرة للموقع لعرضها
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="JPEG")
        output_buffer.seek(0)
        
        return StreamingResponse(output_buffer, media_type="image/jpeg")
    
    except Exception as e:
        return {"error": str(e)}
