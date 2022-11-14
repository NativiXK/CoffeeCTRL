# **Coffee control WEB application**

#### **Video DEMO:** (https://www.youtube.com/watch?v=r3ZmIhr_xcg)

#### **Description**: :smiley::rocket:

For CS50 final project I created a Web application using the following tools:

| Tool | Used for |
|:---|---| 
| **Python** | Backend application and API |
| Flask | Web Framework for python |
| Html + css | Web pages structure |
| Bootstrap | Web pages framework |
| Javascript | End-point application  
| SQL (sqlite) | Data persistence

The core ideia is for each coffee admin with its credentials have access to its own coffee group and control purchases, payments, entrance and exit of contributors, its aim is pretty much to give to the person in charge of the group a reliable way to control the cash flow in the group.

When loading the application, a simple landing page will displayed, it has in the center a search bar to look for coffee group names ("Yeahh you can look for coffee groups hahaha").

If you are a coffee group admin, you can loggin into your group control page with your credentials, and there you'll have access to do whatever you want.

The coffee contributors are displayed in a table that shows their payments or the lack of it, by clicking on each user row, it is possible to add a new payment, to edit all payments made by the person, to edit the contact and also remove the person from the group.

In middle of the screen, there are four fields displayed as follow:

- Monthly price;
- Income;
- Spent;
- Total.

This field aims to give a general overview of the cash flow in the group, in the first one, you can see the monthly price charged to contribute with the coffee and by clicking on the button "Edit", a modal will be displayed and inside of it you can modify or visualize the group info, such as **group name, admin username, admin email, monthly price value and see the amount of contributors**.

The second field shows the income of cash, its pretty simple and there is not so much to talk about it, but below the value field there is a month selector, and when selecting any value on it a income report modal will be displayed with payments received in the month selected or in the whole year if yearly report selected.

likewise the income cash field, the spent cash field has the same behaviour, though it shows outgoing cash and it also shows a report modal when selecting the desired month or a yearly report.

## Structure:

### db.py:
In db.py file occurs almost every database query, except some cases in which it was necessary to make subqueries in code flow to build a modal or a page.

### api.py:
This file is responsible for handling every API request in the application, pretty much of the requests are made by the endpoint Javascript to ask for report modals or trigger some application behaviour.

### templates folder:
Inside this folder are all the templates used in the application and rendered by jinja which Flask uses to build the html page.

### views folder
The views folder contains all blueprints files with the application routes and there is also a modal renderer, which is responsible to return rendered html strings as requested.