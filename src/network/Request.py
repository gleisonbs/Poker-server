from enum import Enum
from RequestSpecification import RequestSpecification

class RequestType(Enum):
    CREATE_TABLE = 'create_table'
    JOIN_TABLE = 'join_table'
    LIST_TABLES = 'list_tables'
    LIST_PLAYERS = 'list_players'

class Request():
    def __init__(self, request):
        self.is_valid = self.is_valid_request(request)
        if self.is_valid:
            self.parameters = request.split(':')
            self.type = self.get_request_type()
            self.value = self.get_request_value()
            self.player = self.get_player()

    def is_valid_request(self, request):
        return RequestSpecification().is_satisfied_by(request)       

    def get_player(self):
        return self.parameters[1]
    
    def get_request_type(self):
        return RequestType(self.parameters[0])

    def get_request_value(self):
        return self.parameters[2:]
    
    def __str__(self):
        return self.parameters and ' - '.join(self.parameters)