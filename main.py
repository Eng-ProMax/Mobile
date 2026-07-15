import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI(
    title="API أسعار الهواتف والمجهزين في العراق",
    description="سيرفر مركزي متطور لجلب أسعار الأجهزة والمجهزين مباشرة من قاعدة بيانات Supabase",
    version="1.0.0"
)

# السماح لجميع التطبيقات والمواقع بالاتصال بالسيرفر بدون حظر (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# جلب روابط الاتصال بشكل آمن من السيرفر المستضيف
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# إنشاء الاتصال بقاعدة البيانات
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/", tags=["الرئيسية"])
def read_root():
    return {
        "status": "online",
        "message": "مرحباً بك في سيرفر أسعار الهواتف العراقي التجريبي",
        "docs_url": "/docs"
    }

@app.get("/products", tags=["المنتجات والأسعار"])
def get_all_products():
    """جلب جميع الأجهزة مع أسعارها وتفاصيل المجهزين لها من قاعدة البيانات"""
    try:
        response = supabase.table("Products").select(
            "product_name, brand, storage_size, current_price_usd, Suppliers(supplier_name, city, location_details)"
        ).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
