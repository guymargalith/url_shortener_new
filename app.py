from operator import ne
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug import exceptions
from hashids import Hashids

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.sqlite3'
db = SQLAlchemy(app)
hashids = Hashids(min_length=5)

class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    code = db.Column(db.String(1000))

    def __repr__(self):
        return f"id: {self.id}, URL: {self.url}, code: {self.code}"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url_input = request.form['url_input']
        url_find = Urls.query.filter_by(url = url_input).first()
        if url_find:
            result= url_find.code
            print(url_find)
        else:
            new_url = Urls(url = url_input)
            db.session.add(new_url)
            db.session.commit()
            new_url.code = hashids.encode(new_url.id)
            db.session.commit()
            result = new_url.code
        return render_template('base.html', result=f'{request.root_url}{result}')
    else:
        return render_template('base.html')

@app.route('/<string:code>', methods = ['GET'])
def route(code):
    url_find = Urls.query.filter_by(code = code).first()
    if url_find:
        return redirect(url_find.url)
    else:
        raise exceptions.NotFound()
            
            
@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return render_template('404.html'), 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return render_template('500.html'), 500

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)