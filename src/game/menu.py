import table

class Menu:
    def __init__(self):
        self.menu_text = """
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

    def display(self):
        print(self.menu_text, end='')
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


menu = Menu()
menu.display()