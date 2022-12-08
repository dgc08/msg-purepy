from requests import get

class UserException(Exception):
    pass


def simple_getter(route, args, json, custom_server):
    x = get(custom_server+route, params=args)
    if x.status_code == 200 and json:
        return x.json()
    elif x.status_code == 200:
        return x.text
    return None

class User:
    _password = ""
    _alias = ""
    _address = ""
    uns = ""
    server = ""

    def logged_in(self):
        if self._password == "":
            return False
        return True

    def fetch(self):
        if self._password == "":
            raise UserException("No token/password provided")
        msgs = simple_getter("/check", {"password": self._password}, True, self.server)
        return msgs


    def send(self, msg, recipient: 'User'):
        if recipient.get_address() == "":
            raise UserException("The recipient has no address to send to")
        if self._password == "":
            raise UserException("No token/password provided")
        res = simple_getter("/send", {"password": self._password, "msg": msg, "recipient": recipient.get_address()}, False, self.server)
        if res != "0":
            return False
        else:
            return True


    def login(self, password: str):
        self._password = password
        self._address = simple_getter("/getusr", {"password": password}, False, self.server)
        ret = simple_getter("/get/address", {"address": self._address}, False, self.uns)
        if ret is None:
            return None

        if ret.strip() == "":
            ret = None

        self._alias = ret

    def resolve_uns(self, name):
        ret = simple_getter("/get/name", {"name": name}, False, self.uns)
        if ret is None:
            return None

        if ret.strip() == "":
            ret = None
        self._alias = name
        self._address = ret
    def set_address(self, hash_address):
        self._address = hash_address

    def get_alias(self):
        return self._alias

    def get_address(self):
        return self._address
