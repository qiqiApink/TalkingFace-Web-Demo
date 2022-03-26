from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from app import app
import os
import glob
import random
import string
import datetime
from app import app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class makeittalk_Upload(FlaskForm):
    # video = FileField('Choose Video File', validators=[FileAllowed(app.config['ALLOWED_VIDEO_EXTENSIONS'], 'Supported format: mp4, avi'), FileRequired('empty')])
    audio = FileField('Choose Audio File', validators=[FileAllowed(app.config['ALLOWED_AUDIO_EXTENSIONS'], 'Supported format: wav, mp3, flac, ape, aac'), FileRequired('empty')])
    image = FileField('Choose Image File', validators=[FileAllowed(app.config['ALLOWED_IMAGE_EXTENSIONS'], 'Supported format: png, jpg, jpeg, PNG, JPEG'), FileRequired('empty')])
    submit = SubmitField('Generate')

class wav2lip_Upload(FlaskForm):
    video = FileField('Choose Video File', validators=[FileAllowed(app.config['ALLOWED_VIDEO_EXTENSIONS'], 'Supported format: mp4'), FileRequired('empty')])
    audio = FileField('Choose Audio File', validators=[FileAllowed(app.config['ALLOWED_AUDIO_EXTENSIONS'], 'Supported format: wav, mp3, flac, ape, aac'), FileRequired('empty')])
    submit = SubmitField('Generate')

class deepfake_Upload(FlaskForm):
    video = FileField('Choose Video File', validators=[FileAllowed(app.config['ALLOWED_VIDEO_EXTENSIONS'], 'Supported format: mp4'), FileRequired('empty')])
    image = FileField('Choose image File', validators=[FileAllowed(app.config['ALLOWED_IMAGE_EXTENSIONS'], 'Supported format: png, jpg, bmp, eps, svg'), FileRequired('empty')])
    submit = SubmitField('Generate')


def generate_random_subdic(length=13):
    time = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(length)]
    random_subdic = ''.join(str_list) + time
    return random_subdic

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

'''
Wave2lip
'''
@app.route('/wav2lip_upload', methods=['GET', 'POST'])
def wav2lip_upload():
    form = wav2lip_Upload()
    if request.method == 'GET':
        return render_template('wav2lip_upload.html', form=form)
    if form.validate_on_submit():
        uid = generate_random_subdic()
        file_dir = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'])
        video = form.video.data
        vfilename = uid + 'video.' + video.filename.rsplit('.', 1)[-1]
        video.save(os.path.join(file_dir, vfilename))
        audio = form.audio.data
        afilename = uid + 'audio.' + audio.filename.rsplit('.', 1)[-1]
        audio.save(os.path.join(file_dir, afilename))
    else:
        return render_template('wav2lip_upload.html', form=form)
    return redirect(url_for('wav2lip_handle', uid=uid))

@app.route('/wav2lip_report/<uid>', methods=['GET'])
def wav2lip_handle(uid):
    content_path = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'])
    output_dic = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER'])
    if not os.path.exists(output_dic):
        os.makedirs(output_dic)
    vfilename = glob.glob(content_path + '/' + uid + 'video.*')[0]
    afilename = glob.glob(content_path + '/' + uid + 'audio.*')[0]
    outputfile = os.path.join(output_dic, app.config['RESULT_FILENAME'])
    # cmd = "CUDA_VISIBLE_DEVICES=2 python {ROOTDIR}/Wav2Lip/inference.py --checkpoint_path {ROOTDIR}/Wav2Lip/checkpoints/wav2lip_gan.pth --face {vfilename} --audio {afilename} --outfile {outputfile}".format(ROOTDIR=app.config['ROOTDIR'], vfilename=vfilename, afilename=afilename, outputfile=outputfile)
    cmd = "CUDA_VISIBLE_DEVICES=2 python /home/zyq/zhangyaqi_1/TalkingFace/app/Wav2Lip/inference.py --checkpoint_path /home/zyq/zhangyaqi_1/TalkingFace/app/Wav2Lip/checkpoints/wav2lip_gan.pth --face {vfilename} --audio {afilename} --outfile {outputfile}".format(vfilename=vfilename, afilename=afilename, outputfile=outputfile)
    os.system(cmd)
    return render_template('wav2lip_report.html', videofile=vfilename.split('/')[-1], audiofile=afilename.split('/')[-1], outputfile=app.config['RESULT_FILENAME'])

'''
Makeittalk
'''
@app.route('/make_it_talk_report/<uid>', methods=['GET'])
def make_it_talk_handle(uid):
    content_path = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'])
    output_dic = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER'])
    if not os.path.exists(output_dic):
        os.makedirs(output_dic, exist_ok=True)
    ifilename = glob.glob(content_path + '/' + uid + 'image.*')[0]
    afilename = glob.glob(content_path + '/' + uid + 'audio.*')[0]
    outputfile = os.path.join(output_dic, app.config['RESULT_FILENAME'])
    cmd = "python {ROOTDIR}/make_it_talk/main_end2end.py --pic {ifilename} --au {afilename} --outfile {outputfile}".format(ROOTDIR=app.config['ROOTDIR'], ifilename=ifilename, afilename=afilename, outputfile=outputfile)
    os.system(cmd)
    return render_template('make_it_talk_report.html', imagefile=ifilename.split('/')[-1], audiofile=afilename.split('/')[-1], outputfile=app.config['RESULT_FILENAME'])

