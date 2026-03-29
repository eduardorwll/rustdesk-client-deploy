import requests
import winapps

import tempfile
import os
import subprocess
import time
import secrets
import string



class RustDesk:
    def __init__(self, url, host, key, temp = tempfile.mkdtemp()):
        self.url = url
        self.host = host
        self.key = key
        self.id = None
        self.password = None
        self.temp = temp
        self.installed = False
        self.path = f"{self.temp}\\rustdesk-installer.exe"
        
    def download_installer(self):
        response = requests.get(self.url)
        
        if response.status_code == 200:
            with open(self.path, 'wb') as file:
                file.write(response.content)
            print('File downloaded successfully')
        else:
            print('Failed to download file')
            
    def check_install(self):
        installed = False
        for item in winapps.list_installed():
            if item.name == "RustDesk":
                self.installed = True
        self.path = "C:\\Program Files\\RustDesk\\rustdesk.exe"
    
    def install(self):
        ans = subprocess.call([self.path, "--silent-install"])
            
        if ans == 0:
            print("Command succeeded.")
            time.sleep(20)
            self.check_install()
            
            while(self.installed == False):
                time.sleep(10)
                self.check_install()
            
            ans = None
            ans = subprocess.call([self.path, "--install-service"])
            
            time.sleep(20)
            
            if ans == 0:
                print("Service installed.")
            else:
                print("Command failed.")
        else:
            print("Command failed.")
    
    def setup(self):
        alphabet = string.ascii_letters + string.digits

        try:
            ans = subprocess.check_output(f"{self.path} --get-id ^| more", text=True)
            self.id = ans
            
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            pass
        
        ans = subprocess.call(f'{self.path} --config "host={self.host},key={self.key}"')
        
        if ans == 0:
            print("Command succeeded.")
            self.password = ''.join(secrets.choice(alphabet) for i in range(12))
            ans = None
            ans = subprocess.call(f'{self.path} --password {self.password}')
        
            if ans == 0:
                print("Command succeeded.")
            else:
                print("Command failed.")
                pass
        else:
            print("Command failed.")
            pass
            
        print(self.id)
        print(self.password)