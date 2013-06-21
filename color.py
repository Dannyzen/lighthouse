from colorama import init, Fore
def colorPrint(state,message):
    """ Prints red if state is 0, green if state is 1 """
    if state == 0:
        print(Fore.RED + message + Fore.RESET)
    if state == 1:
        print (Fore.GREEN + message + Fore.RESET)
