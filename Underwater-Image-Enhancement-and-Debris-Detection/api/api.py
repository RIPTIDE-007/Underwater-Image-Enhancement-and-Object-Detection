from flask import Flask , request , url_for , redirect
from Preprocessing import imageEnhancer
from model import objectDetector

app = Flask(__name__)
@app.route('/api/enhancer',methods=['GET', 'POST'])
def getEnhancedImage():
    # imageEnhancer()
    # result=1
    # return {'status': result}

    content_type = request.headers.get('Content-Type')
    json=None
    if (content_type == 'application/json'):
        json = request.get_json()
        print(json)
    print(json['fileName'],type(json['fileName']))
    imageEnhancer(json['fileName'])
    objectDetector()
    result = 1
    return {'status': result}