from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)

@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('posts_detail.html', article=article)

@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/pasts')
    except:
        return "При удалении статьи произошда ошибка"

@app.route('/posts/<int:id>/update', methods = ['POST', 'GET'])
def create_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.author = request.form['author']
        article.intro = request.form['intro']
        article.text = request.form['text']
        article.comment = request.form['comment']


        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавление статьи произошла ошибка"
    else:
        article =Article.query.get(id)
        return render_template('post_update.html', article= article)



# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
#     return 'User page:' + name + "-" + str(id)

@app.route('/create_article', methods = ['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        intro = request.form['intro']
        text = request.form['text']
        comment = request.form['comment']

        article = Article(title=title, author=author, intro=intro, text=text, comment=comment)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавление произошла ошибка"
    else:
        return render_template('create_article.html')


if __name__ == '__main__':
    app.run(debug=True)