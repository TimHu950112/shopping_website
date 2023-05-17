#上傳圖片
import pyimgur,os
from dotenv import load_dotenv
load_dotenv()


CLIENT_ID = os.getenv("client_id")
PATH = "2.png" #A Filepath to an image on your computer"

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.type)