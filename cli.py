from cli import Store, MainMenu

if __name__ == "__main__":
    store = Store()
    mainMenu = MainMenu(store)
    mainMenu.execute()
