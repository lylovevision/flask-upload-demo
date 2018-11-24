# 标准库
import os
# 第三方库
from flask import (
    Flask, request, render_template, send_from_directory,
    redirect, url_for, abort
)
from werkzeug.datastructures import FileStorage
# 自己写的其他模块
from helper import random_filename, ensure_folder


ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.upload_folder = os.path.join(ROOT, 'upload')
ensure_folder(app.upload_folder)

@app.route('/')
def view_index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def view_upload():
    myfile = request.files.get('myfile')
    if isinstance(myfile, FileStorage):
        new_name = random_filename(myfile.filename)
        # TODO: 把 new_name 保存到数据库
        save_path = os.path.join(app.upload_folder, new_name)
        myfile.save(save_path)
        return redirect(url_for('view_demo'))
    else:
        abort(400)

@app.route('/image/<path:filename>')
def view_image(filename):
    full_path = os.path.join(app.upload_folder, filename)
    if not os.path.exists(full_path):
        return abort(404)
    return send_from_directory(app.upload_folder, filename)

@app.route('/demo')
def view_demo():
    '''
    # 从数据库中读出来的列表
    file_list = [
        '52508804ef2a522f9295c59865d00c08@1235464.jpg',
        'eb6a60e57f7c5e5985befc0380168c6c@asd12543.jpg'
    ]
    '''
    file_list = os.listdir(app.upload_folder)

    return render_template('demo.html', image_list=file_list)


if __name__ == '__main__':
    app.run(debug=True, port=7777)