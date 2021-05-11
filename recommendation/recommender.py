import json
from collections import Counter
from sys import path

# *** Instruction for how to run:
    # 1. Change the file path for json files
    # 2. Run the python script and enter the teammateID when the program asks for the id  

  
# Define the JSON file path (I have used absolute path, Please change path before running)
ratings = open(r"C:\\Users\khan2r\My Python Stuff\ratings.json", "r")
teammates = open(r"C:\\Users\khan2r\My Python Stuff\teammates.json", "r")
restaurants = open(r"C:\\Users\khan2r\My Python Stuff\restaurants.json", "r")
  
# Reading from file
ratingData = json.loads(ratings.read())

teammatesData = json.loads(teammates.read())

restaurantsData = json.loads(restaurants.read())
  
# Method to return list item of likes and dislikes for a teammate
def findLikeDislike(teammateId, likeType):
    likes = []
    for i in ratingData:
        if i['teammateId'] == teammateId and i['rating'] == likeType:
            likes.append(i['restaurantId'])
   
    return likes

# Method to return list of teammateID by restaurant and rating type
def findTeammateIDForLikeDislike(restaurant, likeType):
    ids = []
    for i in ratingData:
        if i['restaurantId'] == restaurant and i['rating'] == likeType:
            ids.append(i['teammateId'])
    
    return ids


# Method to find the similarity index
def similarityIndex(t1, t2):
    
    #Find liked rating restaurants for a teammate 1
    lst1Like = findLikeDislike(t1, 'LIKE')

    #Find liked rating restaurants for a teammate  1
    lst1Dislike = findLikeDislike(t1, 'DISLIKE')

    #Find liked rating restaurants for a teammate 2
    lst2Like = findLikeDislike(t2, 'LIKE')
    
    #Find liked rating restaurants for a teammate 2
    lst2Dislike = findLikeDislike(t2, 'DISLIKE')

    # Find union and intersation and assign value to variables
    intersectLike = set(lst1Like).intersection(lst2Like)
    unionLike = set(lst1Like).union(lst2Like)

    intersectDislike = set(lst1Dislike).intersection(lst2Dislike)
    uniondislike = set(lst1Dislike).union(lst2Dislike)

    unionTotal = set(lst1Like).union((lst1Dislike), lst2Like, lst2Dislike)

    # Results for similarity index
    result = (len(intersectLike) + len(intersectDislike) - len(unionLike) - len(uniondislike))/len(unionTotal)
  
    return result

# Method to find the predictability index
def predictionIndex(teammate, restaurant):

    #Find liked rated restaurants for a teammate 
    liked =  findTeammateIDForLikeDislike(restaurant, "LIKE")

     #Find disliked rated restaurants for a teammate 
    disLiked =  findTeammateIDForLikeDislike(restaurant, "DISLIKE")
   

    # Calculate sum of similarity index for like and dislike and assign it to a variables and calculate prediction index
    sumSimLiked =  0 
    sumSimDisliked = 0

    for t in liked:
        sumSimLiked = sumSimLiked + similarityIndex(teammate, t)

    for t in disLiked:
        sumSimDisliked = sumSimDisliked + similarityIndex(teammate, t)

    
    result = float(sumSimLiked + sumSimDisliked)/(len(liked)+len(disLiked))
    
    
    return result

# Method to Find resturants that teammate is not visited yet in order to avoid recommendation for restaurant in which teammates already been to
def findNotVisted(teammate):
    resIds = []
    for i in ratingData:
        if i['teammateId'] != teammate:
            resIds.append(i['restaurantId'])
    
 
    return resIds

# Method to find top recommended restaurants and print the name of the restaurants
def recomRestaurant(teammate):
    recomList = {}
    notVistedRest = findNotVisted(teammate)
    dictVal = []

    for t in notVistedRest:
        # dictVal = [t, predictionIndex(teammate, t)]
        
        recomList[t] = predictionIndex(teammate, t)
    k = Counter(recomList)
  
    # Finding 3 highest values
    high = k.most_common(3) 
    
    print('*** TOP THREE RESTAURANT RECOMMENDATION***')
    counter = 0
    for i in high:
        counter += 1
        for j in restaurantsData:
            if i[0] == j['id']:
                print('Number ' + str(counter) + ': ' +j['name'])

  
  

# Take input for teammateID
teammateID = input('Please Enter a Team ID for Recomendation: ')

# Call the method for finding recommendations
recomRestaurant(teammateID)

# *** Example json data for convenience ****

# similarityIndex('a24e3439-c647-4006-832d-c4777ee1365c', '019f3e44-8f68-4552-9924-62df6de56fca')

# {'id': 'a24e3439-c647-4006-832d-c4777ee1365c', 'name': 'Brian Kuphal'}

# {'name': 'Middle Child', 'id': 'OAWa1WML2V1ZLJGD6V3nBQ', 'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/K0lt_J75z28vFD8yLBSGFA/o.jpg', 'categories': [{'alias': 'breakfast_brunch', 'title': 'Breakfast & Brunch'}, {'alias': 'sandwiches', 'title': 'Sandwiches'}, {'alias': 'coffee', 'title': 'Coffee & Tea'}], 'price': '$', 'rating': 4.5}

# {'teammateId': 'a24e3439-c647-4006-832d-c4777ee1365c', 'restaurantId': 'dChRGpit9fM_kZK5pafNyA', 'rating': 'DISLIKE'}