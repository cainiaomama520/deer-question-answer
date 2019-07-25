from flask import Flask, render_template, request, url_for, redirect, session
import config
from exts import db
from models import User


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)




@app.route('/')
def index():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run()
