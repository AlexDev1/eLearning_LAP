

#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <winsock2.h>
#include <string.h> // need for memcpy() and strcpy()
#include <windows.h> // need  for all Windows stuff
#pragma comment(lib,"ws2_32.lib")

int main(int argc, char* argv[]){
	WORD wVersionRequested = MAKEWORD(2,2); // stuff for WSA functions
	WSADATA wsaData;
	
	struct hostent *host; // structure for gethostbyname()
	struct in_addr address; // structure for Internet address
	char host_name[256]; //String for host name
	
	if(argc != 2 ){
		printf("***ERROR - incorrect number  of command line argumant \n");
		printf("   usage  is 'getaddr host_name\n'");
		exit(1);
	}
	
	 // Initialize Winsock
	 WSAStartup(wVersionRequested,&wsaData);

	
	//Copy host name into host_name
	strcpy(host_name, argv[1]);
	
	// Do a gethostbyname()
	printf("Looking for IP address for %s\n", host_name);
	host = gethostbyname(host_name);
	
	// Output address  if host found
	
	if(host == NULL){
		printf("IP address for %s could be not found", host_name);
	}
	else{
		memcpy(&address, host->h_addr,4);
		printf("IP address for %s is: %s\n", host_name, inet_ntoa(address));
		
	}

	 // clean up winsock
	 WSACleanup();

	
	system("PAUSE");
	return 0;
	
}
