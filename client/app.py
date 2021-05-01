from flask import Flask, render_template, request, Response, jsonify
from parserfile import convert_eng_to_isl, lemmatize_tokens, filter_stop_words, pre_process
from flask_cors import CORS
import json
import cv2
from camera import VideoCamera
#import util

app = Flask(__name__) 
CORS(app)

video_camera = None
global_frame = None

@app.route("/")
def home():
    return render_template("homePage.html")
    
@app.route("/sign-to-speech")
def signToSpeech():
    return render_template("sign.html")
    
@app.route("/speech-to-sign", methods=['GET', 'POST'])
def speechToSign():
    if request.method=='GET':
        return render_template("speech.html")
    
    elif request.method=='POST':
        #def animate_the_speech():
        speechInput = request.form(['output'])
            
        response = jsonify({
            
                            'signing_animation': util.get_animation(speechInput)
                        })
            
        response.headers.add('Access-Control-Allow-Origin', '*')            
        return response

@app.route('/parser', methods=['GET', 'POST'])
def parseit():
    if request.method == "POST":
        input_string = request.form['text']
    else:
        input_string = request.args.get('speech')

    input_string = input_string.lower()
    isl_text_string = ""
    
    asItIs = ['how are you', 'thank you', 'congratulations']    
    if input_string not in asItIs:
        isl_parsed_token_list = convert_eng_to_isl(input_string)
        # ------------ lemmatized_isl_token_list = lemmatize_tokens(isl_parsed_token_list)
        filtered_isl_token_list = filter_stop_words(isl_parsed_token_list)
        lemmatized_isl_token_list = lemmatize_tokens(filtered_isl_token_list)
    
        for token in lemmatized_isl_token_list:
            isl_text_string += token
            isl_text_string += " "
    
    else:
        isl_text_string = input_string.replace(' ', '')
        
    data = {
        'isl_text_string': isl_text_string,
        'pre_process_string': pre_process(isl_text_string)
    }
    return json.dumps(data)
    
@app.route('/sigmlFiles')
def getSigml():
    with open('sigmlFiles.json') as f:
        data = json.load(f)
        
    return json.dumps(data)

@app.route('/hamnosysText', methods=['GET'])
def getText():
    if request.method == 'GET':
        filename = request.args.get('filename').split(',')
        stext = ''''''
        for i in filename:
            x = ''''''
            with open(f'SignFiles/{i}.sigml', 'r') as f:
                x = f.read()
                x = x.replace('\n','').replace('\t','')
                x = x[7:-8]
                stext += x
        
        stext = "<sigml>" + stext + "</sigml>"
        print(stext)
        return stext
		

@app.route('/video_record', methods=['POST'])
def video_record():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')
							
@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
       
if __name__ == "__main__":
    app.run(debug=True)