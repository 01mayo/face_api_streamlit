import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw, ImageFont



st.title('顔認識アプリ')

subscription_key = '33d23bf17e6f4df4ab569f9ad229c132'
assert subscription_key
face_api_url = 'https://20220105joe.cognitiveservices.azure.com//face/v1.0/detect'

# 描画するテキストを取得
def get_draw_text(faceDictionary):
    rect = faceDictionary['faceRectangle']
    faceAttr = faceDictionary['faceAttributes']
    age = int(faceAttr['age'])
    gender = faceAttr['gender']
    text = f'gender:{gender} age:{age}'

    # 枠に合わせてフォントサイズを調整
    font_size = max(10, int(rect['width'] / len(text)))
    font = ImageFont.truetype('Arial', font_size)

    return (text, font)


# 認識された顔の上にテキストを描く座標を取得
def get_text_rectangle(faceDictionary, text, font):
    rect = faceDictionary['faceRectangle']
    text_width, text_height = font.getsize(text)
    left = rect['left'] + rect['width'] / 2 - text_width / 2
    top = rect['top'] - text_height - 1

    return (left, top)

# テキストを描画
def draw_text(faceDictionary):
    text, font = get_draw_text(faceDictionary)
    text_rect = get_text_rectangle(faceDictionary, text, font)
    draw.text(text_rect, text, align='center', font=font, fill='red')


uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリ取得
    headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key
        }
    params = {
            'returnFaceId': 'true',
            'returnFaceAttributes': 'age,gender,smile,facialHair,headPose,glasses,emotion,hair,makeup,occlusion'       
        }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

    results = res.json()

    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)

        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill=None,  outline=(0,255,255), width=5)
        draw.text(result)
    st.image(img, caption='Uploaded Image.', use_column_width=True)

