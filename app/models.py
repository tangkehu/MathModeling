from app import db


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(128), nullable=False, unique=True)
    user = db.relationship('User', backref='school')


relation_role_permission = db.Table(
    'relation_role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(32), nullable=False, unique=True)
    permission_description = db.Column(db.String(64), nullable=False)
    role = db.relationship('Role',
                           secondary=relation_role_permission,
                           backref=db.backref('permission', lazy='dynamic'),
                           lazy='dynamic')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(32), nullable=False, unique=True)
    is_default = db.Column(db.Boolean)
    user = db.relationship('User', backref='role')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(64), nullable=False)
    real_name = db.Column(db.String(32))
    student_number = db.Column(db.String(16), unique=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
