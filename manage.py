from flask_script import Manager, Server
from twitter import app
from flask_migrate import MigrateCommand


# Creating instance of manager to run command from CLI
manager = Manager(app)
# Adding a command to migrate the database using Flask-Migrate
manager.add_command('db', MigrateCommand)
# Adding a command to start the app from respective server configuration
manager.add_command('runserver', Server(use_debugger=True,
                                       use_reloader=True,
                                       host='0.0.0.0',
                                       port=9000))

# Running the app if it is called from this main file.
if __name__ == '__main__':
    manager.run()