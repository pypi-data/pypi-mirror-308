from scod.modules import Client, Group, Owner, Profile, Property, Uploader, User

class Scod(Client, Group, Owner, Profile, Property, Uploader, User):
    def __init__(self, token: str) -> None:
        self.__headers = {"Authorization": token, "User-Agent": "insomnia/8.4.5"}
