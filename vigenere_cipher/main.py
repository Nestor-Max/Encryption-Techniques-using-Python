from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, RadioField
from wtforms.validators import InputRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class VigenereCipherForm(FlaskForm):
    text = TextAreaField("Text", validators=[InputRequired()])
    key = StringField("Key", validators=[InputRequired()])
    mode = RadioField("Mode", choices=[('encrypt', 'Encrypt'), ('decrypt', 'Decrypt')], default='encrypt')
    submit = SubmitField("Submit")

def vigenere_cipher(text, key, encrypt=True):
    result = ""
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            key_char = key[i % key_length].upper()
            key_offset = ord(key_char) - 65
            if encrypt:
                result += chr((ord(char) - ascii_offset + key_offset) % 26 + ascii_offset)
            else:
                result += chr((ord(char) - ascii_offset - key_offset) % 26 + ascii_offset)
        else:
            result += char
    return result

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = VigenereCipherForm()
    result = None
    if form.validate_on_submit():
        text = form.text.data
        key = form.key.data
        mode = form.mode.data
        if mode == 'encrypt':
            result = vigenere_cipher(text, key, encrypt=True)
        else:
            result = vigenere_cipher(text, key, encrypt=False)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'vigenere_output.txt')
        write_file(file_path, result)
    return render_template('index.html', form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)