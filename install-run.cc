#include <stdio.h>
#include <stdlib.h>

using namespace std;

int main(){
	try{
		system("pip install -r requirements.txt");
		system("python ui.py");
	}
	catch(int e){
		system("pip3 install -r requirements.txt");
		system("python3 ui.py");
	}
}
