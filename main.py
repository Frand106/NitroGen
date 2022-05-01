import string
import time
import asyncio
import aiohttp

try:  # Setup try statement to catch the error
    import requests  # Try to import requests
except ImportError:  # If it has not been installed
    # Tell the user it has not been installed and how to install it
    input(
        "Модуль requests не установлен. Чтобы установить его, напишите 'pip install requests' в консоль."
        "\nНажмите Enter, чтобы завершить программу.")
    exit()  # Exit the program
try:  # Setup try statement to catch the error
    import numpy  # Try to import requests
except ImportError:  # If it has not been installed
    # Tell the user it has not been installed and how to install it
    input(
        "Модуль numpy не установлен. Чтобы установить его, напишите 'pip install numpy' в консоль."
        "\nНажмите Enter, чтобы завершить программу.")
    exit()  # Exit the program

# check if user is connected to internet
url = "https://t.me/localka"
try:
    response = requests.get(url)  # Get the responce from the url
    print("Интернет на месте, работаем")
except requests.exceptions.ConnectionError:
    # Tell the user
    input("Похоже, у вас отсутствует подключение к интернету."
          "\nНажмите Enter, чтобы завершить программу.")
    exit()  # Exit program


class NitroGen:  # Initialise the class
    def __init__(self):  # The initaliseaiton function
        self.fileName = "Nitro Codes.txt"  # Set the file name the codes are stored in
        self.valid = []  # Keep track of valid codes

    async def main(self):  # The main function contains the most important code
        # Print the first question
        num = input('Сколько кодов сгенерировать и проверить?: ')
        #start_time = time.time()
        if num.isdigit():
            num = int(num)  # Ask the user for the amount of codes
        else:
            input("Вы не ввели цифру.\n"
                  "Нажмите Enter, чтобы завершить программу.")
            exit()  # Exit program

        chars = []
        chars[:0] = string.ascii_letters + string.digits

        c = []

        # generate codes faster than using random.choice
        for i in range(num):
            c.append(''.join(numpy.random.choice(chars, size=23)))
        for s in c:  # Loop over the amount of codes to check
            task = asyncio.create_task(self.checker(s))
            await task


        print(f"""
Итоги работы:
 Валидов: {len(self.valid)}
 Невалидов: {num - len(self.valid)}
 Список валиды: {', '.join(self.valid)}""")  # Give a report of the results of the check

        #print("--- %программа выполнилась за ---" % (time.time() - start_time))

    async def checker(self, s):
        try:
            result = asyncio.create_task(self.quickChecker(s))  # Check the codes
            if await result:  # If the code was valid
                # Add that code to the list of found codes
                self.valid.append(s)

        except Exception as e:  # If the request fails
            print(f" Error | " + str(e))  # Tell the user an error occurred

    async def quickChecker(self, nitro: str, notify=None):  # Used to check a single code at a time
        # Generate the request url
        nitro = 'https://discord.gift/' + nitro
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
            ) as resp:
                status_code = resp.status

        if status_code == 200:  # If the responce went through
            # Notify the user the code was valid
            print(f" Valid | " + nitro)
            with open("Nitro Codes.txt", "w") as file:  # Open file to write
                # Write the nitro code to the file it will automatically add a newline
                file.write(str(nitro) + '\n')

            return True  # Tell the main function the code was found

        # If the responce got ignored or is invalid ( such as a 404 or 405 )
        else:
            # Tell the user it tested a code and it was invalid
            print(f" Invalid | " + nitro)
            return False  # Tell the main function there was not a code found


if __name__ == '__main__':
    Gen = NitroGen()  # Create the nitro generator object
    asyncio.run(Gen.main())  # Run the main code
