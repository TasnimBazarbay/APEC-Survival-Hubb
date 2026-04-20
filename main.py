from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'apec_premium_secret_key_2026'

@app.route('/')
def index():
    if 'user' not in session: 
        return redirect(url_for('auth'))
    return render_template('home.html', user=session['user'])

@app.route('/auth')
def auth():
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/auth_firebase', methods=['POST'])
def auth_firebase():
    data_req = request.json
    email = data_req.get('email')
    role = data_req.get('role', 'student')
    
    if not email or not email.endswith('@apec.edu.kz'):
        return jsonify({"status": "error", "message": "Доступ разрешен только для домена @apec.edu.kz"}), 403

    # Просто сохраняем проверенного юзера в сессию
    session['user'] = {"email": email, "name": data_req.get('name'), "role": role}
    return jsonify({"status": "success"})

@app.route('/admin')
def admin():
    # Пускаем только если при входе была назначена роль admin
    if session.get('user', {}).get('role') != 'admin': 
        return "Доступ запрещен. Требуются права администратора.", 403
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth'))

if __name__ == '__main__':
    app.run(debug=True)