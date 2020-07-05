### FarmerMarket Checkout System
##### The application is a web based solution opened at http://<IP>:5000/

### Use application Using Dockerfile
##### cd FarmerMarket
##### docker docker build . -t farmer_image
##### docker run  --net=host  -p 5000:5000 --name farmer_image_container farmer_image

### Steps to start the application using code base:
##### git clone codebase
##### cd FarmerMarket/FarmerMarket
##### python3 checkout.py

### Note
##### The items in grocery store along with prices can be added in json file in the code and UI will display automatically them.

