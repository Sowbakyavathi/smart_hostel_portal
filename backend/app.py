from flask import Flask, send_from_directory, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)

db = SQLAlchemy(app)

# ==================== MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    student_id = db.Column(db.String(20), unique=True)
    hostel_name = db.Column(db.String(50))
    room_number = db.Column(db.String(10))
    branch = db.Column(db.String(100))
    phone = db.Column(db.String(15))

class Complaint(db.Model):
    __tablename__ = 'complaints'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='other')
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notice(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VisitorLog(db.Model):
    __tablename__ = 'visitor_logs'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    visitor_name = db.Column(db.String(100))
    purpose = db.Column(db.String(200))
    check_in = db.Column(db.DateTime, default=datetime.utcnow)

class MessFeedback(db.Model):
    __tablename__ = 'mess_feedback'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    meal_type = db.Column(db.String(20))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True)
    hostel_name = db.Column(db.String(50))
    floor = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    status = db.Column(db.String(20), default='available')

# ==================== PAGE ROUTES ====================

@app.route('/')
def login_page():
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/register')
def register_page():
    return send_from_directory(app.static_folder, 'register.html')

@app.route('/dashboard')
def dashboard_page():
    if 'user_id' not in session:
        return send_from_directory(app.static_folder, 'login.html')
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/menu')
def menu_page():
    if 'user_id' not in session:
        return send_from_directory(app.static_folder, 'login.html')
    return send_from_directory(app.static_folder, 'menu.html')

@app.route('/complaints')
def complaints_page():
    if 'user_id' not in session:
        return send_from_directory(app.static_folder, 'login.html')
    return send_from_directory(app.static_folder, 'complaints.html')

@app.route('/leave')
def leave_page():
    if 'user_id' not in session:
        return send_from_directory(app.static_folder, 'login.html')
    return send_from_directory(app.static_folder, 'leave.html')

@app.route('/visitor')
def visitor_page():
    if 'user_id' not in session:
        return send_from_directory(app.static_folder, 'login.html')
    return send_from_directory(app.static_folder, 'visitor.html')

@app.route('/feedback')
def feedback_page():
    if 'user_id' not in session:
        return send_from_directory(app.static_folder, 'login.html')
    return send_from_directory(app.static_folder, 'feedback.html')

@app.route('/facilities')
def facilities_page():
    if 'user_id' not in session:
        return send_from_directory(app.static_folder, 'login.html')
    return send_from_directory(app.static_folder, 'facilities.html')

@app.route('/profile')
def profile_page():
    if 'user_id' not in session:
        return send_from_directory(app.static_folder, 'login.html')
    return send_from_directory(app.static_folder, 'profile.html')

@app.route('/admin')
def admin_page():
    if 'user_id' not in session:
        return send_from_directory(app.static_folder, 'login.html')
    user = db.session.get(User, session['user_id'])
    if not user or user.role != 'admin':
        return send_from_directory(app.static_folder, 'dashboard.html')
    return send_from_directory(app.static_folder, 'admin.html')

# ==================== API ROUTES ====================

@app.route('/api/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(name=name).first()
    if user and user.password == password:
        session.clear()
        session['user_id'] = user.id
        session['name'] = user.name
        session['role'] = user.role
        return jsonify({'success': True, 'role': user.role})
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401


def require_admin():
    """Return an API error response unless the active session belongs to an admin."""
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'error': 'Not logged in'}), 401
    user = db.session.get(User, user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    return None


@app.route('/api/register', methods=['POST'])
def register():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        student_id = request.form.get('student_id')
        hostel_name = request.form.get('hostel_name')
        branch = request.form.get('branch')
        phone = request.form.get('phone')
        
        if User.query.filter_by(name=name).first():
            return jsonify({'success': False, 'error': 'Name already exists'})
        
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        student = Student(
            user_id=user.id,
            student_id=student_id,
            hostel_name=hostel_name,
            branch=branch,
            phone=phone,
            room_number='Not Assigned'
        )
        db.session.add(student)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful!'})
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# ===== COMPLAINTS =====

@app.route('/api/complaints', methods=['POST'])
def add_complaint():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        category = data.get('category', 'other')
        priority = data.get('priority', 'medium')
        
        complaint = Complaint(
            student_id=student.id,
            title=title,
            description=description,
            category=category,
            priority=priority
        )
        db.session.add(complaint)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Complaint submitted!'})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/complaints', methods=['GET'])
def get_complaints():
    try:
        if 'user_id' not in session:
            return jsonify([])
        
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if not student:
            return jsonify([])
        
        complaints = Complaint.query.filter_by(student_id=student.id).all()
        return jsonify([{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'category': c.category,
            'priority': c.priority,
            'status': c.status,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        } for c in complaints])
    except Exception as e:
        print("Error:", e)
        return jsonify([])

