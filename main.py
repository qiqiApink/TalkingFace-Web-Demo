from app import app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port='33333')
'''
ssh -L 36667:127.0.0.1:33333 -p 9150 nfymzk@202.38.69.85
'''
