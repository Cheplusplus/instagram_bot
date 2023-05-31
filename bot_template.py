from InstagramAPIwrapper import InstagramAPIwrapper
import time as t
from random import choice

class bot:
        def __init__(self, name):
                self._running = False
                self.output_on = True
                self.name = name

        def output(self, string):
                if self.output_on:
                        print(string)

        def set_output(self, state):
                self.output_on = state
                print(f'{self.name}: output:{state}')

        def get_output(self):
                return self.output_on

        def terminate(self):
                if not self._running:
                        print('Bot is not running')
                        return
                print(f'Shutting down {self.name}....')
                self._running = False

        def run(self, username, password, task_delay= 22):          
                print(f"Starting {self.name}....")      
                self._running = True
                w = InstagramAPIwrapper()
                w.login(username, password)
                somecondition = True
                while self._running:

                        # Logic code goes here
                        if somecondition:
                            break 
                                        
                print(f"{self.name} shutdown successful")


        