# PizzaProject
**Building**

To Build and Run the application locally follow the Flask Official documentation to get setup, 

\- Note please name the project “PizzaProject” when creating it here:[ https://flask.palletsprojects.com/en/stable/installation/](https://flask.palletsprojects.com/en/stable/installation/)

After installation, you can move the contents of the GitHub folder titled “PizzaProject” inside your local creation, use the releases link on GitHub to download a zip version of the file that maintains the organization of the folder which can be found here:[ https://github.com/AaronSant1ago/PizzaProject](https://github.com/AaronSant1ago/PizzaProject)

**Running**

Once the files are moved over you can activate the environment again by running 

“.venv\Scripts\activate” for windows machines. Then in the activated environment you run 

“flask --app pizzaProject run” to get the application running. 

A testing environment should open up with an IP address to access the site locally.

**Testing**

To run the tests you must be in the PizzaProject folder then using pytest you run:\
“pytest test\_app.py”\
\
This will automatically run 7 tests that test the application and if it's setup/running properly. 

**Brief Overview**

For this project I used Flask as a framework because I had some experience with the project in the past and I think it was ideal for this project because of its requirements.\
\
Flask also has a lot of support for tools like Bootstrap and SQlite, so I used both of those for some basic formatting on the site and for my database.\
\
I have some experience with Sql from my previous classes, so SQlite felt like the ideal choice.\
\
For the project itself, I split it into two parts based on the stories provided. The manager page and chef page are separate with a home page bridging them on the site, and the code for both of them are in the pizzaProject.py file for simplicity. The manager code comes first, then the chef code is at the bottom of the page. I created two tables to keep the code from getting too complicated, one to manage the toppings and another to manage the pizzas.\
\
Javascript was used on the manager page to make the update toppings option only available with some topping selected. 

For testing, I tested that the site functioned as expected with user traversal to the different pages. I also tested for sql injections, since I wanted to maintain the integrity of my database and test my input validation. I also tested my database creator, which adds default toppings and pizzas into the database if it's empty. 

Overall, this project was a lot of fun and I look forward to hearing the team’s feedback. 
