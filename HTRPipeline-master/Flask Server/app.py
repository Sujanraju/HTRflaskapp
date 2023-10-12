from flask import Flask, render_template, request
import cv2
import matplotlib.pyplot as plt
from path import Path
from htr_pipeline import read_page, DetectorConfig
from autocorrect import spell
from spellchecker import SpellChecker



from distutils.log import debug
from fileinput import filename


app = Flask(__name__)

# @app.route('/')
# def index():
#     return ('hello world')

@app.route('/demo')
def result():
    file = ""
    keyword = ""
    if(request.method == "POST"):
        f = request.files['file']
        keyword = request.form.get('keyword')
        f.save(f.filename)
        file = f.filename
        if(not file.__contains__(".png")):
            return render_template("index.html", error = {"error" : True})
        # print(keyword)
    # result = demo(file)
    return render_template("result.html")


@app.route('/')  
def main():  
    return render_template("index.html")  
  
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)  
        print(f)
        file = f.filename

        print(f'Reading file {file}')
        # for img_filename in Path(file):
        #         print(f'Reading file {img_filename}')

        # read text
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        read_lines = read_page(img, DetectorConfig(height=1000))
        text2=' '
        text1=' '

        # output text
        for read_line in read_lines:
            text1 = (' '.join(read_word.text for read_word in read_line))
            print(text1)
            text2 = text2 + text1 + ' '
        #print(text2)

        line = text2
        lines = line.strip().split(' ')
        new_line = ""
        similar_word = {}
        for l in lines:
            new_line += spell(l) + " "
        text3 = new_line

        return render_template("result.html", name = text3)  
  



def demo(file):
    print(f'Reading file {file}')
    # for img_filename in Path(file):
    #         print(f'Reading file {img_filename}')

    # read text
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    read_lines = read_page(img, DetectorConfig(height=1000))
    text2=' '
    text1=' '

    # output text
    for read_line in read_lines:
        text1 = (' '.join(read_word.text for read_word in read_line))
        print(text1)
        text2 = text2 + text1 + ' '
    #print(text2)

    line = text2
    lines = line.strip().split(' ')
    new_line = ""
    similar_word = {}
    for l in lines:
        new_line += spell(l) + " "
    text3 = new_line



    #spell = SpellChecker()
    #text3=(spell.correction(text2))
        

    # plot image with detections and texts as overlay
    # plt.figure(img_filename)
    plt.imshow(img, cmap='gray')
    for i, read_line in enumerate(read_lines):
        for read_word in read_line:
            bbox = read_word.bbox
            xs = [bbox.x, bbox.x, bbox.x + bbox.w, bbox.x + bbox.w, bbox.x]
            ys = [bbox.y, bbox.y + bbox.h, bbox.y + bbox.h, bbox.y, bbox.y]
            plt.plot(xs, ys, c='r' if i % 2 else 'b')
            plt.text(bbox.x, bbox.y, read_word.text)
    plt.show()
    return (text3)