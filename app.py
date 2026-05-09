from flask import Flask, request, Response, redirect
import pyodbc
import hashlib
import urllib.parse

app = Flask(__name__)

# SQL Server connection string
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-6027H4M\SQLEXPRESS;'
    r'DATABASE=ChatDB;'
    r'Trusted_Connection=yes;'
)

# ==================== USER PAGE LOGIC ====================
@app.route('/')
def index():
    try:
        with open("register.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading form: {e}</h3>"


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("EXEC RegisterUser ?, ?, ?", (username, email, password_hash))
        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote(f"User '{username}' registered successfully.")
        return redirect(f"/?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/?msg={error}")

# ==================== MESSAGES PAGE LOGIC ====================
@app.route('/send-message', methods=['GET'])
def show_send_message_page():
    try:
        with open("send_message.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading send message page: {e}</h3>"


@app.route('/send-message', methods=['POST'])
def send_message():
    sender_id = request.form['sender_id']
    receiver_id = request.form['receiver_id']
    message_text = request.form['message_text']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("EXEC SendMessage ?, ?, ?", (sender_id, receiver_id, message_text))
        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("Message sent successfully!")
        return redirect(f"/send-message?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/send-message?msg={error}")

# ==================== FRIENDS PAGE LOGIC  ====================
@app.route('/add_friend', methods=['GET'])
def show_add_friend_page():
    try:
        with open("add_friend.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading add friend page: {e}</h3>"

@app.route('/add_friend', methods=['POST'])
def add_friend():
    user_id = request.form['user_id']
    friend_id = request.form['friend_id']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("EXEC AddFriend ?, ?", (user_id, friend_id))
        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("Friend added successfully!")
        return redirect(f"/add_friend?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/add_friend?msg={error}")

# ==================== FRIEND REQUEST PAGE LOGIC ====================
@app.route('/send_friend_request', methods=['GET'])
def show_send_friend_request_page():
    try:
        with open("send_friend_request.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading send friend request page: {e}</h3>"

@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    sender_id = request.form['sender_id']
    receiver_id = request.form['receiver_id']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("EXEC SendFriendRequest ?, ?", (sender_id, receiver_id))
        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("Friend request sent!")
        return redirect(f"/send_friend_request?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/send_friend_request?msg={error}")

# ====================GROUP PAGE LOGIC ====================
@app.route('/create_group', methods=['GET'])
def show_create_group_page():
    try:
        with open("create_group.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading create group page: {e}</h3>"

@app.route('/create_group', methods=['POST'])
def create_group():
    group_name = request.form['group_name']
    description = request.form['description']
    created_by = request.form['created_by']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("EXEC CreateGroup ?, ?, ?", (group_name, description, created_by))
        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("Group created successfully!")
        return redirect(f"/create_group?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/create_group?msg={error}")

# ==================== GROUP MEMBER PAGE LOGIC ====================
@app.route('/add_group_member', methods=['GET'])
def show_add_group_member_page():
    try:
        with open("add_group_member.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading add group member page: {e}</h3>"

@app.route('/add_group_member', methods=['POST'])
def add_group_member():
    group_id = request.form['group_id']
    user_id = request.form['user_id']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("EXEC AddGroupMember ?, ?", (group_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("Member added to group!")
        return redirect(f"/add_group_member?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/add_group_member?msg={error}")

# ==================== GROUP MESSAGES PAGE LOGIC ====================

@app.route('/send_group_message', methods=['GET'])
def show_group_message_page():
    try:
        with open("group_message.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            else:
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", "")
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading group message page: {e}</h3>"


@app.route('/send_group_message', methods=['POST'])
def send_group_message():
    try:
        group_id = int(request.form['group_id'])
        sender_id = int(request.form['sender_id'])
        message_text = request.form['message_text']

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

       
        cursor.execute("EXEC SendGroupMessage ?, ?, ?", (group_id, sender_id, message_text))

        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("Group message sent successfully!")
        return redirect(f"/send_group_message?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/send_group_message?msg={error}")



# ==================== BLOCK USER PAGE LOGIC ====================
@app.route('/block_user', methods=['GET'])
def show_block_user_page():
    try:
        with open("block_user.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading block user page: {e}</h3>"


@app.route('/block_user', methods=['POST'])
def block_user():
    blocker_id = request.form.get('blocker_id')
    blocked_id = request.form.get('blocked_id')

   
    if not blocker_id or not blocked_id:
        msg = urllib.parse.quote("Both Blocker ID and Blocked ID are required!")
        return redirect(f"/block_user?msg={msg}")

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("EXEC BlockUser ?, ?", (blocker_id, blocked_id))
        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("User blocked successfully!")
        return redirect(f"/block_user?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/block_user?msg={error}")




# ==================== USER SETTINGS PAGE LOGIC ====================
@app.route('/user_settings', methods=['GET'])
def show_user_settings_page():
    try:
        with open("user_settings.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading user settings page: {e}</h3>"


@app.route('/update_setting', methods=['POST'])
def update_user_settings():
    user_id = request.form.get('user_id')
    setting_key = request.form.get('setting_key')
    setting_value = request.form.get('setting_value')

    
    if not user_id or not setting_key or not setting_value:
        msg = urllib.parse.quote("All fields are required!")
        return redirect(f"/user_settings?msg={msg}")

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        
        cursor.execute("EXEC UpdateUserSetting ?, ?, ?", (user_id, setting_key, setting_value))

        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("User setting updated successfully!")
        return redirect(f"/user_settings?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/user_settings?msg={error}")
# ==================== NOTIFICATIONS  PAGE LOGIC ====================
@app.route('/add_notification', methods=['GET'])
def show_add_notification_page():
    try:
        with open("add_notification.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading add notification page: {e}</h3>"
@app.route('/add_notification', methods=['POST'])
def add_notification():
    
    user_id = request.form['user_id']
    notification_text = request.form['notification_text']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
       
        cursor.execute("EXEC AddNotification ?, ?", (user_id, notification_text))
        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("Notification added successfully!")
        return redirect(f"/add_notification?msg={msg}")
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/add_notification?msg={error}")

# ==================== LOGIN LOG PAGE LOGIC ====================



@app.route('/login_log', methods=['GET', 'POST'])
def login_log():
    if request.method == 'GET':
        
        try:
            with open("login_log.html", "r", encoding="utf-8") as f:
                html = f.read()
                msg = request.args.get("msg")
                if msg:
                    alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                    html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
                return Response(html, mimetype='text/html')
        except Exception as e:
            return f"<h3>Error loading login log page: {e}</h3>"

    elif request.method == 'POST':
       
        user_id = request.form['user_id']
        ip_address = request.form['ip_address']

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

           
            cursor.execute("EXEC LogUserLogin ?, ?", (user_id, ip_address))

            conn.commit()
            cursor.close()
            conn.close()

            msg = urllib.parse.quote("Login log saved successfully!")
            return redirect(f"/login_log?msg={msg}")
        except Exception as e:
            error = urllib.parse.quote(f"Error: {str(e)}")
            return redirect(f"/login_log?msg={error}")



# ==================== REPORT LOGIC PAGE LOGIC ====================


@app.route('/report_user', methods=['GET']) 
def show_report_user_page():
    try:
        with open("report_user.html", "r", encoding="utf-8") as f:
            html = f.read()
            msg = request.args.get("msg")
            if msg:
                alert = f"<div class='alert alert-info text-center'>{urllib.parse.unquote(msg)}</div>"
                html = html.replace("<!--MESSAGE_PLACEHOLDER-->", alert)
            return Response(html, mimetype='text/html')
    except Exception as e:
        return f"<h3>Error loading report user page: {e}</h3>"


@app.route('/create_report', methods=['POST'])  
def create_report():
    reporter_id = request.form['reporter_id']
    reported_user_id = request.form['reported_user_id']
    report_text = request.form['report_text']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        
        cursor.execute("EXEC CreateReport ?, ?, ?", (reporter_id, reported_user_id, report_text))

        conn.commit()
        cursor.close()
        conn.close()

        msg = urllib.parse.quote("User report submitted successfully!")
        return redirect(f"/report_user?msg={msg}")  
    except Exception as e:
        error = urllib.parse.quote(f"Error: {str(e)}")
        return redirect(f"/report_user?msg={error}")  


if __name__ == '__main__':
    app.run(debug=True)
