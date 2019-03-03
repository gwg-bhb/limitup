#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

@version: 0.1
@author:  ALIENWARE
@email:   wangrui0810@gmail.com
@file:    test.py
@time:    2018/11/27 14:23
"""
from flask import Flask, render_template, request, redirect, url_for,session,g
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_wtf import Form # 导入Form
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'I have a dream'

app.config['UPLOADED_IMAGES_DEST'] = os.path.dirname(__file__)+'/uploads'
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
patch_request_class(app)

class UploadForm(Form):
    image = FileField('选择上传的文件',validators=[
        FileAllowed(images, '只能上传图片！'),
        FileRequired('文件未选择！')])
    submit = SubmitField('上传')


@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        print(images)
        print(type(images))
        filename = images.save(form.image.data)
        print(filename)
        print(type(filename))
        file_url = images.url(filename)
        return '上传成功，路径：'+file_url+'<br><img src="'+file_url+'" width="450px">'
    return render_template('upload.html', form=form, title='文件上传')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('limit_up.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)