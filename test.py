from flask import Flask, request, render_template, url_for, redirect
import json
import requests
import datetime

currentTime = datetime.datetime.now()
date = "&date=" + currentTime.strftime("%Y-%m-%d")
hd = '&True'
title = ''
explanation = ''
imageURL = 'https://apod.nasa.gov/apod/image/1907/moon_eclipse_span1066.jpg'
videoURL = ''
mediaType = ''
url = ''

def getToday():
    nowtime = datetime.datetime.now()
    return nowtime

def dateFormetChange(date):
    date = "&date=" + date.strftime("%Y-%m-%d")
    return date

def updateDate():
    #global date
    global currentTime
    date = dateFormetChange(currentTime)
    print("this is date: "+ date)
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
    print("this is apikey in connectNASA: "+apikey)
    print('this is date in connectNASA: '+ date)
    if(apikey == ''):
        url = 'https://api.nasa.gov/planetary/apod?api_key=ybnJWsrHUoT6QlQLuRpYQ5n0IkwkN7p2m5tvn5Ef'
        url = url + date
    else:
        url = apikey
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
    currentTime = currentTime - temp
    date = updateDate()
    print("this is date: "+ date)
    return redirect(url_for('APOD',date = date, apikey = ''))

@app.route("/next")
def next():
    global currentTime
    today = getToday()
    if(today > currentTime):
        temp = datetime.timedelta(days=1)
        currentTime = currentTime + temp
        date = updateDate()
        return redirect(url_for('APOD',date = date, apikey = ''))
    else:
        return redirect(url_for('APOD'))

@app.route('/apikey', methods=['POST'])
def receive_data():
    apikey = request.form['apikey']
    print("this is apikey: "+apikey)
    #return redirect(url_for('APOD',apikey = apikey))
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
    # if request.method == 'POST':
    #     apikey = request.form['apiKey']
    print("this is date in apod: "+ date)
    print("this is apikey: "+ apikey)
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
