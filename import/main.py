import requests
from dotenv import load_dotenv
from os import getenv, path

load_dotenv()

ACCESS_TOKEN = getenv("ACCESS_TOKEN")
BASE_URL = getenv("BASE_URL")

headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

images_directory = "../images"


def get_image_list():
    res = requests.get(f"{BASE_URL}/images?limit=1000", headers=headers)
    data = res.json()
    return data["items"]


def save_image(image):
    image_id = image["_id"]
    image_url = f"{BASE_URL}/images/{image_id}"
    image_path = path.join(images_directory, image_id)
    res = requests.get(image_url, stream=True)
    res.raise_for_status()
    with open(image_path, "wb") as file:
        for chunk in res.iter_content(chunk_size=8192):
            file.write(chunk)
    print(image_id)


images = get_image_list()
for image in images:
    save_image(image)
