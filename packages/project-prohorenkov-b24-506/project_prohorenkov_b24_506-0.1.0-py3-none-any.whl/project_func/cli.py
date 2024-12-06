def welcome():
    print("Первая попытка запустить проект!")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    
    while True:
        user_input = input("Введите команду: ").strip().lower()
        
        if user_input == "exit":
            print("Выход из программы...")
            break
        elif user_input == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            print(f"Неизвестная команда: {user_input}")
