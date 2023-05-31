from InstagramAPIwrapper import InstagramAPIwrapper
import time as t
from random import choice


class Like_bot:
        def __init__(self):
                self._running = False
                self.output_on = True
                self.ratelimit = 300

        def terminate(self):
                if not self._running:
                        print('Bot is not running')
                        return
                print('Shutting down Like bot....')
                self._running = False


        def run(self, username, password, task_delay= 45):          
                print("Starting Like bot....")      
                self._running = True
                w = InstagramAPIwrapper()
                w.login(username, password)
                user = w.get_user_id('jodiwindvogel')
                fallback = w.get_user_followers(user_id=user)
                init_time = task_delay
                t.sleep(1)
                while self._running:
                        followers = w.get_user_followers(user_id=user)
                        if len(followers) == 0:
                                user = choice(fallback)
                                continue
                        
                        user = choice(followers)
                        t.sleep(1)
                        for follower in followers:
                                if not self._running:
                                        break
                                
                                media = w.get_user_media(follower, count=2)
                                wait = t.time() - init_time
                                for med in media:
                                        while t.time() - wait < task_delay:
                                                if not self._running:
                                                        break
                                        if not self._running:
                                                break
                                        init_time = 0
                                        res = w.like_post(med)        
                                        self.output("Like-Bot: " + str(res))
                                        wait = t.time()
                                        if res == 400:
                                                self._running = False
                                        
                print("Like bot shutdown successful")


        def output(self, string):
                if self.output_on:
                        print(string)

        def set_output(self, state):
                self.output_on = state
                print(f'Like-Bot: output:{state}')

        def get_output(self):
                return self.output_on

