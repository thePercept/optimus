# BizzinnoStrategist Ad-Platform

This is a part of a project made for an advertisement platform created by Bizzinnostrategist (A company in Gurgaon, India) 
![alt text](https://github.com/thePercept/optimus/blob/master/cropped-logo.png "BizzinnoStrategist")


The platform has 3 components in total:

1. Optimus
2. Merchant Portal
3. Cablet

## Optimus

It's aimed to be used as an admin system where core business operations can take place like Merchant Registration, Payements, Resource management, Verification, Q/A and Publishing of deals. 


## Merchant Portal
A business owner (a.k.a Merchant) can use this portal to sell their inventory 

After the merchants and their details are added , by signing up the merchnats via a business contract on paper/legal docs, their accounts are created on Optimus. A system generated email, carrying login credentials for the Merchant Portal, is sent to the registered email id of the merchant. 

Now a merchant can upload their inventory(Pictures,Logo, Title, OLd Price, New Price, Content, Menu Item ) and start making deals (currently a % discount on their total selling price is supported and can be modified as per needs ). The merchant should publish the created deals so that it can go through Q/A on Optimus. After the backend team approves ( just a click after seeing the details ) the deal, the deal is now visible on CABLET (Android devices that were aimed to be installed in Taxis).

Using this portal, the Merchant recieves a ticket whenever anyone grabs (getting the deal on phone, by entering the phone no. , via SMS) a deal on CABLET. The person carrying the Deal Voucher can present it to the respective shop/restaurant/store and avail the respective discount.

Payements are done when you reach the shop and want to use the voucher in CASH (currently this is only supported but should be via digital medium so that the business owner gets a % of the sale)

Revenue can also be made by selling plans for advertisement to the Merchant. You can decide it upfront during Merchant Sign-Ups

## Cablet


Pre-requisites for this concept are :

+ You have some Video Content (It will be shown to the commuters) licensed for your company
+ You to have to have a commercial SIM/Internet availability,inside the cabs, for data usage
+ You are in a deal with a fleet of cabs/vehicles where you can place the Android devices (You can think of putting these devices at any place according to your business needs)

+ The Android app is made for Marshmallow version. You can customize it according to your needs


CAB-LET . It's an advertisement platform placed inside a cab where commuters can watch quality content and also play various cab to cab games (like one move chess with another passenger in another cab).

It was supposed to have some variety for content like :

1. Shortfilms (~ 10 mins)
2. Music Videos (~ 5-7 mins)
3. Short News
4. Chit Chat
5. Comedy Videso
6. Animal Videos
7. Explore your city


The main concept of CABLET is that a commuter gets to watch variety of content and during his time in the cab , he also gets to see deals from sourrounding location and destination . 

## Working of CABLET

Commuter sits in the car and the ride has been started and so the device too.(Currently the startung point is done via a watch now button which has to be replaced with a face detection feature.)  Now the device will start playing content. The content being played can be changed from the Hamburger Menu.

There's a banner ad in the bottom which covers apprx. < 25 % of the screen where the nearby Merchant's deals are *being loaded* .
A pre-roll and post roll ads are being played after every 10 minutes without interfering the current video played. The system decides to play the video in a optimal and user friendly manner.
The deals are loaded in slots . Means that the business owner can decide how much deals and Video-ads in total has to be shown throughout the day as per the plan purchased by the Merchant.


## Notes

1. This repo contains Optimus and Merchant portal in a single Django Project and is exposing apis for the client. (Android- Cablet)

2. The above mentioned details explains the ideal condition when the project is 100% complete . Right now ceratin features are remaining like Slot-Wise allotment of Ads to be shown and Face Detection in cablet.

3. Feel free to use this and develop it further for your needs.
 
 







