# uCode by Adidas 2017
The hackathon took place in Zaragoza between 10-12 March, 2017

## hiberus challenge
### Smartlify
Smartlify is an android app based in the client-server paradigm that allows the user to control its own drone with our app, watching in real time the camera of the drone on the mobile screen and showing all the nearest Access Points sharing Wi-Fi using an attached Raspberry Pi on the drone

### Gadgets
To create this application, the following gadgets were used:
 - Parrot Minidrones Jett Jumping race drone
 - Raspberry Pi 3 (Model B)
 - Sony Xperia Z Android smartphone

### Goals
Main goal is to be able to connect a mobile phone, a drone and a Raspberry Pi attached to the drone into a single WiFi network to provide communication between them and allow the Raspbery Pi that is dynamically moved thanks to the drone scan access points remotely.

### Uses
The ability to scan networks remotely is useful to:
 - Audit remote networks
 - Find rogue (evil) Access Points remotely
 - Find low-level signal spots remotely

#### Future uses
The following ideas can be implemented with more time and research, but using the same or more gadgets:
 - Find low-level signal spots and let the drone move there to create a WiFi repeater nearer to the highest signal spot
 - Track users that are using your wireless networks and make a map with them
 - Automatically create a map with the access points in the floor

#### Use summary
Therefore with further work the application can be used by system administrators
to remotely secure their buildings from unauthorized wireless networks while
keeping track of their status, use and users.

### Language and dependencies
Client and server modules to communicate the Raspberry Pi attached to the drone with the mobile application are coded in Python 3.4, using the following libraries:
	- `netifaces`
	- `wifi`

### Android application
The Android app that controls the drone and displays the found wireless access points can be found here:
<center>[https://github.com/cgardev/DroneClient](https://github.com/cgardev/DroneClient)</center>

<> with ❤ by [ccebrecos](https://github.com/ccebrecos), [davidlj95](https://github.com/davidlj95), [cgardev](https://github.com/cgardev) and [persicris](https://github.com/persicris).
