"""
Auth: Nate Koike
Desc: a quick and dirty installer for python packages
"""

import os

def main():
    # account for different versions of python being installed
    try:
        os.system("pip install -r requirements.txt")
    except:
        os.system("pip3 install -r requirements.txt")

if __name__ == "__main__":
    main()
