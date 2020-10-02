import subprocess

def ocr():
    print("start")
    try:
        subprocess.call("ocr.sh")
    except:
        subprocess.call("ocr.bat")        
    print("end")
