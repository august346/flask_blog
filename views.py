from operator import attrgetter

import datetime

from myapp import app
from models import Member, db, Article, Tag
from forms import LoginForm, PostForm
from flask import render_template, request, url_for, redirect, session


@app.route('/')
def index():
    articles = Article.query
    articles = sorted(articles, key=attrgetter('pub_date'), reverse=True    )
    tags = Tag.query.filter(Tag.articles>0)
    tags = sorted(tags, key=attrgetter('articles'), reverse=True)

    return render_template('index.html', articles=articles, tags=tags)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<int:post_num>')
def get_post(post_num):
    art = Article.query.filter_by(id=post_num).first()
    art.pub_date = art.pub_date.strftime('%Y.%m.%d')

    return render_template('post.html', art=art)


@app.route('/tag/<tagname>')
def by_tag(tagname):
    posts = Article.query
    tags = Tag.query.filter_by(name=tagname)
    result = []
    for post in posts:
        if tagname in post.tags:
            result.append(post)

    return render_template('index.html', articles=result, tags=tags)


@app.route('/admin')
def admin():
    if is_admin():
        articles = Article.query
        articles = sorted(articles, key=attrgetter('pub_date'), reverse=True)
        return render_template('admin/admin.html', posts=articles)
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)

    name = request.form['username']
    password = request.form['password']
    admin = Member.query.filter_by(name=name, password=password).first()
    if admin:
        session['name'] = 'admin'
    return redirect(url_for('index'))


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if not is_admin():
        return redirect(url_for('admin'))
    if request.method == 'GET':
        form = PostForm()
        return render_template('new_post.html', form=form)
    title = request.form['title']
    text = request.form['text']
    description = request.form['description']
    picture = request.form['picture']
    tags = request.form['tags']

    article = Article(
        title=title,
        text=text,
        description=description,
        picture=picture,
        tags=tags)

    db.session.add(article)
    db.session.commit()

    for tag in set(tags.split(' ')):
        tag_in_base = Tag.query.filter_by(name=tag).first()
        if tag_in_base:
            tag_in_base.articles += 1
        else:
            tag_in_base = Tag(name=tag)
        db.session.add(tag_in_base)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('name')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not is_admin():
        return redirect(url_for('admin'))
    post = Article.query.filter_by(id=id).first()
    if request.method == 'POST':
        for tag in post.tags.split(' '):
            if tag == '':
                continue
            print(tag)
            minustag = Tag.query.filter_by(name=tag).first()
            minustag.articles -= 1
            if minustag.articles == 0:
                db.session.delete(minustag)
            db.session.commit()
        post.title = request.form['title']
        post.text = request.form['text']
        post.description = request.form['description']
        post.picture = request.form['picture']
        post.tags = request.form['tags']
        post.pub_date = datetime.datetime.utcnow()

        db.session.commit()
        for tag in post.tags.split(' '):
            if tag == '':
                continue
            tag_in_base = Tag.query.filter_by(name=tag).first()
            if tag_in_base:
                tag_in_base.articles += 1
            else:
                tag_in_base = Tag(name=tag)
            db.session.add(tag_in_base)
            db.session.commit()
        return redirect(url_for('index'))

    form = PostForm()
    form.description.data = post.description
    form.text.data = post.text
    form.title.data = post.title
    form.tags.data = post.tags
    form.picture.data = post.picture
    return render_template('new_post.html', post=post, form=form)


@app.route('/delete/<int:id>')
def delete(id):
    if not is_admin():
        return redirect(url_for('admin'))
    post = Article.query.filter_by(id=id).first()
    try:
        for tag in post.tags.split(' '):
            if tag == '':
                continue
            print(tag)
            minustag = Tag.query.filter_by(name=tag).first()
            minustag.articles -= 1
            if minustag.articles == 0:
                db.session.delete(minustag)
            db.session.commit()
    except:
        pass
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


def is_admin():
    if session.get('name'):
        return True
    return False

