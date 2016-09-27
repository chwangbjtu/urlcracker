#include "en_interface.h"
#include <iostream>
#include <string>
#include "stdlib.h"

using namespace std;

int main()
{
    int a_index = 1;
    int key_index = rand() & 0x000F; 
    unsigned int random = rand() & 0xFFFF;
    
    string source = "ab";
    string request = source;
    
    ftsps::encrypt(a_index, key_index, random, (unsigned char*)request.c_str(), request.length());
    cout << request << endl;
    
    ftsps::decrypt(a_index, key_index, random, (unsigned char*)request.c_str(), request.length());
    cout << request << endl;
    return 0;
}
