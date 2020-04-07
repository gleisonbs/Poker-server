class MainMenu:
    @staticmethod
    def get():
        return """
         /$$$$$$$           /$$                          
        | $$__  $$         | $$                          
        | $$  \ $$ /$$$$$$ | $$   /$$  /$$$$$$   /$$$$$$ 
        | $$$$$$$//$$__  $$| $$  /$$/ /$$__  $$ /$$__  $$
        | $$____/| $$  \ $$| $$$$$$/ | $$$$$$$$| $$  \__/
        | $$     | $$  | $$| $$_  $$ | $$_____/| $$      
        | $$     |  $$$$$$/| $$ \  $$|  $$$$$$$| $$      
        |__/      \______/ |__/  \__/ \_______/|__/      
        

        1. Join table
        2. Create table
        3. List tables

        : """

    @staticmethod
    def choose_option():
        option = input()

        if (option == '1'):
            print(f'You chose 1')
        elif (option == '2'):
            print(f'You chose 2')
        elif (option == '3'):
            print(f'You chose 3')
        else:
            print("What?")