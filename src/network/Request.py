from enum import Enum

class RequestType(Enum):
    CREATE_TABLE = 'create_table'
    JOIN_TABLE = 'join_table'
    LIST_TABLE = 'list_tables'

def is_valid_request(request):
    if ':' not in request:
        return False
    
    parameters = request.split(':')

    return create_table_specification(parameters) \
            or join_table_specification(parameters) \
            or list_tables_specification(parameters)

def create_table_specification(parameters):
    return len(parameters) == 4 and parameters[1] == 'create_table'

def join_table_specification(parameters):
    return len(parameters) == 3 and parameters[1] == 'join_table'

def list_tables_specification(parameters):
    return len(parameters) == 2 and parameters[1] == 'list_tables'

class Request():
    def __init__(self, request):
        self.parameters = self.parse(request)
        self.type = self.get_request_type()
        self.value = self.get_request_value()

    def parse(self, request):
        try:
            if is_valid_request(request):
                return request.split(':')
            else:
                raise Exception(f'Invalid request\n{request}')
                        
        except Exception as ex:
            print(ex)
            return []
    
    def get_request_type(self):
        if not self.parameters:
            return None
        return RequestType(self.parameters[1])

    def get_request_value(self):
        if not self.parameters:
            return None
        return self.parameters[2:]
    
    def __str__(self):
        print(f'str {self.parameters}')
        if not self.parameters:
            return ''
        return ' - '.join(self.parameters)