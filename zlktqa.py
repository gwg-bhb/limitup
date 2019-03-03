#encoding: utf-8

from flask import Flask,render_template,request,redirect,url_for,session,g
import config
from exts import db
from models import DailyResult
from decorator import login_required
from tools import get_elements
import os

from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads, patch_request_class


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 文件上传
photos = UploadSet('photos', IMAGES)
# 设置上传文件的地址
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()
# 上传的初始化
configure_uploads(app, photos)
# 配置上传文件大小，默认64M，设置None则会采用MAX_CONTENT_LENGTH配置选项
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
patch_request_class(app, size=None)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        print(user)
        if user and user.check_password(password):
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后再登录！'


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
        print(user)
        if user:
            return '该手机号码已被注册，请更换手机号码！'
        else:
            # password1要和password2相等才可以
            if password1 != password2:
                return '两次密码不相等，请核对后再填写！'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登录的页面
                return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    #先把user_id删掉
    del session['user_id']
    return redirect(url_for('login'))


@app.context_processor
def my_context_processer():
    #在执行试图函数之前 都会先执行钩子函数
    user_id = session.get('user_id')
    print('执行了钩子函数')
    print(user_id)
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            print(user)
            return {'user': user}
    else:
        return {}


#登录限制的装饰器
def login_required(func):
    @wraps(func)
    def wrappers(*args, **kwargs):
        pass

    return wrappers


@app.route('/')
def index():
    element_list = get_elements()
    img_url = None
    if request.method == 'POST' and 'photo' in request.files:
        # 生成随机的文件名
        suffix = os.path.splitext(request.files['photo'].filename)[1]
        filename = 'aaa' + suffix
        # 保存上传文件
        photos.save(request.files['photo'], name=filename)
        # 获取上传图片的URL
        img_url = photos.url(filename)
    return render_template('limit_up.html', element_list=element_list, img_url=img_url)

# before_request -> 视图函数 -> context_processor
if __name__ == '__main__':
    app.run(port=5000)
