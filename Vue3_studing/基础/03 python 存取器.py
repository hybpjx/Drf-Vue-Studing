from hashlib import md5


class User(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password

    # getter 取数据
    @property
    def password(self):
        return self._password

    # setter 存数据
    @password.setter
    def password(self, password):
        self._password = md5(password.encode()).hexdigest()


if __name__ == '__main__':
    xm = User("a", "1234")
    print(xm.name)
    print(xm.password)
