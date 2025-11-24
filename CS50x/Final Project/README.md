# Current exchange market environmental recognition system with MetaTrader
#### Video Demo:  <https://youtu.be/pusQPCdEvLs>
#### Description:

# ABOUT
This is the system called Current exchange market environmental recognition system that notifies me daily rate of major currencies by chat app discord (or LINE). Appellative name of the project is "Watchdog" as it watch the market 24/7.

# PREREQUISITE
Due to high volatile of rates of currencies recent years as we can see especially in weak Japanese yen that sometimes makes the country be called "bargain" by other nations, it's important for us to understand the environment of those market for some sorts of emergencies in the future. And that is one of the reason I built the system as a whole.

# FUNCTIONS
First, this system assumes to run on windows server because it needs to keep running so that the system can watch the market 24 hours 6 days a week. (not exactly 24/7, because current market is open except sunday.)
So if you need to design that the system to reboot for maintenance purpose, for example, it will be designed to do so on the day.
(which I don't design in the function this time because it should be controlled by OS, using Group Policy Object and so forth.)
And the information collected by the main function in the file called "Daily notification test" will be uploaded to Discord API server.
So it also requires notification function that denotes API key and functions according to its objectives.(e.g. text, image and so forth.)
This function is in the file called "Notification_dev".

In addition, in the files called "upload_image_file_*", I use windows command line prompt to supplement the function that can not be realized with functions in meta trader. (e.g. curl command to send a http request/response header to API server)

Second, the content of the information the system collect is basically daily currency volatile, highest or lowest rates, and shoot related screenshots. This is the main function as programed in "Daily notification test".

Finally, I designed the function called "converToJpTime" that is literally convert server time zone into Japanese time. (for better notification purpose.)

# DEMONSTRATION
Usually, the trading server can always watch the rate of currency I set in the system, for example, if I set USDJPY signals at every 6AM in my program, it automatically collect the information at the time.
For demonstration purpose, however, I will use the tester of the system to see if it works properly.
In this time, I will collect the daily rate information of USDollar and Japanese yen pair.

You can see on my discord chat in the demonstration video that I receive the information once I run the program.
(-1.32yen volatile, rate, time, and the screenshot image at the time.)

This always can help me understand whenever sudden changing of the rate would happen, on what time, how and so forth.
And of course you can custom as you like if you want to change current pair, or ordering, selling function and so forth, for example, I added the strong movement judgement function in "Daily notification test" to see if strong volatile of rates(over +-0.2yen movements) has occurred that enables me design what the next action is if that were happened.(e.g. notification, selling all of positions and so forth)
And that is definitely solve my actual problem.
