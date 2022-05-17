from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
import os
app = Flask(__name__)
bootstrap = Bootstrap(app)
nav=Nav()
nav.register_element(
    'top', Navbar(
        '人脸项目',
        View('首页', 'index'),
        Subgroup(
            '人脸动画',
            View('说特定的语音(Wav2Lip)', 'wav2lip_upload'),
            Separator(),
            View('让图像动起来(Make It Talk)', 'make_it_talk_upload')
        ),
        Subgroup(
            '换脸',
            View('换脸(DeepFake)', 'deepfake_upload')
        ),
        Subgroup(
            '你的方法',
            View('你的方法', 'baidu')
        )
    )
)
nav.init_app(app)
UPLOAD_FOLDER = 'uploads'
app.config['SECRET_KEY'] = 'taeyeon'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ROOTDIR'] = os.path.abspath(os.path.dirname(__file__))
app.config['RESULT_FOLDER'] = "result"
app.config['RESULT_FILENAME'] = "resultvideo.mp4"
app.config['RESULT_AUDIO'] = 'result.mp3'
app.config['ALLOWED_VIDEO_EXTENSIONS'] = set(['mp4', 'avi', 'rmvb', 'wmv', 'mov'])
app.config['ALLOWED_AUDIO_EXTENSIONS'] = set(['wav', 'mp3', 'flac', 'ape', 'aac'])
app.config['ALLOWED_IMAGE_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'PNG', 'JPEG', 'bmp', 'eps', 'svg'])
from app import routes
