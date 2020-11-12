#include <stdio.h>
#include <stdlib.h>

using namespace std;

int main(){
  try{
    system("pip install -r requirements.txt");
  }
  catch{
    system("pip3 install -r requirements.txt");
  }
}
