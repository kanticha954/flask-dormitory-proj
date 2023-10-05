from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime, date
from pprint import pprint as pp
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
SHEET_NAME = "Kanticha Mansion"
output_folder = "image"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:/1_Work/Python-Proj/flask-cal-dormitory/image'
# Get data
def get_client(sheet_name=SHEET_NAME):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("GOOGLE_CRED.json", scope)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    client = client.open(sheet_name).sheet1
    data = client.get_all_records()
    pp(data)
    return client


@app.route("/")
def index():
    return render_template("add.html", room_count=3)


# create image
# def create_image(invoice_date, room_number, water_unit, electricity_unit, additional_type, additional_cost, total_cost):
def create_image(
    invoice_date,
    room_number,
    water_unit,
    electricity_unit,
    additional_type,
    additional_cost,
    total_cost,
):
    # image formatting
    img = Image.open("image/format_pic.png")
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/ChakraPetch-Medium.ttf", 18)  # ใช้ฟอนต์เริ่มต้น
    font_bold = ImageFont.truetype("fonts/ChakraPetch-Medium.ttf", 22)
    font_add = ImageFont.truetype("fonts/ChakraPetch-Medium.ttf", 16)

    # Mockup Data 
    # invoice_date = datetime.now().strftime("%b-%Y")
    # room_number = 1
    # water_unit = 9
    # electricity_unit = 8
    # water_cost = 25 * water_unit
    # electricity_cost = 8 * electricity_unit
    # additional_type = "เพิ่มเติม"
    # additional_cost = 200

    # total_cost = int(2500 + water_cost + electricity_cost + additional_cost)

    # draw image (x,y)
    d.text((40, 80), f"{invoice_date}", fill=(0, 0, 0), font=font_bold)
    d.text((280, 80), f"Room {room_number}", fill=(0, 0, 0), font=font_bold)
    d.text((310, 215), f"{water_unit}", fill=(0, 0, 0), font=font)
    d.text((310, 268), f"{electricity_unit}", fill=(0, 0, 0), font=font)
    d.text((50, 340), f"{additional_type}", fill=(28, 156, 238), font=font_add)
    d.text((310, 340), f"{additional_cost}", fill=(28, 156, 238), font=font_add)
    d.text((300, 385), f"{total_cost}", fill=(0, 0, 0), font=font)

    # save
    save_folder = output_folder
    save_path = os.path.join(save_folder, f"result_room_{room_number}.png")
    img.save(save_path)

    print("บันทึกรูปภาพเสร็จสิ้น")
    return save_path


@app.route("/saveData", methods=["POST"])
def save_single_room():
    room_count = int(request.form["room_count"])

    for room_number in range(1, room_count + 1):
        water_unit_key = f"water_unit_{room_number}"
        electricity_unit_key = f"electricity_unit_{room_number}"
        additional_type_key = f"additional_type_{room_number}"
        additional_cost_key = f"additional_cost_{room_number}"
        
        try:
            water_unit = int(request.form[water_unit_key])
        except ValueError:
            water_unit = 0
        try:
            electricity_unit = int(request.form[electricity_unit_key])
        except ValueError:
            electricity_unit = 0
        try:
            additional_type = request.form[additional_type_key]
        except ValueError:
            additional_type = "ไม่มี"
        try:
            additional_cost = float(request.form[additional_cost_key])
        except ValueError:
            additional_cost = 0


        invoice_date = datetime.now().strftime("%b-%Y")
        water_rate = 25
        electricity_rate = 8
        water_cost = water_rate * water_unit
        electricity_cost = electricity_rate * electricity_unit

        total_cost = int(2500 + water_cost + electricity_cost + additional_cost)

        create_image(
            invoice_date,
            room_number,
            water_cost,
            electricity_cost,
            additional_type,
            additional_cost,
            total_cost,
        )
        print(f'รูปภาพห้องที่ {room_number} ถูกบันทึกแล้ว')

    return "รูปภาพถูกบันทึกเรียบร้อย"

@app.route("/", methods=["POST"])
def add_water_electricity():
    room_count = int(request.form["room_count"])
    client = get_client()

    for room_number in range(1, room_count + 1):
        water_unit_key = f"water_unit_{room_number}"
        electricity_unit_key = f"electricity_unit_{room_number}"
        additional_type_key = f"additional_type_{room_number}"
        additional_cost_key = f"additional_cost_{room_number}"

        invoice_status = request.form.get(f"invoice_status_{room_number}", "none")
        
        try:
            water_unit = int(request.form[water_unit_key])
        except ValueError:
            water_unit = 0
        try:
            electricity_unit = int(request.form[electricity_unit_key])
        except ValueError:
            electricity_unit = 0
        try:
            additional_type = request.form[additional_type_key]
        except ValueError:
            additional_type = "ไม่มี"
        try:
            additional_cost = float(request.form[additional_cost_key])
        except ValueError:
            additional_cost = 0

        invoice_date = datetime.now().strftime("%b-%Y")
        water_rate = 25
        electricity_rate = 8
        water_cost = water_rate * water_unit
        electricity_cost = electricity_rate * electricity_unit

        total_cost = int(2500 + water_cost + electricity_cost + additional_cost)

        create_image(
            invoice_date,
            room_number,
            water_cost,
            electricity_cost,
            additional_type,
            additional_cost,
            total_cost,
        )
        print("f'รูปภาพถูกบันทึกเรียบร้อย'")
        print(room_number)

        client.append_row(
            [
                "",
                room_number,
                "",
                invoice_status,
                datetime.now().strftime("%b-%Y"),
                water_unit,
                electricity_unit,
                additional_type,
                additional_cost,
                total_cost,
            ]
        )

    return "บันทึกข้อมูลเสร็จสิ้น!"

@app.route('/image/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/show_images')
def show_images():
    room_count = 3
    image_paths = [f'result_room_{room_number}.png' for room_number in range(1, room_count + 1)]
    return render_template('show_images.html', image_paths=image_paths)


#test function
@app.route("/save", methods=["POST"])
def save_data():
    room_count = int(request.form["room_count"])
    for room_number in range(1, room_count + 1):
        water_cost_key = f"water_cost_{room_number}"
        electricity_cost_key = f"electricity_cost_{room_number}"

        try:
            water_unit = float(request.form[water_cost_key])
        except ValueError:
            water_unit = 0
        try:
            electricity_unit = float(request.form[electricity_cost_key])
        except ValueError:
            electricity_unit = 0

        water_rate = 25
        electricity_rate = 8

        water_cost = water_rate * water_unit
        electricity_cost = electricity_rate * electricity_unit

        img = Image.new("RGB", (800, 600), color=(255, 200, 200))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/THSarabun.ttf", 30)  # Choose a stylish font

        d.text((100, 20), f"ห้องหมายเลข: {room_number}", font=font, fill=(0, 0, 0))
        d.text((100, 60), f"น้ำ: {water_cost} Baht", font=font, fill=(0, 0, 0))
        d.text((100, 100), f"ค่าไฟ: {electricity_cost} Baht", font=font, fill=(0, 0, 0))

        # Save the image
        save_folder = "D:/1_Work/Python-Proj/flask-cal-dormitory/image"
        save_path = os.path.join(save_folder, f"result_room_{room_number}.png")
        img.save(save_path)
        print(request.form)

    return "บันทึกข้อมูลและรูปภาพเรียบร้อย"


if __name__ == "__main__":
    # create_image()
    app.run(debug=True)
