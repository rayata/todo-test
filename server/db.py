import sqlite3
import logging

logger = logging.getLogger()

db_file = 'db.sqlite'


class ManageTodoDB:

    def connect_db(self):
        try:
            db = sqlite3.connect(db_file)
            logger.info("Connected to DB: %s", db_file)
            return db
        except sqlite3.Error as e:
            logger.error('Error connecting to DB: %s', e)

    # Create tables
    def create_db_struct(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name VARCHAR(250) NOT NULL,
                task_description VARCHAR(1000) NOT NULL,
                task_assignee INTEGER NOT NULL,
                task_start_date DATE, task_end_date DATE,
                FOREIGN KEY (task_assignee) REFERENCES users(user_id)
            );
                 
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name VARCHAR(50) NOT NULL
            );
              '''
        c = self.connect_db().cursor()
        try:
            c.executescript(sql)
            logger.info("DB structure was created!")
        except sqlite3.Error as e:
            logger.error("Error creating DB: %s", e)
            return e

    # Add new user
    def add_user(self, username):
        sql = '''
            INSERT INTO users (user_name) VALUES("{:s}")    
        '''.format(username)
        c = self.connect_db().cursor()
        try:
            c.executescript(sql)
            logger.info("Successfully added user %s", username)
        except sqlite3.Error as e:
            logger.error("Error adding user %s. Message: %s", username, e)
            return e

    # Add new task
    def add_task(self, name, description, assignee, start_date, end_date):

        user_id = self.get_user_id(assignee)

        sql = '''
            INSERT INTO tasks (task_name, task_description, task_assignee, task_start_date, task_end_date)
            VALUES("{:s}", "{:s}", {:d}, "{:s}", "{:s}")
        '''.format(name, description, user_id, start_date, end_date)

        c = self.connect_db().cursor()
        try:
            c.executescript(sql)
            logger.info("Successfully added task: %s", name)
        except sqlite3.IntegrityError as e:
            logger.error("DB integrity error: %s", e)
            return e

    # Helper  method to user id by name
    def get_user_id(self, user_name):

        sql = '''
            SELECT user_id FROM users WHERE user_name="{:s}"
        '''.format(user_name)

        c = self.connect_db().cursor()
        user_id = c.execute(sql).fetchone()[0]

        return user_id

    # Remove all tables
    def remove_tables(self):
        sql = '''
            DROP TABLE IF EXISTS tasks;
            DROP TABLE IF EXISTS users;
        '''
        c = self.connect_db().cursor()

        return c.executescript(sql)
