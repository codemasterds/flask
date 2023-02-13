import requests
from flask import Flask, redirect, render_template, request, url_for
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from flask import *

#starting an flask application
app=Flask(__name__)
app.run(debug= True)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context()

#creating an instance of sqlalchemy

db=SQLAlchemy(app)

class City(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)

def get_weather_data(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c8ed8ac36eb1c1a2b1b134cdd2678faf'
    response = requests.get(url.format(city)).json()
    return response
    

@app.route('/')
def index_get():
    cities=City.query.all() 
    weather=[]
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c8ed8ac36eb1c1a2b1b134cdd2678faf'

    for city in cities:
        print(city)
        response= get_weather_data(city.name)
        pprint(response)  
        w={
            "city":city.name,
            "temperature":response['main']['temp'],
            "desc":response['weather'][0]['description'],
            "icon":response['weather'][0]['icon']
        }
        weather.append(w)
    return render_template('weather.html',weather=weather)



@app.route('/', methods=['POST'])
def index_post():
        cities=City.query.all() 
    
        new_city=request.form.get('city')
        if new_city:
            res=get_weather_data(new_city)
            if res['cod']==200:
                existing_city=City.query.filter_by(name=new_city).first()
                if not existing_city:
                
                        n_c=City(name=new_city)
                        db.session.add(n_c)
                        db.session.commit()    
                else:
                        err_msg="City already exists"
            else:
                err_msg="city doesn't exist in the world"
            
            
            
            
                
           
          
    
   
        return redirect(url_for('index_get'))

