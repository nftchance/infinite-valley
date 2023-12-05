import base64
import numpy as np

from io import BytesIO
from PIL import Image


image_prompts = (
    "seeing infinity",
    "surrounded by music",
    "feeling loved",
    "evolving to take on a new meaning",
    "breaking into a new dimension",
    "splitting into a lot of pieces",
)


def get_prompt(hour):
    # 0 - 10
    randomness = np.random.randint(0, 10)

    timeOfDay = "birth"
    if hour < 6:
        timeOfDay = "dark night, moonlight, stars"
    elif hour < 12:
        timeOfDay = "sunrise"
    elif hour < 18:
        timeOfDay = (
            f"day,{'sunlight' if hour % 3 == 0 else ''}"
            f",{'clouds' if hour % 3 == 0 else ''}"
            f",{'birds, birds flying' if randomness > 5 else ''}"
            f",{'butterflies' if randomness > 6 else ''}"
        )
    elif hour < 24:
        timeOfDay = "evening, sunset, twilight"

    prompt = (
        f"realistic painting,high detail,high resolution,"
        f"{timeOfDay} scene, hour {hour},"
        f"fantasy landscape, fictional world,"
        f"valley, medieval village in a valley,"
        f"winding dirt paths with rock walls, zooming in"
    )

    print("Generating the next snapshot of the day with:", prompt)

    return prompt


def get_pixelated_image(pil_image, pixelation=6):
    pixel_image = pil_image.resize(
        (pil_image.width // pixelation, pil_image.height // pixelation),
        Image.NEAREST,
    )
    pixel_image = pixel_image.resize(
        (pixel_image.width * pixelation, pixel_image.height * pixelation),
        Image.NEAREST
    )

    return pixel_image


def get_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    return img_str.decode("utf-8")


def get_image(text_pipe, image_pipe, day, last_image=None):
    intervals = 4
    hour = day % (24 * intervals)
    prompt = get_prompt(hour)

    new_image = None
    if last_image is None:
        new_image = text_pipe(
            prompt=prompt,
            num_inference_steps=1,
            guidance_scale=0.0
        ).images[0].resize((960, 540), Image.LANCZOS)
    else:
        if last_image is None:
            raise Exception("last_image is None")

        new_image = image_pipe(
            prompt=prompt,
            image=last_image,
            num_inference_steps=2,
            strength=0.8,
            guidance_scale=0.0,
        ).images[0]

    pixel_image = get_pixelated_image(new_image)
    pixel_image = pixel_image.resize((
        pixel_image.width * 2,
        pixel_image.height * 2
    ), Image.LANCZOS)
    pixel_image_base64 = get_base64(pixel_image)

    return prompt, pixel_image_base64