# ===== NOTICES =====

@app.route('/api/notices', methods=['GET'])
def get_notices():
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'content': n.content,
        'created_by': n.created_by or 'Admin',
        'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')
    } for n in notices])

# ===== LEAVE =====

@app.route('/api/leave', methods=['POST'])
def add_leave():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        reason = data.get('reason')
        
        leave = LeaveRequest(
            student_id=student.id,
            from_date=datetime.strptime(from_date, '%Y-%m-%d').date(),
            to_date=datetime.strptime(to_date, '%Y-%m-%d').date(),
            reason=reason
        )
        db.session.add(leave)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Leave submitted!'})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/leave', methods=['GET'])
def get_leave():
    try:
        if 'user_id' not in session:
            return jsonify([])
        
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if not student:
            return jsonify([])
        
        leaves = LeaveRequest.query.filter_by(student_id=student.id).all()
        return jsonify([{
            'id': l.id,
            'from_date': l.from_date.strftime('%Y-%m-%d'),
            'to_date': l.to_date.strftime('%Y-%m-%d'),
            'reason': l.reason,
            'status': l.status
        } for l in leaves])
    except Exception as e:
        print("Error:", e)
        return jsonify([])

# ===== VISITOR =====

@app.route('/api/visitor', methods=['POST'])
def add_visitor():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        visitor_name = data.get('visitor_name')
        purpose = data.get('purpose')
        
        visitor = VisitorLog(
            student_id=student.id,
            visitor_name=visitor_name,
            purpose=purpose
        )
        db.session.add(visitor)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Visitor logged!'})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/visitor', methods=['GET'])
def get_visitors():
    try:
        if 'user_id' not in session:
            return jsonify([])
        
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if not student:
            return jsonify([])
        
        visitors = VisitorLog.query.filter_by(student_id=student.id).all()
        return jsonify([{
            'id': v.id,
            'visitor_name': v.visitor_name,
            'purpose': v.purpose,
            'check_in': v.check_in.strftime('%Y-%m-%d %H:%M')
        } for v in visitors])
    except Exception as e:
        print("Error:", e)
        return jsonify([])

# ===== MESS FEEDBACK =====

@app.route('/api/mess/feedback', methods=['POST'])
def add_feedback():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        meal_type = data.get('meal_type')
        rating = data.get('rating')
        comment = data.get('comment')
        
        feedback = MessFeedback(
            student_id=student.id,
            meal_type=meal_type,
            rating=rating,
            comment=comment
        )
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Feedback submitted!'})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/mess/feedback', methods=['GET'])
def get_feedback():
    try:
        if 'user_id' not in session:
            return jsonify([])
        
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if not student:
            return jsonify([])
        
        feedbacks = MessFeedback.query.filter_by(student_id=student.id).all()
        return jsonify([{
            'id': f.id,
            'meal_type': f.meal_type,
            'rating': f.rating,
            'comment': f.comment,
            'created_at': f.created_at.strftime('%Y-%m-%d %H:%M')
        } for f in feedbacks])
    except Exception as e:
        print("Error:", e)
        return jsonify([])

# ===== PROFILE =====

@app.route('/api/profile', methods=['GET'])
def get_profile():
    if 'user_id' not in session:
        return jsonify({})
    
    user = User.query.get(session['user_id'])
    student = Student.query.filter_by(user_id=session['user_id']).first()
    
    return jsonify({
        'name': user.name,
        'email': user.email,
        'student_id': student.student_id if student else '',
        'hostel_name': student.hostel_name if student else '',
        'room_number': student.room_number if student else '',
        'branch': student.branch if student else '',
        'phone': student.phone if student else ''
    })

@app.route('/api/profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    if student:
        student.phone = request.form.get('phone', student.phone)
        student.room_number = request.form.get('room_number', student.room_number)
        db.session.commit()
    return jsonify({'success': True, 'message': 'Profile updated!'})

# ===== ROOMS =====

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{
        'id': r.id,
        'room_number': r.room_number,
        'hostel_name': r.hostel_name,
        'floor': r.floor,
        'capacity': r.capacity,
        'status': r.status
    } for r in rooms])

# ===== MENU =====

