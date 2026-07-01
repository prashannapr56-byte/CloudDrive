from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Auto-create tables if they don't exist
with app.app_context():
    db.create_all()

# 1. Home Page / Dashboard Route
@app.route('/')
def index():
    files = []
    if session.get('username'):
        # List files for this specific user if S3 is configured
        if app.config.get('AWS_S3_BUCKET') and app.config.get('AWS_ACCESS_KEY_ID') and app.config.get('AWS_ACCESS_KEY_ID') != 'your_access_key_id_here':
            from s3_helper import list_files_in_s3
            try:
                all_files = list_files_in_s3(app.config['AWS_S3_BUCKET'])
                user_prefix = f"{session['username']}/"
                files = [f.replace(user_prefix, '', 1) for f in all_files if f.startswith(user_prefix)]
            except Exception as e:
                print(f"Error listing files: {e}")
    return render_template('index.html', files=files) 

# 2. Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('register'))
            
    return render_template('register.html')

# 3. Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return redirect(url_for('login'))
            
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
            
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        
        flash('Logged in successfully!', 'success')
        return redirect(url_for('index'))
        
    return render_template('login.html')

# 4. Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# 5. S3 File Upload Route
@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('username'):
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))
        
    file = request.files.get('file')
    if not file or file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('index'))
        
    aws_id = app.config.get('AWS_ACCESS_KEY_ID')
    bucket = app.config.get('AWS_S3_BUCKET')
    
    if not aws_id or aws_id == 'your_access_key_id_here' or not bucket or bucket == 'your_s3_bucket_name_here':
        flash('AWS S3 is not configured yet! Please update your .env file with actual credentials.', 'danger')
        return redirect(url_for('index'))
        
    from s3_helper import upload_file_to_s3
    user_prefix = f"{session['username']}/"
    object_name = f"{user_prefix}{file.filename}"
    
    try:
        upload_file_to_s3(file, bucket, object_name)
        flash('File uploaded successfully to AWS S3!', 'success')
    except Exception as e:
        flash(f'Upload failed: {e}', 'danger')
        
    return redirect(url_for('index'))

# 6. S3 File Delete Route
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if not session.get('username'):
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))
        
    bucket = app.config.get('AWS_S3_BUCKET')
    aws_id = app.config.get('AWS_ACCESS_KEY_ID')
    
    if not aws_id or aws_id == 'your_access_key_id_here' or not bucket or bucket == 'your_s3_bucket_name_here':
        flash('AWS S3 is not configured.', 'danger')
        return redirect(url_for('index'))
        
    from s3_helper import delete_file_from_s3
    user_prefix = f"{session['username']}/"
    object_name = f"{user_prefix}{filename}"
    
    try:
        delete_file_from_s3(bucket, object_name)
        flash('File deleted from AWS S3.', 'success')
    except Exception as e:
        flash(f'Delete failed: {e}', 'danger')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)