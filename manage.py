# -*- encoding: utf-8 -*-

from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate
from app import create_app, db
from app.models import Role, TrainFileType, TrainFiles

app = create_app('development')

manager = Manager(app)
migrate = Migrate(app, db)    # 用于数据库迁移


@manager.command
def deploy():
    """
    Run deployment tasks.
    """
    from app import db
    from app.models import Role, TrainFileType

    db.drop_all()
    db.create_all()
    Role.insert_roles()
    TrainFileType.insert_types()


def make_shell_context():
    """
    添加shell中的命令
    :return:
    """
    return dict(app=app, db=db, Role=Role, TrainFileType=TrainFileType, TrainFiles=TrainFiles)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)    # 用于数据库迁移

if __name__ == '__main__':
    manager.run()
