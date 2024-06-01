from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, Regexp, ValidationError
import os
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class SubstitutionCipherForm(FlaskForm):
    text = TextAreaField("Text", validators=[InputRequired()])
    key = StringField(
        "Key", 
        validators=[
            InputRequired(),
            Length(min=26, max=26, message="Key must be 26 characters long"),
            Regexp(r'^[A-Za-z]+$', message="Key must only contain alphabetic characters")
        ]
    )
    mode = RadioField("Mode", choices=[('encrypt', 'Encrypt'), ('decrypt', 'Decrypt')], default='encrypt')
    submit = SubmitField("Submit")

    def validate_key(self, field):
        if len(set(field.data.upper())) != 26:
            raise ValidationError("Key must contain 26 unique alphabetic characters")

def substitution_cipher(text, key, encrypt=True):
    alphabet = string.ascii_uppercase
    key = key.upper()
    if encrypt:
        table = str.maketrans(alphabet, key)
    else:
        table = str.maketrans(key, alphabet)
    return text.upper().translate(table)

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = SubstitutionCipherForm()
    result = None
    if form.validate_on_submit():
        text = form.text.data
        key = form.key.data
        mode = form.mode.data
        if mode == 'encrypt':
            result = substitution_cipher(text, key, encrypt=True)
        else:
            result = substitution_cipher(text, key, encrypt=False)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'substitution_output.txt')
        write_file(file_path, result)
    return render_template('index.html', form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)
