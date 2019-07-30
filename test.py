from flask import Flask, request, render_template, url_for, redirect
import requests
import datetime

currentTime = datetime.datetime.now().date()
date = "&date=" + currentTime.strftime("%Y-%m-%d")
hd = '&True'
title = ''
explanation = ''
imageURL = ''
videoURL = ''
mediaType = ''
url = ''

def getToday():
    nowtime = datetime.datetime.now().date()
    return nowtime

def dateFormetChange(date):
    date = "&date=" + date.strftime("%Y-%m-%d")
    return date

def updateDate():
    global currentTime
    date = dateFormetChange(currentTime)
    return date

def connectNASA(date,apikey):
    global hd
    global title
    global explanation
    global mediaType
    global imageURL
    global mediaType
    global videoURL
    url = ''
    if(apikey == ''):
        url = 'https://api.nasa.gov/planetary/apod?api_key=ybnJWsrHUoT6QlQLuRpYQ5n0IkwkN7p2m5tvn5Ef'
        url = url + date
    else:
        url = apikey
    r = requests.get(url)
    jData = r.json()
    title = jData['title']
    explanation = jData['explanation']
    mediaType = jData['media_type']
    if(mediaType == 'image'):
        imageURL = jData['url']
        videoURL = ''
        mediaType = 'image'
    else:
        imageURL = ''
        videoURL = jData['url']
        mediaType = 'video'

app = Flask(__name__)

@app.route("/")
def hello():
    return """Hello, welcome to the NASA APOD alternative website!
                This website can show the APOD by enter the url 'http://127.0.0.1:5000/nasa.
                You can use this website browse yesterday's APOD or next's day APOD(if it exist).
                You also can enter your own api key to browse any date of APOD you want.
                """

@app.route("/previous", methods = ['POST','GET'])
def previous():
    temp = datetime.timedelta(days=1)
    global currentTime
    currentTime = currentTime - temp
    date = updateDate()
    return redirect(url_for('APOD',date = date, apikey = ''))

@app.route("/next")
def next():
    global currentTime
    today = getToday()
    date = ''
    if(today > currentTime):
        temp = datetime.timedelta(days=1)
        currentTime = currentTime + temp
        date = updateDate()
    else:
        date = dateFormetChange(today)
    return redirect(url_for('APOD',date = date, apikey = ''))

@app.route('/apikey', methods=['POST'])
def receive_data():
    apikey = request.form['apikey']
    global explanation
    global title
    global imageURL
    global videoURL
    connectNASA("",apikey)
    if(mediaType == 'image'):
        return render_template('nasa.html',title=title, explanation = explanation, imageURL = imageURL)
    else:
        return render_template('nasa.html',title=title, explanation = explanation, videoURL = videoURL)

@app.route("/nasa", defaults = {'date':'','apikey':''})
@app.route("/nasa/<date>")
def APOD(date = '',apikey = ''):
    global explanation
    global title
    global imageURL
    global videoURL
    apikey = ''
    if not (apikey == ''):
        connectNASA('date',apikey)
    elif not (date == ''):
        connectNASA(date,apikey)
    else:
        date = getToday()
        date = dateFormetChange(date)
        connectNASA(date,apikey)
    if(mediaType == 'image'):
        return render_template('nasa.html',title=title, explanation = explanation, imageURL = imageURL)
    else:
        return render_template('nasa.html',title=title, explanation = explanation, videoURL = videoURL)


if __name__ == "__main__":
    app.run()
