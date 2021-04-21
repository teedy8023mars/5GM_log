1. Check the IP address of your PC that is used to receive the syslog 
	- Press WIN+R, enter cmd
	- Enter ipconfig and check the IPv4 address
2. Log into the router that your is connected to (Not TeaM1 5GM)
	- Open a browser (e.g., Chrome, Edge)
	- Enter the gateway of the router (e.g., 192.168.1.1)
	- Do Port forwarding for your PC's IP address
	- Set Public (external) port (e.g., 514)
	- Set LAN (internal) port (e.g., 514)
3. Open the Log View.exe application
	- Navigate to 'Config your PC' Section
	- Enter your PC's IP address and the LAN port you set in Step2
	- Click 'Start/Stop' Button
	- If you entered wrong port, no error message will show, double check it 	and click the 'Start/Stop' Button to stop, correct your port, and click the 'Start/Stop' button again.  


Caution:
	 - Unix (macos / Linux )operating system: make sure run the program with sudo permission.