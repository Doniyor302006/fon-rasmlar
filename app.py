from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Faqat admin uchun parol
ADMIN_PASSWORD = "Doniyor06"

# Watermark qo‘shish funksiyasi
def add_watermark(image_path, watermark_text="DONIYOR"):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    # Watermark uchun shaffof qatlam yaratish
    txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Shrift sozlamalari (agar shrift faylingiz bo‘lmasa, standart ishlatiladi)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Matn o‘lchamini hisoblash
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Matnni rasmning pastki o‘ng burchagiga joylashtirish
    position = (width - text_width - 10, height - text_height - 10)
    draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))  # Oq rang, yarim shaffof

    # Asl rasmga watermark qo‘shish
    watermarked = Image.alpha_composite(image, txt_layer)
    watermarked = watermarked.convert("RGB")  # JPG uchun RGB ga o‘tkazish
    watermarked.save(image_path, "JPEG")

@app.route('/')
def index():
    images = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            file = request.files['file']
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)  # Avval rasmni saqlaymiz
                add_watermark(file_path, watermark_text="Mening Saytim")  # Watermark qo‘shamiz
                return redirect(url_for('index'))
        return "Noto‘g‘ri parol!"
    return render_template('upload.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5000, debug=True)
