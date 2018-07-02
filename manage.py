from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate
from app import create_app, db

# app = create_app('default')
app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)    # 用于数据库迁移


@manager.command
def deploy():
    """应用程序的初始化配置，主要是数据库基础数据配置"""
    from flask_migrate import upgrade
    from app.models import School, Permission, Role, User
    # db.drop_all()
    # db.create_all()
    upgrade()
    School.insert_basic_schools()
    Permission.insert_basic_permission()
    Role.insert_basic_roles()
    User.insert_admin_user()
    return '配置成功'


@manager.command
def test_set():
    """应用程序测试环境数据配置"""
    from app.models import User, School, TrainStudent

    def test_user():
        for i in range(15):
            i = str(i)
            user = User(username='用户' + i,
                        email=i+'@test.cn',
                        password='123456',
                        school=School.query.filter_by(school_name=app.config['ADMIN_SCHOOL']).first(),
                        real_name='实名'+i,
                        student_number='20141041221'+i)
            db.session.add(user)
        db.session.commit()

    def test_train_student():
        for one in User.query.all():
            if one.username == 'admin':
                continue
            student = TrainStudent(resume='我热爱数学建模，并为之努力学习，从模型结构到代码实现，我是'+one.username,
                                   user=one,
                                   verify_status=False,
                                   school=one.school)
            db.session.add(student)
        db.session.commit()

    test_user()
    test_train_student()

    return '测试数据配置成功'


def make_shell_context():
    """添加shell中的命令"""
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)    # 用于数据库迁移

if __name__ == '__main__':
    manager.run()
