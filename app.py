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

        image = request.files["image"]

        top_text = request.form["top_text"]
        bottom_text = request.form["bottom_text"]

        # Save uploaded image
        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            image.filename
        )

        image.save(image_path)

        # Open image
        img = Image.open(image_path)

        # Draw object
        draw = ImageDraw.Draw(img)

        # Image width
        width = img.width
        height = img.height

        # Font size
        font_size = int(width / 12)

        # Load font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # TOP TEXT POSITION
        top_position = (50, 30)

        # BOTTOM TEXT POSITION
        bottom_position = (50, height - 100)

        # Draw outline function
        def draw_outline_text(position, text):

            x, y = position

            # Black outline
            for i in range(-2, 3):
                for j in range(-2, 3):
                    draw.text(
                        (x + i, y + j),
                        text,
                        font=font,
                        fill="black"
                    )

            # Main white text
            draw.text(
                position,
                text,
                font=font,
                fill="white"
            )

        # Draw texts
        draw_outline_text(top_position, top_text.upper())
        draw_outline_text(bottom_position, bottom_text.upper())

        # Save meme
        generated_filename = "meme_" + image.filename

        generated_path = os.path.join(
            app.config["GENERATED_FOLDER"],
            generated_filename
        )

        img.save(generated_path)

        meme_image = generated_path

    return render_template(
        "index.html",
        meme_image=meme_image
    )


if __name__ == "__main__":
    app.run(debug=True)