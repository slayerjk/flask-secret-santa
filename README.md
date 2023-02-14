<h1>Secret Santa Project</h1>

<h2>Description</h2>

This is the Secret Santa Project. The purpose is to allow users(from LDAP auth and LDAP group members) to add own wishlist and get random wishlist to execute.

For LDAP auth I've used this page: https://code.tutsplus.com/tutorials/flask-authentication-with-ldap--cms-23101

<h2>Directory Structure</h2>

Project files and folders:
* run.py - running script
* myapp/ - dir of application files
  * myapp/static/css
    * bootstrap.min.css
    * bootstrap.min.css.map
    * main.css - custom css
  * myapp/static/js
    * bootstrap.min.js
    * bootstrap.min.js.map
    * jquery-3.6.3.min.js
  * myapp/templates/
    * admin.html - template for admin page with all users and their wishlists, form to assign wishlist, clear table with assigned wishlists
    * base.html - base template for other templates
    * cabinet.html - cabinet page for loged in user with his/her wishlist and assigned wishlist to execute
    * index.html - home page
    * login.html - page with login form
  * myapp/app.py - main flask application script
  * myapp/forms.py - flask forms
  * myapp/models.py - flask models
  * myapp/routes.py - flask routes
  * myapp/ldap-data - your LDAP data and creds to bind

<h2>Requirements</h2>

* flask
* flask_login
* flask_sqlalchemy
* flask_wtf
* wtforms
* ldap3

<h2>sec-san.db</h2>

Tables:
* users: id, username, is_admin
* wishlist: id, wishlist, user_id(FK users.id)
* lottery: id, user_id(user.id), assigned_wishlist(wishlist.id)

<h2>Workflow</h2>

Application runs by default http://127.0.0.1:5000

<h3>Admins</h3>
myapp/app.py contain admins list that contains all admins that are not participants of 'Secret Santa' lottery. They are lowercase of ldap user accounts. The admins have no cabinet page, only admin page for running/cleaning lottery.

<h3>Searching Users</h3>
The app only allow user of <YOUR DOMAIN GROUP NAME CONTAINS ALL YOUR USERS> group. So by first login app search for that group in domain and get CN of every user and save them in list.

<h3>Logging in</h3>
With first login attempt on login page, app checks:

if user is in admins list create admin user(is_admin='Y')
if user is in domain user list, but not admin - create user(is_admin='N')
all other users not allowed
Then trying to bind to ldap using provided username and password.

<h3>Cabinet page</h3>
In cabinet page user allowed:

to create/update his/her wishlist
if assigned - user see assigned wishlist

<h3>Admin page</h3>
Admins see all of the users and their wishlist.

If there is a quourum(even number of users) admin can run 'lottery' - assign random wishlist to all listed users.

If there is a 'lottery' table - it's possible to see it and clear it, to run 'lottery' again then.
