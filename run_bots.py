import sys, os, re
import threading
from IG_like import Like_bot
from IG_follow_unfollow import Follow_bot
import time
from getpass import getpass
try:
    import msvcrt
except:
    import termios

username = ''
password = ''

if len(sys.argv) > 1:
    username = sys.argv[1]
    try:
        password = sys.argv[2]
    except:
        pass
follow_accounts = []
whitelist = []

like = Like_bot()
follow = Follow_bot()

def setup():
    for bot in bots_mappings.values():
        try: 
            bot.setup(username)
        except:
            pass
    
def set_username(_):
    global username
    print("Enter username:")
    username = input("")
    print(f"username: {username} - success")

def set_password(_):
    global password
    print("Enter password - password will not show up as you type")
    password = getpass()
    print(f"password change - success")

def start(bot):
    if username == '' or password == '':
        print('Set username and password')
        return
    def run_bot(username, password):
            bot.run(username, password)
    x = threading.Thread(target=run_bot, args=(username, password))
    x.start()

def start_all(_):
    if username == '' or password == '':
        print('Set username and password')
        return
    for bot in bots_mappings.values():
        start(bot)

def stop(bot):
    bot.terminate()

def stop_all(_):
    for bot in bots_mappings.values():
        bot.terminate()

def set_follow_direction(direction):
    if 'true' in direction:
        print("Bot is now following")
        follow.follow_direction = True
    if 'false' in direction:
        print("Bot is now unfollowing")
        follow.follow_direction = False

def set_output(bot):
    bot.set_output(not bot.get_output())

def flush_input():
    try:
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def help(_):
    print(" " + 40*"_" + "\n|"+ 40*" " + "|" + "\n|             //// Help ////             |\n" + "|" + 40*"_" + "|")
    print(f"""

        available bots: like-bot, follow-bot
        --------------------------------------
        
        Commands:

        username -enter-> <YOUR-INSTAGRAM-USERNAME>
        password -enter-> <YOUR-INSTAGRAM-PASSWORD>
        
        run <bot-name>
        stop <bot-name>
        runall
        stopall

        follow <true/false> - 'false' starts bot in unfollow mode - can be used while running. default = false
        upper <number value> - the upper bounds. ie follow-bot switches from follow to unfollow at this boundry
        lower <number value> - the lower bounds. ie follow-bot switches from unfollow to follow at this boundry

        output <bot-name> - toggle bots output string
        quit
    """) 

def _quit(_):
    global running
    running = False
    
function_mappings = {
    'username': set_username,
    'password': set_password,
    'run': start,
    'runall': start_all,
    'stop': stop,
    'stopall': stop_all,
    'follow' : set_follow_direction,
    'output': set_output,
    'help': help,
    'quit': _quit,
}

bots_mappings = {
    'like-bot': like,
    'follow-bot': follow,
}

wait = time.time()
os.system('cls' if os.name == 'nt' else 'clear')
print(" " + 40*"_" + "\n|"+ 40*" " + "|" + "\n|   //// Instagram Automation Bot ////   |\n" + "|" + 40*"_" + "|")
print("\nEnter a command. For a list of commands enter 'help'")

running = True
try:
    while running:
        
        if username != '' and password != '':
            print('ok')
            setup()
        
        flush_input()
        cmd = input("").split()
        try:
            try:
                args = bots_mappings[cmd[1]]
            except:
                try:
                    args = cmd[1]
                except:
                    args = 1
            function_mappings[cmd[0]](args)
        except:
            print(f"Failed to execute your command")
    else:
        for key in bots_mappings.keys():
            stop(bots_mappings[key])
        os.system('cls' if os.name == 'nt' else 'clear')
except:

    for key in bots_mappings.keys():
            stop(bots_mappings[key])
    os.system('cls' if os.name == 'nt' else 'clear')