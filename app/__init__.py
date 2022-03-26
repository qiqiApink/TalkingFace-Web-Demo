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
        'FaceProject',
        View('Home', 'index'),
        Subgroup(
            'TalkingFace',
            View('Wav2Lip', 'wav2lip_upload'),
            Separator(),
            View('Test', 'test')
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
app.config['ALLOWED_VIDEO_EXTENSIONS'] = set(['mp4'])
app.config['ALLOWED_AUDIO_EXTENSIONS'] = set(['wav', 'mp3', 'flac', 'ape', 'aac'])
from app import routes
