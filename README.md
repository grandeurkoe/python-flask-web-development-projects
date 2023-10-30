# Python Flask Web Development Projects

These python Flask web development projects are built in correspondence with " [100 Days of Code - The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) " course. This course was taught by London's App Brewery top instructor Angela Yang.<br/>

Each project has been built from scratch with minimal to no assistance.<br/>

### Day 054 - Python Decorator

This project involves constructing your own custom python decorator. 

Here, we created a delay constructor that prints "How are you?" after a 2 second delay.

For a live version, go [here](https://replit.com/@grandeurkoe/python-decorators?v=1) .

![Python Decorator](python-decorators/python-decorators.gif)

### Day 055 - Higher or Lower URLs

This project simulates a Higher or Lower URLs website using the Flask framework. Generate a random integer using the randint() function from the random module. This random integer is the number that the player has to guess.

Website Navigation:
- The Higher or Lower URLs website is running on a development server that Flask ships with.
- Use the "/" route to navigate to the homepage.
- Use the "/guessed_number" route to play the  Higher or Lower URLs game. Get the guessed_number as user input.
- If the guessed_number is less than the correct number, then display a webpage with "Too low, try again!" red heading and a funny GIF.
- If the guessed_number is greater than the correct number, then display a webpage with "Too high, try again!" purple heading and a funny GIF.
- If the guessed_number is correct, then display a webpage with "You found me!" green heading and a funny GIF.

![Higher or Lower URLs](higher-or-lower-urls/higher-or-lower-urls.gif)

### Day 056 - Name Card

This project simulates a Name Card website using the Flask framework. Use [Aerial](https://html5up.net/aerial) template from [HTML5 UP](https://html5up.net/) website.

Website Navigation:
- The Name Card website is running on a development server that Flask ships with.
- Use the "/" route to navigate to the name card webpage.

For a live version, go [here](https://replit.com/@grandeurkoe/name-card?v=1) .

![Higher or Lower URLs](name-card/name-card.gif)

### Day 057 - Blog (v1)

This project simulates a Blog website using the Flask framework.

Website Navigation:
- The Blog website is running on a development server that Flask ships with.
- Use the "/blog" route to navigate to the blog webpage.
- Each post on the blog webpage has a "Read" link.
- Click on "Read" link to navigate to that post's webpage.
- Use the "/post/post_id" route to navigate to each post based on post_id (integer).

![Blog (v1)](blog/blog.gif)

### Day 059 - Blog (v2)

This project simulates a Blog website using the Flask framework. Use the requests module to get post data from the [npoint](https://api.npoint.io/eb6cd8a5d783f501ee7d) API. Store the newly acquired JSON response.

Website Navigation:
- The Blog website is running on a development server that Flask ships with.
- Use the "/" route to navigate to the blog homepage.
- Each post on the homepage is a link.
- Click on post link to navigate to that post's webpage.
- Click on "ABOUT" link to navigate to the about webpage.
- Click on "CONTACT" link to navigate to the contact webpage.
- Use the "/post/post_id" route to navigate to each post based on post_id (integer).
- Use the "/" route to navigate to the blog homepage.
- Use the "/about" route to navigate to the about webpage.
- Use the "/contact" route to navigate to the contact webpage.

For a live version, go [here](https://replit.com/@grandeurkoe/better-blog?v=1) .

![Blog (v2)](better-blog/better-blog.gif)

### Day 060 - Blog (v3)

This project is a upgraded version of [Blog (v2)](#day-059---blog-v2) with a functional contact form. 

For a live version, go [here](https://replit.com/@grandeurkoe/better-blog-with-contact?v=1) .

![Blog (v3)](better-blog-with-contact/better-blog-with-contact.gif)
