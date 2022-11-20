import requests
from flask import Flask, render_template, request
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy

#starting an flask application
app=Flask(__name__)
# app.run(debug= True)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.app_context()

#creating an instance of sqlalchemy

db=SQLAlchemy(app)

class City(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)


cities=City.query.all()  
@app.route('/', methods=['GET','POST'])
def index():
    
    if request.method=='POST':
        new_city=request.form.get('city')
        if new_city:
            n_c=City(name=new_city)
            db.session.add(n_c)
            db.session.commit()
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c8ed8ac36eb1c1a2b1b134cdd2678faf'
    #city="Las vegas"
    weather=[]
    for city in cities:
        response = requests.get(url.format(city.name)).json()
        #pprint(response)
        w={
            "city":city.name,
            "temperature":response['main']['temp'],
            "desc":response['weather'][0]['description'],
            "icon":response['weather'][0]['icon']
        }
        weather.append(w)
    return render_template('weather.html',weather=weather)


