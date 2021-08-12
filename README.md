# Commercial Software Engineering Take home Challenge

A (relatively) quick attempt to approach the Microsoft CSE team take home challenge that asks for a REST service built around food truck data. Heavily commented to show my thought process while working on the challenge.

Focus was placed on the design and creation of the backend of the app which had a few design changes (change in routing structure, brief attempts at different data structure set up and nested data structures, decisions how to return the data). Front end is mostly based on setup from previous projects and made to be serviceable rather than full production quality for end users.

# Addressing Technical Requirements

## Interface

The requirements state that someone ***can*** return a set of food trucks and the team is fluent in JSON. Since the wording gave a sensse of flexibility, I decided the interface was going to be forms and tables on a few different HTML pages.

## Expected Data Size

The main data structure used here is a list in Python. The maximum amount of items that a list can hold should be able to handle millions and millions of records. The app was designed to load all the data from the CSV before the server even starts so the CSV will be processed into a data structure before the user can interact or disturb it.

## Data Stroage

A language native data structure, List in this case, was chosen as the in-memory data store.

## Service Requirements

The endpoints provided in the app will allow the possibility for a user to:
- Add a new food truck
- Retrieve a food truck based on the locationid field
- Get all food trucks for a given block

# Possible Areas of Improvement

- Look into using a different/faster data structure to hold the list of food trucks (maybe multiple data structures to partition data or one where operations just tend to move faster)
- Programmatically create JSON object that can be returned with some list data instead of populating a table
- Enhanced UI (forms, navigation bar, layout)
- Consider a different Python library for reading the CSV file
- Try to use Swagger for 
- Find a better fix for the routing and HTTP 308 message
- Check if there are viable ways to filter results of the list faster
- Add validation checks for when a food truck is added