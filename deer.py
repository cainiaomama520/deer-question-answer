from flask import Flask, render_template, request, url_for, redirect, session
import config
from exts import db
from models import User, Question, Answer


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)




@app.route('/')
def index():
    content = {
        "questions": Question.query.order_by('create_time').all()
    }
    return render_template('index.html', **content)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return "没有此用户的信息，请重新注册！"


@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_answer/', methods=['POST'])
def add_answer():
    session_id = session.get('user_id')
    if session_id:
        content = request.form.get('answer_content')
        question_id = request.form.get('question_id')
        answer = Answer(content=content)
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        answer.author = user
        question = Question.query.filter(Question.id == question_id).first()
        answer.question = question
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("detail", question_id=question_id))
    else:
        return redirect(url_for('login'))


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return "该用户已经注册，请换一个手机号码！"
        else:
            if password1 != password2:
                return "两次密码不一致，请重新输入密码！"
            else:
                user = User(username=username, telephone=telephone, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
def question():
    user_id = session.get('user_id')
    if user_id:
        if request.method == 'GET':
            return render_template('question.html')
        else:
            title = request.form.get('title')
            content = request.form.get('content')
            question = Question(title=title, content=content)
            user = User.query.filter(User.id == user_id).first()
            question.author = user
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.context_processor   # 上下文处理器函数必须返回一个字典，这个字典的key可以在所有的模板中使用
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}

    return {}



if __name__ == '__main__':
    app.run()
