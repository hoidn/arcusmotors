#include <stdio.h>
#include <string.h>
#include "ArcusPerformaxDriver.h"

int main(void)
{
	char 		lpDeviceString[PERFORMAX_MAX_DEVICE_STRLEN];
	AR_HANDLE	Handle; //usb handle
	char		out[64];
	char		in[64];
	AR_DWORD	num;
	int i;
	
	memset(out,0,64);
	memset(in,0,64);

	//acquire information
	
	if(!fnPerformaxComGetNumDevices(&num))
	{
		printf("error in fnPerformaxComGetNumDevices\n");
		return 1;
	}
	if(num<1)
	{
		printf( "No motor found\n");
		return 1;
	}

	if( !fnPerformaxComGetProductString(0, lpDeviceString, PERFORMAX_RETURN_SERIAL_NUMBER) ||
		!fnPerformaxComGetProductString(0, lpDeviceString, PERFORMAX_RETURN_DESCRIPTION) )
	{
		printf("error acquiring product string\n");
		return 1;
	}
	
	//printf("device description: %s\n", lpDeviceString);
	
	//setup the connection
	
	if(!fnPerformaxComOpen(0,&Handle))
	{
		printf( "Error opening device\n");
		return 1;
	}
	
	if(!fnPerformaxComSetTimeouts(5000,5000))
	{
		printf("Error setting timeouts\n");
		return 1;
	}
	if(!fnPerformaxComFlush(Handle))
	{
		printf("Error flushing the coms\n");
		return 1;
	}
	
	// setup the device
	
	strcpy(out, "LSPD=3000"); //set low speed
	if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
	{
		printf("Could not send\n");
		return 1;
	}
	strcpy(out, "HSPD=3000000"); //set high speed
	if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
	{
		printf("Could not send\n");
		return 1;
	}
/* This seems to be an unknown command in the current firmware...	
	strcpy(out, "CUR=500"); //set current
	if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
	{
		printf("Could not send\n");
		return 1;
	}
*/
	
	strcpy(out, "POL=16"); //set polarity on the limit switch to be positive
	if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
	{
		printf("Could not send\n");
		return 1;
	}

	strcpy(out, "ACC=300"); //set acceleration
	if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
	{
		printf("Could not send\n");
		return 1;
	}
	
	strcpy(out, "EO=1"); //enable device
	if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
	{
		printf("Could not send\n");
		return 1;
	}
/* Incremental mode no longer appears to be supported...
	strcpy(out, "INC"); //set incremental mode
	if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
	{
		printf("Could not send\n");
		return 1;
	}
*/
	
	strcpy(out, "ID"); //read current
	if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
	{
		printf("Could not send\n");
		return 1;
	}
	
	printf("Arcus Product: %s\n",in);

	strcpy(out, "DN"); //read current
	if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
	{
		printf("Could not send\n");
		return 1;
	}
	
	printf("Device Number: %s\n",in);

	printf("Motor is moving. Please wait.\n");
	
	for (i=0; i<5; i++)
	{
		do
		{
			strcpy(out, "X-320000"); //move the motor
			if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
			{
				printf("Could not send\n");
				return 1;
			}
			
			sleep(1);
		} while(in[0]!='O'); //motor is still moving. wait and retry;
		
		do
		{
			strcpy(out, "X320000"); //move the motor
			if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
			{
				printf("Could not send\n");
				return 1;
			}
			
			sleep(1);
		}while(in[0]!='O'); //motor is still moving. wait and retry;
	
	}
	
	if(!fnPerformaxComClose(Handle))
	{
		printf( "Error Closing\n");
		return 1;
	}
	
	printf("Motor connection has been closed\n");
}
