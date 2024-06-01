from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, StringField
from wtforms.validators import InputRequired
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class RSACipherForm(FlaskForm):
    text = TextAreaField("Text", validators=[InputRequired()])
    mode = RadioField("Mode", choices=[('encrypt', 'Encrypt'), ('decrypt', 'Decrypt')], default='encrypt')
    private_key = StringField("Private Key")
    submit = SubmitField("Submit")

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def rsa_encrypt(text, public_key):
    rsa_public_key = RSA.import_key(public_key)
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    encrypted_text = rsa_public_key.encrypt(text.encode())
    return encrypted_text

def rsa_decrypt(encrypted_text, private_key):
    rsa_private_key = RSA.import_key(private_key)
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
    decrypted_text = rsa_private_key.decrypt(encrypted_text).decode()
    return decrypted_text

def write_file(file_path, content):
    with open(file_path, 'wb') as file:
        file.write(content)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = RSACipherForm()
    result = None
    public_key = None
    if form.validate_on_submit():
        text = form.text.data
        mode = form.mode.data
        if mode == 'encrypt':
            private_key, public_key = generate_rsa_keys()
            result = rsa_encrypt(text, public_key)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'rsa_encrypted.txt')
        else:
            private_key = form.private_key.data
            result = rsa_decrypt(text.encode(), private_key)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'rsa_decrypted.txt')
        write_file(file_path, result)
    return render_template('index.html', form=form, result=result, public_key=public_key)

if __name__ == '__main__':
    app.run(debug=True)
