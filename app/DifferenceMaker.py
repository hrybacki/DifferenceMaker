__author__ = 'jakerose27'

from app import app, ALLOWED_EXTENSIONS
from flask import render_template, request, url_for
from diff_match_patch import diff_match_patch
import werkzeug, copy

lst_dff=[]

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/diff', methods = ['GET', 'POST'])
def diff():
    old_text = request.form['old_text']
    new_text = request.form['new_text']
    d = diff_match_patch()
    s = d.diff_main(old_text, new_text)
    s = d.diff_prettyHtml(s)
    return render_template("diff.html",
                           changes = s)

@app.route('/diff_files', methods = ['GET', 'POST'])
def diff_files():

    file1 = request.files['old_file']
    file2 = request.files['new_file']
    if file1 and file2 and allowed_file(file1.filename) and allowed_file(file2.filename):
        old_text = file1.stream.read()
        new_text = file2.stream.read()
        d = diff_match_patch()
        s = d.diff_main(old_text, new_text)
        s = d.diff_prettyHtml(s)
        return render_template("diff_files.html",
                               old_text = old_text,
                               new_text = new_text,
                               changes = s)
    if not file1 or not file2:
        up_error = "You must upload two files!"
        return render_template("404.html",
                               s = up_error), 404
    ext_error = "One of your files was not found or has an invalid extension type."
    return render_template("404.html",
                           s = ext_error), 404

@app.route('/diff_drag_files', methods=['GET','POST'])
def diff_drag_files():
    if len(lst_dff)==2 and not lst_dff.__contains__('extension'):
        old_text = copy.deepcopy(lst_dff[0])
        new_text = copy.deepcopy(lst_dff[1])
        del lst_dff[:]
        d = diff_match_patch()
        s = d.diff_main(old_text, new_text)
        s = d.diff_prettyHtml(s)
        return render_template("diff_files.html",
                               old_text = old_text,
                               new_text = new_text,
                               changes = s)
    ext_error = "One of your files was not found or has an invalid extension type."
    del lst_dff[:]
    return render_template("404.html",
                           s = ext_error), 404

@app.route('/dealer', methods=['GET', 'POST'])
def dealer():
    if request.files['file'] and allowed_file(request.files['file'].filename):
        s = request.files['file'].stream.read()
        lst_dff.append(s)
    elif not allowed_file(request.files['file'].filename):
        lst_dff.append('extension')
    return ''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