@app.route('/api/menu', methods=['GET'])
def get_menu():
    day = datetime.now().strftime('%A')
    menu = {
        'Monday': {
            'breakfast': 'Poha, Idli, Chutney',
            'lunch': 'Rice, Dal, Roti, Veg Curry, Salad',
            'dinner': 'Roti, Veg Curry, Salad'
        },
        'Tuesday': {
            'breakfast': 'Dosa, Chutney, Sambar',
            'lunch': 'Biryani, Raita, Salad',
            'dinner': 'Chapati, Paneer, Veg'
        },
        'Wednesday': {
            'breakfast': 'Upma, Tea, Biscuits',
            'lunch': 'Rice, Sambar, Veg Fry',
            'dinner': 'Roti, Mixed Veg, Dal'
        },
        'Thursday': {
            'breakfast': 'Pongal, Chutney, Vada',
            'lunch': 'Fried Rice, Manchurian',
            'dinner': 'Chapati, Dal, Veg'
        },
        'Friday': {
            'breakfast': 'Idli, Vada, Chutney',
            'lunch': 'Rice, Curry, Chicken',
            'dinner': 'Roti, Butter Chicken'
        },
        'Saturday': {
            'breakfast': 'Poori, Bhaji, Sweet',
            'lunch': 'Special Lunch, Ice Cream',
            'dinner': 'Special Dinner'
        },
        'Sunday': {
            'breakfast': 'Pongal, Vada, Chutney',
            'lunch': 'Rice, Dal, Veg Curry, Sweet',
            'dinner': 'Roti, Paneer, Dessert'
        }
    }
    m = menu.get(day, menu['Monday'])
    return jsonify({
        'day': day,
        'breakfast': m['breakfast'],
        'lunch': m['lunch'],
        'dinner': m['dinner']
    })

# ===== STATS =====

@app.route('/api/stats', methods=['GET'])
def get_stats():
    if 'user_id' not in session:
        return jsonify({'total': 0, 'pending': 0, 'resolved': 0, 'leaves': 0})
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    if not student:
        return jsonify({'total': 0, 'pending': 0, 'resolved': 0, 'leaves': 0})
    
    total = Complaint.query.filter_by(student_id=student.id).count()
    pending = Complaint.query.filter_by(student_id=student.id, status='pending').count()
    resolved = Complaint.query.filter_by(student_id=student.id, status='resolved').count()
    leaves = LeaveRequest.query.filter_by(student_id=student.id).count()
    
    return jsonify({
        'total_complaints': total,
        'pending_complaints': pending,
        'resolved_complaints': resolved,
        'leave_requests': leaves
    })

# ===== ADMIN API ROUTES =====

@app.route('/api/admin/complaints', methods=['GET'])
def admin_get_complaints():
    denied = require_admin()
    if denied:
        return denied
    complaints = (db.session.query(Complaint, User.name)
                  .outerjoin(Student, Complaint.student_id == Student.id)
                  .outerjoin(User, Student.user_id == User.id)
                  .order_by(Complaint.created_at.desc()).all())
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'description': c.description,
        'category': c.category,
        'priority': c.priority,
        'status': c.status,
        'student_id': c.student_id,
        'student_name': student_name or 'Unknown student',
        'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
    } for c, student_name in complaints])

@app.route('/api/admin/complaints/<int:complaint_id>', methods=['PUT'])
def admin_update_complaint(complaint_id):
    denied = require_admin()
    if denied:
        return denied
    complaint = db.session.get(Complaint, complaint_id)
    if not complaint:
        return jsonify({'error': 'Complaint not found'}), 404
    
    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    
    if new_status not in ['pending', 'in_progress', 'resolved', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400
    
    complaint.status = new_status
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Complaint status updated to {new_status}'})

@app.route('/api/admin/leave', methods=['GET'])
def admin_get_leave():
    denied = require_admin()
    if denied:
        return denied
    leaves = (db.session.query(LeaveRequest, User.name)
              .outerjoin(Student, LeaveRequest.student_id == Student.id)
              .outerjoin(User, Student.user_id == User.id)
              .order_by(LeaveRequest.created_at.desc()).all())
    return jsonify([{
        'id': l.id,
        'student_id': l.student_id,
        'student_name': student_name or 'Unknown student',
        'from_date': l.from_date.strftime('%Y-%m-%d'),
        'to_date': l.to_date.strftime('%Y-%m-%d'),
        'reason': l.reason,
        'status': l.status
    } for l, student_name in leaves])

@app.route('/api/admin/leave/<int:leave_id>', methods=['PUT'])
def admin_update_leave(leave_id):
    denied = require_admin()
    if denied:
        return denied
    leave = db.session.get(LeaveRequest, leave_id)
    if not leave:
        return jsonify({'error': 'Leave request not found'}), 404
    
    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    
    if new_status not in ['pending', 'approved', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400
    
    leave.status = new_status
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Leave request {new_status}'})

# ==================== RUN APP ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("✅ Server running at http://localhost:5000")
    print("📋 Admin Panel: http://localhost:5000/admin")
    app.run(debug=True, port=5000)
