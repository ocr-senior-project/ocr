#include <stdio.h>
#include <stdlib.h>

using namespace std;

int main(){
  try{
    system("pip install numpy");
    system("pip install pillow");
    system("pip install opencv-python");
    system("pip install tensorflow");
    system("pip install pyqt5");
  }
  catch(int e){
    system("pip3 install numpy");
    system("pip3 install pillow");
    system("pip3 install opencv-python");
    system("pip3 install tensorflow");
    system("pip3 install pyqt5");  }
}
