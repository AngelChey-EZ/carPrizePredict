# CA1-DAAA2B02-2214634-AngelCheyEeZia


Dataset Source:https://www.kaggle.com/datasets/shubham1kumar/usedcar-data?select=UserCarData.csv

### Context
This is an application develope for users in USA to predict thier used car's price so that they would know what is a suitable range to sell thier car. 

The application is developed by a car resale company in USA, aiming to analyze used car market in USA. 


### What affects used car's price?
- <b>mileage</b>
- <b>condition</b> 
- Ownership Frequency
- Age of the Car
- Whether the model is in high demand or not
- Accident history
- Transmission Type
    -Though manual transmissions (stick shifts) have historically been slightly more fuel-efficient than automatic transmissions, they’re usually detrimental to resale value. That’s because most drivers don’t know how to drive stick, have mobility issues that make shifting painful or difficult, or simply don’t like keeping their right hands and left feet in constant motion in stop-and-go traffic.   
- options
- location
- color

### Data Transformation for Prediction
1. ordinal encode owner
2. one hot encode brand and fuel
3. scale numeric data
4. predict

### Key Features
1. Login
2. Sign up
3. predict car resale price with following parameters:
    - year of purchase
    - engine displacement (cc/L)
    - max power (hp/kw)
    - toque (nm/kgm)
    - car brand
    - fuel
    - owner type
4. some prediction parameters have 2 units to choose from 
5. get all users' (by user id, user need to login to access this function) prediction records
6. get latest top 5 prediction from database
7. filter/search frunction on getting latest top 5 prediction from database

### Deployment
url: https://carpricepredict-aohu.onrender.com/
