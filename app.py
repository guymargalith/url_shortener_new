from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug import exceptions

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.sqlite3'
db = SQLAlchemy(app)

class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"id: {self.id}, URL: {self.url}"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url_input = request.form['url_input']
        url_find = Urls.query.filter_by(url = url_input).first()
        if url_find:
            result= url_find.id
        else:
            new_url = Urls(url = url_input)
            db.session.add(new_url)
            db.session.commit()
            result = new_url.id
        return render_template('base.html', result=result)
    else:
        return render_template('base.html')

@app.route('/<int:id>', methods = ['GET'])
def route(id):
    url_find = Urls.query.filter_by(id = id).first()
    if url_find:
        return redirect(url_find.url)
    else:
        raise exceptions.NotFound()
            
            
@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    app.run(debug=True)