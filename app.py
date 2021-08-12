import csv
from flask import Flask, render_template, request

app = Flask(__name__)
# master list of food trucks we can access everywhere else when searching and adding
# potential for a faster data structure than a list?
# a set? if we somehow end up with a duplicate its removed and set operations to retreive
#     and insert should be faster. using a set is a potential upgrade to look into
# the max size of a list should be fine for a list of food trucks in a city
#     (there should be a max to how much we need to scale)
food_truck_list = []

def load_food_trucks():
   # csv is a standard library to use but there might be a better library for loading this
   # pandas can use csv, right? is it faster? potential improvement speed improvement here.
   reader = csv.reader(open('.\static\Mobile_Food_Facility_Permit.csv', 'r'))
   # this is the header, we don't care about that when creating our dictionary so lets essentially
   #     dump the first line
   next(reader)
   for row in reader:
      # for the sake of the scope of the challenge, lets try to limit to the most relevant columns
      #     when we create a truck to add to the list
      food_truck = {
         "locationid": row[0],
         "applicant": row[1],
         "address": row[5],
         "block": row[7],
         "food": row[11],
      }
      food_truck_list.append(food_truck)

@app.route('/')
def home():
   global food_truck_list
   return render_template("index.html", pageTitle = "Home", foodTruckCount = len(food_truck_list))

# retrieve a food truck based on the locationid field
@app.route('/search/location', methods = ['GET']) # some URLs were getting HTTP 308 seeminlgy randomly, not all URLs had the issue
@app.route('/search/location/', methods = ['GET']) # so lets make sure both request mappings are covered; look into this behavior later
def get_food_truck_by_location_id():
   global food_truck_list
   locationID = ""
   result = []
   food_truck = None
   if request.method == 'GET' and request.args.get('locationID') != None: # the check for None is just a safe guard in case we manage to get a really awful URL
      locationID = request.args.get('locationID')
      result = list(filter(lambda food_truck: food_truck['locationid'] == locationID, food_truck_list))
      if len(result) > 0:
         food_truck = result[0]

   return render_template("findLocation.html", pageTitle = "Find Food Trucks By Location",
   foodTruckCount = len(food_truck_list), locationID = locationID, result_size = len(result), food_truck = food_truck)

# get all food trucks for a given block
@app.route('/search/block', methods = ['GET'])
@app.route('/search/block/', methods = ['GET'])
def get_food_truck_by_block():
   global food_truck_list
   block = ""
   result = []
   if request.method == 'GET' and request.args.get('block') != None:
      block = request.args.get('block')
      result = list(filter(lambda food_truck: food_truck['block'] == block, food_truck_list))
   return render_template("findBlock.html", pageTitle = "Find Food Trucks By Block",
   foodTruckCount = len(food_truck_list), block = block, result_size = len(result), result = result)

# add a new food truck
@app.route('/addFoodTruck', methods = ['GET', 'POST'])
@app.route('/addFoodTruck/', methods = ['GET', 'POST'])
def add_new_food_truck():
   global food_truck_list
   foodTruckAdded = False
   if request.method == 'POST':
      new_food_truck = {
         "locationid": request.form['locationID'], # should validate against this since it should be unique
         "applicant": request.form['name'],
         "address": request.form['address'],
         "block": request.form['block'],
         "food": request.form['foodType'], # we could leave this blank since some in the CSV seemed to be missing this (but block too though?)
      }
      food_truck_list.append(new_food_truck)
      foodTruckAdded = True
   return render_template('addTruck.html', pageTitle = "Add a New Food Truck",
   foodTruckCount = len(food_truck_list), foodTruckAdded = foodTruckAdded)

# need a route to handle the 404
# there should be a built-in 404 handler inside of Flask that could be used

if __name__ == '__main__':
   # no database usage? lets load these into a convenient data structure
   #     before the server boots up so we don't have interruption
   load_food_trucks()
   # harder to test with no reloading but we also wont accidentally
   # start reloading the list a second time with load_food_trucks
   app.run(debug=True, use_reloader=False)