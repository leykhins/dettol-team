from threading import Timer
import os
from urllib.parse import urljoin
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, url_for, redirect
from flask import render_template, send_file
from werkzeug.utils import secure_filename


app = Flask(__name__)
BASE_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(BASE_PATH, "static")
FONT_PATH = os.path.join(STATIC_PATH, "fonts")
CERTIFICATE_PATH = os.path.join(STATIC_PATH, "certificates")
GENERATED_PATH = os.path.join(STATIC_PATH, "generated")

@app.route("/", methods={'GET', 'POST'})
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username, number = request.form.get('username'), request.form.get('number')
        certificate = make_certificate(username, number)
    return send_file(certificate, as_attachment=True, mimetype='image.png', attachment_filename='gen.png')

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
    #base_64 = urljoin(request.host_url, url_for("static", filename="generated/" + img_title))
    return os.path.join(GENERATED_PATH, img_title)

def download():
    try:
        image = request.files['img_title']
        nom_image = secure_filename(image.filename)
        image = Image.open(image)
        image.save(file_path + nom_image)
        return send_file(file_path, as_attachment=True, attachment_filename='cert.png')
    except Exception as e:
        print(e)
        return redirect(url_for('upload'))

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data['']
        subject = data['subject']
        message = data['message']
        csv_write = csv.writer(database2, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_write.writerow([email,subject,message])

# @app.route('/download/', methods=['POST'])
# def download():
#     try:
#         image = request.files['img_title']
#         nom_image = secure_filename(image.filename)
#         image = Image.open(image)
#         ...
#         image.save('/home/modificateurimage/mysite/static/images/'+nom_image)
#         return send_file('/home/modificateurimage/mysite/static/images/'+nom_image, mimetype='image/jpeg', attachment_filename=nom_image, as_attachment=True), os.remove('/home/modificateurimage/mysite/static/images/'+nom_image)

#     except Exception as e:
#         print(e)
#         return redirect(url_for('upload'))

# handling error 404 - Page not found
@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title='404'), 404

if __name__ == "__main__":
    app.run(debug=True)