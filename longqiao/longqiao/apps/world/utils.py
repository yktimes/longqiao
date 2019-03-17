import io



from PIL import Image
from django.conf import settings



def upload(img):
    _img = img.read()
    size = len(_img) / (1024 * 1024)  # 上传图片的大小 M单位

    image = Image.open(io.BytesIO(_img))

    name = 'upfile.{0}'.format(image.format)  # 获取图片后缀（图片格式）

    if size > 1:
        # 压缩
        x, y = image.size
        im = image.resize((int(x / 1.73), int(y / 1.73)), Image.ANTIALIAS)  # 等比例压缩 1.73 倍
    else:
        # 不压缩
        im = image

    im.save('./media/' + name)  # 在根目录有个media文件
    path = './media/' + name

