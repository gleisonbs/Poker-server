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
        print(f'You chose {option}')

        if (option == '1'):
            pass
        elif (option == '2'):
            pass
        elif (option == '3'):
            pass
        else:
            print("What?")