from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_data():
    water_rate = 4
    electricity_rate = 11
    water_unit = float(request.form['water_cost'])
    electricity_unit = float(request.form['electricity_cost'])
    
    water_cost = water_unit * water_rate
    electricity_cost = electricity_unit * electricity_rate
    
    
     # Create a beautiful template using Pillow
    img = Image.new('RGB', (800, 600), color=(255, 200, 200))  # Background color
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/THSarabun.ttf", 36)  # Choose a stylish font
    
    # Draw text on the image
    d.text((100,50), f'ค่าน้ำ: {water_cost} Baht', font=font, fill=(0, 0, 0))
    d.text((100, 100), f'ค่าไฟ: {electricity_cost} Baht', font=font, fill=(0, 0, 0))

    # Save the image using UTF-8 encoding
    img.save('result.png', 'PNG', encoding='utf-8')  # Specify encoding here

    return 'save image success'

if __name__ == '__main__':
    app.run(debug=True)
