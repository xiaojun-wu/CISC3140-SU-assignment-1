from flask import Flask, request, render_template, url_for, redirect
import json
import requests
import datetime

nowtime = datetime.datetime.now()
currentTime = nowtime
date = "&date=" + currentTime.strftime("%Y-%m-%d")
hd = '&True'
title = ''
explanation = ''
imageURL = 'https://apod.nasa.gov/apod/image/1907/moon_eclipse_span1066.jpg'
videoURL = ''
mediaType = ''
url = ''

def updateDate():
    global date
    global currentTime
    date = "&date=" + currentTime.strftime("%Y-%m-%d")

def connectNASA(date):
    global url
    url = 'https://api.nasa.gov/planetary/apod?api_key=ybnJWsrHUoT6QlQLuRpYQ5n0IkwkN7p2m5tvn5Ef'
    global hd
    global title
    global explanation
    global mediaType
    global imageURL
    global mediaType
    global videoURL
    url = url + date
    r = requests.get(url)
    jData = r.json()
    title = jData['title']
    explanation = jData['explanation']
    print(explanation)
    mediaType = jData['media_type']
    if(mediaType == 'image'):
        imageURL = jData['url']
        videoURL = ''
        mediaType = 'image'
    else:
        imageURL = ''
        videoURL = jData['url']
        mediaType = 'video'
        print(videoURL)
    print(jData["title"])
    print('\n')
    print(jData['explanation'])

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world"

@app.route("/previous", methods = ['POST','GET'])
def previous():
    temp = datetime.timedelta(days=1)
    global currentTime
    newTime = currentTime - temp
    currentTime = newTime
    global date
    updateDate()
    return redirect(url_for('APOD'))

@app.route("/next")
def next():
    global currentTime
    global nowtime
    if(nowtime > currentTime):
        temp = datetime.timedelta(days=1)
        currentTime = currentTime + temp
        global date
        updateDate()
        return redirect(url_for('APOD'))
    else:
        return redirect(url_for('APOD'))

@app.route('/nase', methods=['POST'])
def receive_data():
    apiKey = request.form['apiKey']
    print(apiKey)
    global url
    url = apiKey
    return redirect(url_for('APOD'))


@app.route("/nasa")
def APOD():
    global explanation
    global title
    global imageURL
    global videoURL
    connectNASA(date)
    if(mediaType == 'image'):
        return render_template('nasa.html',title=title, explanation = explanation, imageURL = imageURL)
    else:
        return render_template('nasa.html',title=title, explanation = explanation, videoURL = videoURL)


if __name__ == "__main__":
    app.run()
