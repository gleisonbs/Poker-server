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
        has_4_parameters = len(parameters) == 4
        max_players = parameters[3]
        has_valid_max_players = max_players.isnumeric() \
            and int(max_players) >= 2 \
            and int(max_players) <= 10
        return has_4_parameters and has_valid_max_players

    def join_table_specification(self, parameters):
        return len(parameters) == 3

    def list_tables_specification(self, parameters):
        return len(parameters) == 2

    def list_players_specification(self, parameters):
        return len(parameters) == 2