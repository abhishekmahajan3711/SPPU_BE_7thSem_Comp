from PIL import Image, ImageDraw, ImageFont
import string, random 

def random_string():
    N = 5
    s = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # generate a random string of length 5
    random_string = ''.join(random.choices(s, k=N))
    return random_string

getit = lambda : (random.randrange(5, 85),random.randrange(5, 55))
colors = ["black","red","blue","green",(64, 107, 76),(0, 87, 128),(0, 3, 82)]
fill_color = [(64, 107, 76),(0, 87, 128),(0, 3, 82),(191, 0, 255),(72, 189, 0),(189, 107, 0),(189, 41, 0)]

def gen_captcha_img():
   
    img = Image.new('RGB', (90, 60), color="white")
    draw = ImageDraw.Draw(img)   
    captcha_str = random_string()
    text_colors = random.choice(colors)
    draw.text((20,20), captcha_str, fill=text_colors)

    for i in range(5,random.randrange(6, 10)):
        draw.line((getit(), getit()), fill=random.choice(fill_color), width=random.randrange(1,3))

    for i in range(10,random.randrange(11, 20)):
        draw.point((getit(), getit(), getit(), getit(), getit(), getit(), getit(), getit(), getit(), getit()), fill=random.choice(colors))

    img.save(captcha_str +".png")
    return True

gen_captcha_img()

