import pymongo
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, length

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap

conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database('memo')
collection = db.get_collection('memo')

app = Flask(__name__) 

######
app.config['SECRET_KEY'] = 'hard to guess string'
######

bootstrap = Bootstrap(app) 

######
class NameForm(FlaskForm):    
    #name = StringField('What is your schedules', validators=[Required()])
    name = TextAreaField('이벤트를 입력하세요', validators=[Required(),length(max=30)])    #validators=[Required()]
    submit = SubmitField('추가') 
######

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        flash('added a new schedules')
        session['name'] = form.name.data
        form.name.data = ''
        memo = session.get('name')
        collection.insert_one({memo:memo})
        #return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'))

@app.route('/user/<name>') 
def user(name):    
    return render_template('user.html', name=name)

if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0')


