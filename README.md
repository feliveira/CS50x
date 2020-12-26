# :money_with_wings: C T R L - CS50x Final Project
A web application created to make finance management easier.  
Built with HTML, CSS, JavaScript, Bootstrap, Python, Flask and SQL.

## How it works

When you enter in the website for the first time, you will see the index page of the application which you can do two things **Sign Up** or **Login**, and each option will redirect the user to it own route, where it have all of the means needed to fulfill its purpose, may it be register route where the user can be registered in the system (needing to type an email, username and password) or may it be the login route (where the user can login on their own account with their email and password).  
After registering and loging in, the user will reach the main part of the application which we will explain how it works right now. Basically, CTRL is divided in four routes, being them: 

### Dashboard

It is essentially the main page of the application, it has 6 boxes, each one for a specific category (balance, food, savings, bills, shopping and other) every one of them will open an exclusive modal when clicked, showing to the user statistics about the category they clicked, indicating how much and in which way they are spending their money on it.

### Income

It is the route where the user can add their income, they can change the value too, to solve mistakes or just change the value to a more specific one without needing to calculate the difference, the route also has a box that shows to the user how much they have in balance and below that there is a button that opens a modal with a table with the history of all changes in the income value.

### Expenses

As the name says, it is where the user can register or delete all of their expenses, when the user add an expense they can define in which category the expense fits, then organizing and dividing each one in their properly place. Below the input field there is a button like the one that the user can find in the income page, but now it shows the history of the user expenses.  
In the same page the user can add, change value, and remove an saving, giving a title for every one of them, being then in much more control of how they spend their money, below the input field there is also a button that shows the history of savings.

### Settings

The last but not the least, the settings page is where the user can change their password and/or the currency symbol that will show next to the treated values.

And in every one of the routes there is a button in the upper right corner called **Logout** that will logout the user when clicked, redirecting them back to the index page.

## Requirements

To make the project fully functional you will need to have installed all of the dependencies that it needs, to do so you will need to type the following command in the terminal of your IDE

```
pip install 
```
Before pressing enter, type one of the dependencies name and then press enter to download it, repeat it until you have all of them, the dependencies are:

```
py3-validate-email  
flask  
flask_session  
werkzeug  

```
The last one is a little different, you will need to download it from its own website

[sqlite3](https://www.sqlite.org/download.html)

after installing everything, just type **flask run** in the terminal and you will be ready to go! :smile:


## Authors
* [abhilash-katuru](https://github.com/abhilash-katuru)

* [feliveira](https://github.com/feliveira)

* [PosaLusa24](https://github.com/PosaLusa24)


### **This was CS50x.**
