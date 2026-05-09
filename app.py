from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# Folder paths
UPLOAD_FOLDER = "static/uploads"
GENERATED_FOLDER = "static/generated"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER


# Function to delete old files
def clear_old_files(folder):

    files = os.listdir(folder)

    for file in files:

        file_path = os.path.join(folder, file)

        try:
            os.remove(file_path)

        except:
            pass


@app.route("/", methods=["GET", "POST"])
def home():

    meme_image = None

    if request.method == "POST":

        # Delete old files
        clear_old_files(UPLOAD_FOLDER)
        clear_old_files(GENERATED_FOLDER)

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

        # Create drawing object
        draw = ImageDraw.Draw(img)

        # Image dimensions
        width = img.width
        height = img.height

        # Dynamic font size
        font_size = int(width / 10)
        # Reduce font size for long text
        if len(top_text) > 10 or len(bottom_text) > 10:
            font_size = int(width / 18)

        # Load font
        try:
            font = ImageFont.truetype(
                "arial.ttf",
                font_size
            )

        except:
            font = ImageFont.load_default()

        # Convert text to uppercase
        top_text = top_text.upper()
        bottom_text = bottom_text.upper()

        # Calculate text widths
        top_text_width = draw.textlength(
            top_text,
            font=font
        )

        bottom_text_width = draw.textlength(
            bottom_text,
            font=font
        )

        # Top text position
        top_position = (
            (width - top_text_width) / 2,
            50
        )

        # Bottom text position
        bottom_position = (
            (width - bottom_text_width) / 2,
            height - font_size - 80
        )

        # Function for meme outline text
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

            # White main text
            draw.text(
                position,
                text,
                font=font,
                fill="white"
            )

        # Draw top text
        draw_outline_text(
            top_position,
            top_text
        )

        # Draw bottom text
        draw_outline_text(
            bottom_position,
            bottom_text
        )

        # Generated meme filename
        generated_filename = "meme_" + image.filename

        # Generated path
        generated_path = os.path.join(
            app.config["GENERATED_FOLDER"],
            generated_filename
        )

        # Save final meme
        img.save(generated_path)

        # Send image path to HTML
        meme_image = generated_path

    return render_template(
        "index.html",
        meme_image=meme_image
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    