from db import Users, session


class UserModel():

    __tablename__ = 'rm_users'

    def __init__(self, username=None, email=None, password=None, firstname=None, lastname=None, address=None):
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.address = address

    def json(self, username, email, firstname, lastname, address):
        return {
            'username': username,
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'address': address
        }

    def find_by_email(self, email):
        return session.query(Users).filter_by(email=email).first()

    def find_by_username(self, _username):
        return session.query(Users).filter_by(username=_username).first()

    def save_to_db(self):
        new_user = Users(
            username=self.username,
            email=self.email,
            password=self.password,
            firstname=self.firstname,
            lastname=self.lastname,
            address=self.address
        )
        session.add(new_user)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()
