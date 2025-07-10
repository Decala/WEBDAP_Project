class Services:
    all_services = []

    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.__class__.all_services.append(self)


def clear_service():
    Services.all_services = []