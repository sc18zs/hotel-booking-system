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
When the user logs in and chooses the option to remain logged in, the website uses cookies to store user information. When the user opens the website page again, the stored infor- mation is automatically logged in. This information will be deleted after the user logs out. In addition, the first page will display a cookie usage reminder to the user.

In the room reservation page, session is used to store the check-in and departure times entered by the user, so as to save the query record of each date and send the information to the order page for display. The changed time will be automatically updated when the user resubmits the query form.

In the user order query page, session is used to store the order filter information entered by the user, so as to ensure that the query condition can be saved when the page is turned.

### Authentication
When the user enters the login information, the user record will be matched in the data, and if the information is correct, it will redirect to the hotel page. When you select the option to remain logged in at logon time, the site will use cookie user information to automatically log in the next time the user opens a web page. The website will remind you to use cookies on the front page. Users can log out by clicking the logout link at the top right. Flash reminds the user of their current status when they log in and log out successfully. The site allows users to change their passwords. The site provides a form for users to enter their account information and a new password, and flash alerts when the password is incorrectly formatted or the account information is incorrect.

### Styling

The web page follows a responsive design to ensure a good user experience on different devices.

### Logging
This project outputs the logs in a set format (stored in flask.log) and grades the logs in four type: debug, info, error, critical.

## Other features
### Bootstrap and jQuery
This project uses JQuery date picker plug-in colored by Bootstrap to help the user enter a date in the form, locate the date picker to the date of the day, and help the user select a reasonable time period.

### Geolocation
The site has set up an interface to call Api interface to display the location of the hotel.

### Administration
This website also provide an entrance to the background stage for administrator.

### Send email
Every time when user finished booking, a confirm email will be received from admin.

## Analysis and evaluation
The website test results on main web browsers are as follows: As shown here, the style and some features can be implemented successfully in these web browsers. The following is a detailed assessment of each function:

1. Web forms: the designed forms can successfully allowed user to input data and post data into server side to do operations. It can give warnings for wrong input format and also receive flash information from server side and display to users which is much more convenient for individual to check webpage status. However, this website need to collect some identity information, like ID number, which may be hard to validate except only by checking data format.

2. Database: the database is designed including a many to many relationship, which needs a relation table to connect. The hotel list page and room list page is displayed by read records information from hotels and rooms table. This design is good for admin to add new hotels information in this booking system by insert records into database instead of change templates.

Users can fill in the search bar according to their needs, and the background will filter the matching information in the database and send the information to the client for dis- play. This is good for users experience when searching matched hotels or orders intelligently.
This limitation is that some information stored in this database may not be used be- cause of shortage design.

3. Sessions and cookies: sessions and cookies are used for store some information about user actions so that it can have better interaction with client server. Also, this website show a cookie usage agreement for users to let them know the website status.
  
4. Authentication: this website restrict the logins of non-authenticated users by matching login information based on user records in the database. In addition, some web pages are only displayed to authenticated users, such as personal account page and administrator background, which can only be accessed by corresponding user roles, enhancing the secu- rity of the website.
   
5. Deployment: test results after website deployment is shown here: Some functions like geolocation and sending email can not be correctly implemented due to the restrict access to the external network by pythonanywhere.

## Security
In order to enhance the security of the website, the system is set to store the user’s pass- word and ID number encrypted into the database by using hash code, in case the user’s personal new information is leaked and causing losses.

The security of cookies stored by websites is relatively low, so the data stored by the system using cookies does not include important information such as user password.