@app.route('/make_it_talk_upload', methods=['GET', 'POST'])
def make_it_talk_upload():
    form = makeittalk_Upload()
    if request.method == 'GET':
        return render_template('make_it_talk_upload.html', form=form)
    if form.validate_on_submit():
        uid = 'make_it_talk_' + generate_random_subdic()
        file_dir = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'])
        image = form.image.data
        ifilename = uid + 'image.' + image.filename.rsplit('.', 1)[-1]
        image.save(os.path.join(file_dir, ifilename))
        audio = form.audio.data
        afilename = uid + 'audio.' + audio.filename.rsplit('.', 1)[-1]
        audio.save(os.path.join(file_dir, afilename))
    else:
        return render_template('make_it_talk_upload.html', form=form)
    return redirect(url_for('make_it_talk_handle', uid=uid))

'''
deepfake
'''
@app.route('/deepfake_upload', methods=['GET', 'POST'])
def deepfake_upload():
    form = deepfake_Upload()
    if request.method == 'GET':
        return render_template('deepfake_upload.html', form=form)
    if form.validate_on_submit():
        uid = generate_random_subdic()
        file_dir = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'])
        video = form.video.data
        print('video: ', video)
        vfilename = uid + 'video.' + video.filename.rsplit('.', 1)[-1]
        video.save(os.path.join(file_dir, vfilename))
        image = form.image.data
        ifilename = uid + 'image.' + image.filename.rsplit('.', 1)[-1]####################################这里我不确定有没有错
        image.save(os.path.join(file_dir, ifilename))
        
    else:
        return render_template('deepfake_upload.html', form=form)
    return redirect(url_for('deepfake_handle', uid=uid))

@app.route('/deepfake_report/<uid>', methods=['GET'])
def deepfake_handle(uid):
    content_path = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'])
    output_dic = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER'])
    if not os.path.exists(output_dic):
        os.makedirs(output_dic)
    vfilename = glob.glob(content_path + '/' + uid + 'video.*')[0]
    ifilename = glob.glob(content_path + '/' + uid + 'image.*')[0]
    mp3file = "/home/nfymzk/WorkFile/Work1/TalkingFace-Web-Demo-main/app/uploads/temp"+uid+'.mp3'
    outputfile = os.path.join(output_dic, app.config['RESULT_FILENAME'])
    # cmd = "CUDA_VISIBLE_DEVICES=2 python {ROOTDIR}/Wav2Lip/inference.py --checkpoint_path {ROOTDIR}/Wav2Lip/checkpoints/wav2lip_gan.pth --face {vfilename} --audio {afilename} --outfile {outputfile}".format(ROOTDIR=app.config['ROOTDIR'], vfilename=vfilename, afilename=afilename, outputfile=outputfile)
    cmd = "python /home/nfymzk/WorkFile/Work1/Faceswap1/faceswap.py  --video {vfilename} --image {ifilename} --outputfile {outputfile}".format(ROOTDIR=app.config['ROOTDIR'], vfilename=vfilename, ifilename=ifilename, outputfile=outputfile)
    os.system(cmd)
    cmd = "ffmpeg -i {vfilename} -f mp3 -vn {mp3file}".format(vfilename=vfilename, mp3file=mp3file)
    os.system(cmd)
    cmd = "ffmpeg -i {outputfile} -i {mp3file} -c:v copy -c:a {outputfile}".format(outputfile=outputfile, mp3file=mp3file)
    os.system(cmd)
    cmd = "cp -r /home/nfymzk/WorkFile/Work1/TalkingFace-Web-Demo-main/app/uploads/result/resultvideo.mp4 /home/nfymzk/WorkFile/Work1/TalkingFace-Web-Demo-main/app/uploads/"
    os.system(cmd)
    return render_template('deepfake_report.html', videofile=vfilename.split('/')[-1], imagefile=ifilename.split('/')[-1], videofile2='resultvideo.mp4',outputfile=app.config['RESULT_FILENAME'])
#这里穿的参数是什么我不太明白

@app.route('/videodownload/<outputfile>', methods=["GET"])
def videodownload(outputfile):
    result_dic = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER'])
    return send_from_directory(result_dic, outputfile, as_attachment=True)

@app.route('/videoshow/<videofile>', methods=["GET"])
def videoshow(videofile):
    video_path = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'])
    return send_from_directory(video_path, videofile)

@app.route('/imageshow/<imagefile>', methods=["GET"])
def imageshow(imagefile):
    image_path = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'])
    return send_from_directory(image_path, imagefile)

@app.route('/audioshow/<audiofile>', methods=["GET"])
def audioshow(audiofile):
    audio_path = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'])
    return send_from_directory(audio_path, audiofile)

@app.route('/resultshow/<outputfile>', methods=["GET"])
def resultshow(outputfile):
    video_path = os.path.join(app.config['ROOTDIR'], app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER'])
    return send_from_directory(video_path, outputfile)

@app.route('/500')
def test():
    return render_template('500.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
