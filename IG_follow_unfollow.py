from InstagramAPIwrapper import InstagramAPIwrapper
from itertools import cycle
import time as t
from re import sub


class Follow_bot():
    def __init__(self):

        self._running = False
        self.whitelist = []
        self.follow_accounts = []
        self.lower = 200
        self.upper = 4000
        self.ratelimit_timer = 300
        self.task_delay = 45
        self.following_count = 100
        self.follow_direction = False
        self.follower_count = 50
        self.output_on = True

    def setup(self, username):
        try:
            with open(f"{username}_follow_accounts.txt", "r") as f:
                for name in f:
                    name = sub('\n', '', name)
                    self.follow_accounts.append(int(name))
        except:
            with open(f"{username}_follow_accounts.txt", "w+") as f:
                pass
        try:
            with open(f"{username}_whitelist.txt", "r") as f:
                for name in f:
                    name = sub('\n', '', name)
                    self.whitelist.append(name)
        except:
            with open(f"{username}_whitelist.txt", "w+") as f:
                pass

            print('Finished setup....')

    def terminate(self):
        if not self._running:
            print('Bot is not running')
            return
        print('Shutting down Follow bot....')
        self._running = False

    def output(self, string):
                if self.output_on:
                        print(string)
    
    def set_output(self, state):
                self.output_on = state
                print(f'Follow-Bot: output:{state}')

    def get_output(self):
            return self.output_on

    def run(self, username, password):
        print("Starting Follow bot....")
        self._running = True

        w = InstagramAPIwrapper()
        w.login(username, password)
        whitelist_ids = []



        self.follow_accounts = cycle(self.follow_accounts)
        next_acc = next(self.follow_accounts)

        for user in self.whitelist:
            whitelist_ids.append(w.get_user_id(user))
            t.sleep(0.5)

        whitelist_ids = set(whitelist_ids)

        my_id = w.id

        wlist = len(self.whitelist)
        wait = t.time() - 60
        wait_time = 60

        while self._running:
            
            while t.time() - wait < wait_time:
                # Do things while we wait
                if not self._running:
                        break
            if not self._running:
                break
            my_following_count = w.get_user_following_count(my_id)

            if my_following_count <= self.lower:
                self.follow_direction = True
                
            elif my_following_count >= self.upper:
                self.follow_direction = False

            this_acc, next_acc = next_acc, next(self.follow_accounts)

            if my_following_count < self.following_count:
                self.following_count = my_following_count    
            
            elif my_following_count - self.lower < self.following_count and not self.follow_direction:
                self.following_count = my_following_count - self.lower + wlist

            elif self.upper - my_following_count < self.following_count and self.follow_direction:
                self.follower_count = self.upper - my_following_count

            if self.follow_direction:
                task_delay = 120
                self.output('Follow-Bot: following')
                users = w.get_user_followers(this_acc, count=self.follower_count)
            else:
                task_delay = 45
                self.output('Follow-Bot: unfollowing')
                users = w.get_user_following(my_id, count=self.following_count)

            flow_change = self.follow_direction
            t.sleep(1)
            for user in users: 
                while t.time() - wait < wait_time:
                    if flow_change != self.follow_direction:
                        break
                    if not self._running:
                        break
                if flow_change != self.follow_direction:
                        break
                if not self._running:
                        break
                if user in whitelist_ids:
                    self.output('Follow-Bot: skipped whitelisted user')
                    continue
                if self.follow_direction:
                    r = w.follow_user(user)

                else:
                    r = w.unfollow_user(user)
                
                self.output("Follow-Bot: " + str(r))

                if r == 429:
                    self.output("Follow-Bot: too fast!")
                    wait = t.time()
                    wait_time = self.ratelimit_timer
                else:
                    wait = t.time()
                    wait_time = task_delay
            if not self._running:
                    break
            if flow_change == self.follow_direction:
                self.output(f'Follow-Bot: cycle complete: sleeping {self.ratelimit_timer} seconds')
                wait_time = self.ratelimit_timer
            else:
                wait = t.time()
                wait_time = 0

        print("Follow bot shutdown successful")