from app import create_app
from flask_script import Server, Manager, Shell
from flask_migrate import MigrateCommand
from app.extensions import *
from app import models

def _make_context():
    return dict(app=create_app, db=db, models=models)

manager = Manager(create_app)
manager.add_command("runserver", Server())
manager.add_command("db", MigrateCommand)
manager.add_command('shell', Shell(make_context=_make_context))

if __name__=="__main__":
    manager.run()