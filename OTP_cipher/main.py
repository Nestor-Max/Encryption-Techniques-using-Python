from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, StringField
from wtforms.validators import InputRequired, Optional
import os
import secrets
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class OTPCipherForm(FlaskForm):
    text = TextAreaField("Text", validators=[InputRequired()])
    key = StringField("Key", validators=[Optional()])
    mode = RadioField("Mode", choices=[('encrypt', 'Encrypt'), ('decrypt', 'Decrypt')], default='encrypt')
    submit = SubmitField("Submit")

def otp_cipher(text, key):
    result = ""
    for i, char in enumerate(text):
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            key_offset = ord(key[i]) - ascii_offset
            result += chr((ord(char) - ascii_offset + key_offset) % 26 + ascii_offset)
        else:
            result += char
    return result

def generate_otp(length):
    return ''.join(secrets.choice(string.ascii_uppercase) for _ in range(length))

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = OTPCipherForm()
    result = None
    key = None
    if form.validate_on_submit():
        text = form.text.data
        mode = form.mode.data
        key = form.key.data if mode == 'decrypt' else generate_otp(len(text))

        result = otp_cipher(text, key)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'otp_output.txt')
        write_file(file_path, result)
    
    return render_template('index.html', form=form, result=result, key=key)

if __name__ == '__main__':
    app.run(debug=True)
