# 1. Python bazaviy imidjdan boshlaymiz
FROM python:3.13-slim

# 2. Konteyner ichida ishchi papka yaratamiz
WORKDIR /app

# 3. Kerakli fayllarni konteynerga ko‘chiramiz
COPY requirements.txt .
COPY .env .env

# 4. Kutubxonalarni o‘rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# 5. Butun loyihani konteynerga nusxalaymiz
COPY . .

# 6. Django serverni ishga tushirish komandasi (dev uchun)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

