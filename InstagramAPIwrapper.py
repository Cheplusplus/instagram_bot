import re, os
from requests import get, post, Session
from datetime import datetime


username = 'castro_witha_sauce'
password = 'Che0718584040!'


class InstagramAPIwrapper:
        
        session: Session = Session()

        link: str = 'https://www.instagram.com/accounts/login/'
        login_url: str = 'https://www.instagram.com/accounts/login/ajax/'
        pvt_api: str = 'https://i.instagram.com/api/v1'
        web_url: str = 'https://www.instagram.com/web'

        def login(self, username, password) -> None:
                try:
                        open(f'{username}_cookies.txt', 'x')
                except:
                        self.use_stored_cookies(username)
                        return

                time = int(datetime.now().timestamp())
                
                payload = {
                        'username': username,
                        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',  # <-- note the '0' - that means we want to use plain passwords
                        'queryParams': {},
                        'optIntoOneTap': 'false'
                }

                r = self.session.get(self.link)

                self.session.cookies['x-csrftoken'] = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]

                r = self.session.post(self.login_url,data=payload,headers={
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
                        "x-requested-with": "XMLHttpRequest",
                        "referer": "https://www.instagram.com/accounts/login/",
                        "x-csrftoken":self.session.cookies['x-csrftoken']
                }).json()

                if not r['authenticated']:
                        os.remove(f"{username}_cookies.txt")
                        return "login failed"
                with open(f'{username}_cookies.txt', 'w') as f:
                        for cookie in self.session.cookies.values():
                                f.write(cookie + '\n')

                return

        def use_stored_cookies(self, username) -> None:
                """Helper function for getting the stored cookies and adding them to the session"""
                try:
                        lines = []
                        with open(f'{username}_cookies.txt', 'r') as f:
                                lines = f.read().splitlines()
                                
                        self.session.cookies['x-csrftoken'] = lines[0]
                        self.session.cookies['csrftoken'] = lines[1]
                        self.session.cookies['dsuserid'] = lines[2]
                        self.session.cookies['ig_did'] = lines[3]
                        self.session.cookies['ig_nrcb'] = lines[4]
                        self.session.cookies['mid'] = lines[5]
                        self.session.cookies['rur'] = lines[6]
                        self.session.cookies['sessionid'] = lines[7]
                        print("Login Success")
                except:
                        os.remove(f"{username}_cookies.txt")
                        return "Login failed"

        @property
        def default_headers(self):
                return {
                        'Host': 'i.instagram.com',
                        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'X-CSRFToken': self.session.cookies['x-csrftoken'],
                        'X-IG-App-ID': '936619743392459',
                        'X-ASBD-ID': '198387',
                        'X-IG-WWW-Claim': 'hmac.AR1Nqxc4MvdDRFb0suptHWht0hSgdm91lyeOT77eWLqJ20PI',
                        'Origin': 'https://www.instagram.com',
                        'Alt-Used': 'i.instagram.com',
                        'Connection': 'keep-alive',
                        'Referer': 'https://www.instagram.com/',
                        'Cookie': f"""  mid={self.session.cookies['mid']}; 
                                        ig_did={self.session.cookies['ig_did']}; 
                                        ig_nrcb={self.session.cookies['ig_nrcb']}; 
                                        datr=yqqbYv8WlKnrgYUIH0fxB3gR; 
                                        csrftoken={self.session.cookies['x-csrftoken']}; 
                                        ds_user_id={self.session.cookies['dsuserid']}; 
                                        sessionid={self.session.cookies['sessionid']};""",
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'Sec-GPC': '1',
                }

        @property
        def public_headers(self):
                return {
                        "Host": "www.instagram.com",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
                        "Accept": "*/*",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate, br",
                        "X-CSRFToken": self.session.cookies['x-csrftoken'],
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-Requested-With": "XMLHttpRequest",
                        "Origin": "https://www.instagram.com",
                        "Alt-Used": "www.instagram.com",
                        "Connection": "keep-alive",
                        "Referer": "https://www.instagram.com/",
                        "Cookie": f"""  csrftoken={self.session.cookies['x-csrftoken']}; 
                                        ds_user_id={self.session.cookies['dsuserid']}; 
                                        sessionid={self.session.cookies['sessionid']}""",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-GPC": "1",
                }

        @property
        def like_header(self):
                return {
                        'Host': 'www.instagram.com',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'X-CSRFToken': self.session.cookies['x-csrftoken'],
                        'X-Instagram-AJAX': '1005664968',
                        'X-IG-App-ID': '936619743392459',
                        'X-ASBD-ID': '198387',
                        'X-IG-WWW-Claim': 'hmac.AR1Nqxc4MvdDRFb0suptHWht0hSgdm91lyeOT77eWLqJ20PI',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Origin': 'https://www.instagram.com',
                        'Alt-Used': 'www.instagram.com',
                        'Connection': 'keep-alive',
                        'Referer': 'https://www.instagram.com/p/CemcOeKOO0j/',
                        'Cookie': f"""  mid={self.session.cookies['mid']}; 
                                        ig_did={self.session.cookies['ig_did']}; 
                                        ig_nrcb={self.session.cookies['ig_nrcb']}; 
                                        datr=yqqbYv8WlKnrgYUIH0fxB3gR; 
                                        csrftoken={self.session.cookies['x-csrftoken']}; 
                                        ds_user_id={self.session.cookies['dsuserid']}; 
                                        sessionid={self.session.cookies['sessionid']};""",
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-GPC': '1',
                }

        @property
        def media_headers(self):
                return {
                        'Host': 'i.instagram.com',
                        'user-agent':'Instagram 219.0.0.12.117 Android',
                        'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Access-Control-Request-Method': 'GET',
                        'Access-Control-Request-Headers': 'x-asbd-id,x-csrftoken,x-ig-app-id,x-ig-www-claim',
                        'Referer': 'https://www.instagram.com/',
                        'Origin': 'https://www.instagram.com',
                        'Connection': 'keep-alive',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'Sec-GPC': '1',
                }


        def like_post(self, post_id):
                r = post(f'{self.web_url}/likes/{post_id}/like/', headers=self.like_header)
                return r.status_code


        def is_user_new(self, user_id):
                username = self.get_user_username(user_id)
                r = get(f'{self.pvt_api}/users/web_profile_info/?username={username}', headers=self.default_headers)
                if "<!DOCTYPE html>" in r.text:
                        return 0
                is_new = re.findall("\"is_joined_recently\":(.*?),",r.text)[0]
                return is_new


        def get_user_id(self, username):
                r = get(f'{self.pvt_api}/users/web_profile_info/?username={username}', headers=self.default_headers)
                if "<!DOCTYPE html>" in r.text:
                        return 0
                user_id = re.findall("\"id\":\"(\d+)\"",r.text)[0]
                return user_id


        def get_user_username(self, user_id):
                r = self.session.get(f'{self.pvt_api}/users/{user_id}/info', headers=self.default_headers)
                if "<!DOCTYPE html>" in r.text:
                        return 0
                username = re.findall("\"username\":\"(.*?)\"",r.text)[0]
                return username


        def get_user_media(self, user_id, count = 5):
                r = self.session.get(f'{self.pvt_api}/feed/user/{user_id}/', headers=self.media_headers)
                media_id = re.findall("\"pk\":(\d+),",r.text)

                media_id = [pk for pk in media_id if len(pk) >= 18]
                if count > len(media_id):
                        count = len(media_id)
                return media_id[:count]


        def get_user_followers(self, user_id, count=10):    
                r = get(f'{self.pvt_api}/friendships/{user_id}/followers/?count={count}&search_surface=follow_list_page', headers=self.default_headers)
                usernames = re.findall(r"pk\":(.*?),",r.text)
                return usernames


        def get_user_follower_count(self, user_id):
                username = self.get_user_username(user_id)
                r = get(f'{self.pvt_api}/users/web_profile_info/?username={username}', headers=self.default_headers)
                if "<!DOCTYPE html>" in r.text:
                        return 0
                count = re.findall("\"count\":(.*?)}",r.text)[0]
                return int(count)


        def get_user_following(self, user_id, count=10):    
                r = get(f'{self.pvt_api}/friendships/{user_id}/following/?count={count}&search_surface=follow_list_page', headers=self.default_headers)
                usernames = re.findall(r"pk\":(.*?),",r.text)
                return usernames


        def get_user_following_count(self, user_id):
                username = self.get_user_username(user_id)
                r = get(f'{self.pvt_api}/users/web_profile_info/?username={username}', headers=self.default_headers)
                if "<!DOCTYPE html>" in r.text:
                        return 0
                count = re.findall("\"count\":(.*?)}",r.text)[1]
                return int(count)


        def follow_user(self, user_id,):
                y = post(f'{self.web_url}/friendships/{user_id}/follow/',headers=self.public_headers)
                return y.status_code


        def unfollow_user(self, user_id,):
                y = post(f'{self.web_url}/friendships/{user_id}/unfollow/',headers=self.public_headers)   
                return y.status_code


def main():
        w = InstagramAPIwrapper()
        w.login(username, password)
        print()


if __name__ == '__main__':
        main()



