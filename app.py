from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
GENERATED_FOLDER = "static/generated"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():

    meme_image = None

    if request.method == "POST":

        # Get uploaded image
        image = request.files["image"]

        # Get texts
        top_text = request.form["top_text"]
        bottom_text = request.form["bottom_text"]

        # Save uploaded image
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(image_path)

        # Open image using Pillow
        img = Image.open(image_path)

        # Create drawing object
        draw = ImageDraw.Draw(img)

        # Font
        font = ImageFont.load_default()

        # Draw top text
        draw.text((20, 20), top_text, fill="white", font=font)

        # Draw bottom text
        draw.text((20, img.height - 40), bottom_text, fill="white", font=font)

        # Save generated meme
        generated_path = os.path.join(
            app.config["GENERATED_FOLDER"],
            "meme_" + image.filename
        )

        img.save(generated_path)

        meme_image = generated_path

    return render_template("index.html", meme_image=meme_image)


if __name__ == "__main__":
    app.run(debug=True)