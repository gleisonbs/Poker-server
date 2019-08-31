class RequestSpecification:
    def __init__(self):
        self.specifications = {
            'create_table': self.create_table_specification,
            'join_table': self.join_table_specification,
            'list_tables': self.list_tables_specification,
            'list_players': self.list_players_specification
        }

    def is_satisfied_by(self, request):
        if ':' not in request:
            return False

        parameters = request.split(':')
        action = parameters[0]

        if action in self.specifications:
            return self.specifications[action](parameters)

    def create_table_specification(self, parameters):
        return len(parameters) == 4

    def join_table_specification(self, parameters):
        return len(parameters) == 3

    def list_tables_specification(self, parameters):
        return len(parameters) == 2

    def list_players_specification(self, parameters):
        return len(parameters) == 2