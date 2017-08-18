#encoding:utf-8
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from exts import db
from ifsys import app

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app,db)
# 添加迁移脚本命令到manage中
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    db.init_app(app)
    # with app.test_request_context():
    #     db.create_all()
    manager.run()