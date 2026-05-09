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
        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            image.filename
        )

        image.save(image_path)

        # Open image
        img = Image.open(image_path)

        # Create draw object
        draw = ImageDraw.Draw(img)

        # Image dimensions
        width = img.width
        height = img.height

        # Dynamic font size
        font_size = int(width / 12)

        # Load font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Calculate text widths
        top_text_width = draw.textlength(
            top_text.upper(),
            font=font
        )

        bottom_text_width = draw.textlength(
            bottom_text.upper(),
            font=font
        )

        # Center top text
        top_position = (
            (width - top_text_width) / 2,
            30
        )

        # Center bottom text
        bottom_position = (
            (width - bottom_text_width) / 2,
            height - font_size - 40
        )

        # Function for outline text
        def draw_outline_text(position, text):

            x, y = position

            # Black outline
            for i in range(-3, 4):
                for j in range(-3, 4):

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

        # Draw top text
        draw_outline_text(
            top_position,
            top_text.upper()
        )

        # Draw bottom text
        draw_outline_text(
            bottom_position,
            bottom_text.upper()
        )

        # Generated meme filename
        generated_filename = "meme_" + image.filename

        # Save path
        generated_path = os.path.join(
            app.config["GENERATED_FOLDER"],
            generated_filename
        )

        # Save meme image
        img.save(generated_path)

        # Send image path to HTML
        meme_image = generated_path

    return render_template(
        "index.html",
        meme_image=meme_image
    )


if __name__ == "__main__":
    app.run(debug=True)