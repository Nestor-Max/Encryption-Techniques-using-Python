from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField, RadioField
from wtforms.validators import InputRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class CaesarCipherForm(FlaskForm):
    text = TextAreaField("Text", validators=[InputRequired()])
    shift = IntegerField("Shift", validators=[InputRequired()])
    mode = RadioField("Mode", choices=[('encrypt', 'Encrypt'), ('decrypt', 'Decrypt')], default='encrypt')
    submit = SubmitField("Submit")

def caesar_cipher(text, shift, encrypt=True):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 97 if char.islower() else 65
            if encrypt:
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = CaesarCipherForm()
    result = None
    if form.validate_on_submit():
        text = form.text.data
        shift = form.shift.data
        mode = form.mode.data
        if mode == 'encrypt':
            result = caesar_cipher(text, shift, encrypt=True)
        else:
            result = caesar_cipher(text, shift, encrypt=False)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.txt')
        write_file(file_path, result)
    return render_template('index.html', form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)