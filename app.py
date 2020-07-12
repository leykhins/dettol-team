from threading import Timer
import os
from urllib.parse import urljoin
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, url_for, redirect

app = Flask(__name__)
BASE_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(BASE_PATH, "static")
FONT_PATH = os.path.join(STATIC_PATH, "fonts")
CERTIFICATE_PATH = os.path.join(STATIC_PATH, "certificates")
GENERATED_PATH = os.path.join(STATIC_PATH, "generated")

@app.route("/")
def index():
    return "Hello World"


@app.route("/generate/")
def generate():
    certificate = make_certificate(**request.args)
    return redirect(certificate)

def delete_file(img_title):
    os.unlink(os.path.join(GENERATED_PATH, img_title))

def make_certificate(username, number):
    # set certificate style
    font = "PTSans-Bold.ttf"
    track_font = "LeagueSpartan-Bold.otf"

    # name style
    color = "#ffffff"
    size = 58
    y = 676

    # track style
    track_color = "#ffffff"
    track_size = 70

    # name text
    text = "{}".format(username).upper()
    raw_img = Image.open(os.path.join(CERTIFICATE_PATH, "jersey.jpeg"))
    img = raw_img.copy()
    draw = ImageDraw.Draw(img)

    # draw name
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, font), size)
    w, h = draw.textsize(text, font=PIL_font)
    W, H = img.size
    print(w)
    x = 382.603000431 +  ((272.780888595 - w) / 2)
    draw.text((x, y), text, fill=color, font=PIL_font)

    # draw number
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, track_font), track_size)
    track_text = "{}".format(number)
    w, h = draw.textsize(track_text, font=PIL_font)
    W, H = img.size
    x = 385.431 + ((269.000 - w) / 2)
    y = 796.871
    draw.text((x, y), track_text, fill=track_color, font=PIL_font)

    # save certificate
    img_title = "{}-{}.png".format(username, number)
    img.save(os.path.join(GENERATED_PATH, img_title))
    task = Timer(30, delete_file, (img_title,))
    task.start()
    base_64 =  urljoin(request.host_url, url_for("static", filename="generated/" + img_title))

    return base_64
# def make_certificate(username, jerseynumber, type, track=None):
#     def draw_text(filename, type, username, jerseynumber, track=None):
#         font = "PTSans-Bold.ttf"
#         color = "#ff0000"
#         size = 50
#         track_color = "#000000"
#         track_size = 20
#         y = 350
#         x = 0
#         text = "{} {}".format(username, jerseynumber).upper()
#         if type == "2":
#             font = "LeagueSpartan-Bold.otf"
#             size = 60
#             color = "#e05a47"
#             y = 175
#             x = 88
#             text = "{}\n{}".format(username, jerseynumber).upper()
#         raw_img = Image.open(os.path.join("certificates", filename))
#         img = raw_img.copy()
#         draw = ImageDraw.Draw(img)

#         # draw name
#         if username:
#             PIL_font = ImageFont.truetype(os.path.join("fonts", font), size)
#             w, h = draw.textsize(text, font=PIL_font)
#             W, H = img.size
#             x = (W - w) / 2 if x == 0 else x
#             draw.text((x, y), text, fill=color, font=PIL_font)
#         img_url = os.path.join("static", "{}-{}-Join-Me-On-The-Cool-Team.png".format(username, jerseynumber, type))
#         img.save(img_url)
#         return request.host_url + img_url

#2
        # draw track
        #if track:
        #    PIL_font = ImageFont.truetype(os.path.join("fonts", font), track_size)
        #    w, h = draw.textsize(track, font=PIL_font)
        #    x, y = 183, 450
        #    draw.text((x, y), track, fill=track_color, font=PIL_font)
        #img_url = os.path.join("static", "{}-{}-{}-Join-Me-On-The-Winning-Team.png".format(username, jerseynumber, type))
        #img.save(img_url)
        #return request.host_url + img_url

#new code
    # base_64 = draw_text("framed.png", type, username, jerseynumber)
    # return base_64

    #tracks = {"frontend": "Front-End Web Development", "backend": "Back-End Web Development", "python": "Python Programming", "android": "Mobile Development", "ui": "UI/UX Design", "design": "Engineering Design"}
    #track = tracks.get(track, None)
    #    base_64 = draw_text("framed.png", type, first_name, last_name, track)
    #if type == "3":
    #    base_64 = draw_text("average performace.jpg", type, first_name, last_name, track)
    #if type == "4":
    #    base_64 = draw_text("good performance.jpg", type, first_name, last_name, track)
    #if type == "5":
    #    base_64 = draw_text("outstanding.jpg", type, first_name, last_name, track)
    #if type == "1":
    #    base_64 = draw_text("participated.jpg", type, first_name, last_name)
    #if type == "2":
    #    base_64 = draw_text("mentor.jpg", type, first_name, last_name)
    #return base_64


if __name__ == "__main__":
    app.run(debug=True)
