# Hotel Booking System

website link: http://zihanshe.pythonanywhere.com/

User account

username:lynn & password:12345678

Admin account

username:admin & password:11111111

## The purpose of this website
This website is designed as a hotel booking system which can support user registration, login and log out, room match and booking, order search and system background man- agement. The administrator can publish and manage the hotel and room information on this website. After the user logs in, the website will filter the hotel information and room information according to the information entered by the user to match the most suitable reservation scheme.

## A list of features implemented
### Web forms
This website generally use form to collect user information.

For user registration, the web page provide a form to collect personal information in- cluding account name, password, validation for the password, email address and phone number. After user finish the form, the client server first checks the data to confirm user information can be successfully added into the database. Options for checking include:

• Username: username is unique which means it can not be the same as other user’s nickname.

• Password: password is set at least 8 characters long and the confirm password must match the first input.

• Email: user must input a valid email address.

• Phone Number: user must input a valid phone number which is 11 characters long.

For login form, after the user input username and password and click the login button, it will post data to the server side and match user records in the database. If match result is not None, it will jump to the hotel page, otherwise it will flash warning information on the homepage. Moreover, the website provides a single choose box for users who tend to keep logged in this website.

Same conditions described above applies to form submissions that change passwords and user personal information. For the search form, for example in the hotel list page, when the user clicks the search button without entering any filter information, the client verifies that the form information is empty and gives a pop-up warning to fill in the check-in time.

### Database

![image](https://github.com/sc18zs/hotel-booking-system/blob/main/IMG/database.png)
### Sessions or cookies














