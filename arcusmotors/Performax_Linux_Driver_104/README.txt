********************
*** Requirements ***
********************

libusb 1.0

************************************
** Installing Necessary Libraries **
************************************

Make sure that you have internet access since it is necessary to install the
[libusb-dev] library.

These instructions are for use with Ubuntu, and were created using Ubuntu 9.04:

1) Open command line
2) Execute: "sudo apt-get install libusb-1.0-0-dev"
3) Execute: "sudo apt-get install build-essential"

************************************
*** Compiling the static version ***
************************************

1) Download the "Performax_Linux_Driver_104" to your computer 
2) Open the command line
3) Navigate to the "Performax_Linux_Driver_104" directory
4) Execute: "gcc -o test test.c ArcusPerformaxDriver.c -lusb-1.0"
   (Optionally add "-DDEBUGARCUS" to the above commandline if you want more verbose text output)

************************************
**** Running the sample program ****
************************************	

1) Open the command line
2) Navigate to the "Performax_Linux_Driver_104" directory
3) Execute: "sudo ./test"

************************************
***** Creating your own program ****
************************************	

1) Modify the "test.c" to customize your application.
	

