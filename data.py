import pymongo
import certifi
import os
from dotenv import load_dotenv
load_dotenv()



client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.shop
print('\x1b[6;30;42m' + '資料庫連線成功'.center(87) + '\x1b[0m')


# collection=db.product
# collection.insert_one({
#     "_id":7,
#     "name":"test",
#     "price":["100","200"],
#     "size":["normal","special"],
#     "photo":"https://i.imgur.com/Y5ZjfLh.jpg",
#     "introduction":"這是一個商品",
#     "categories":"鴨",
#     "inventory":[0,0],
#     "disable":0
# })]

# collection.insert_one({
#     "order_id":2,
#     "phone":"0958058578",
#     "email":"roryrory960526@gmail.com",
#     "address":"基隆市仁二路77號",
#     "account":"120",
#     "price":1000,
#     "password":"",
#     "delivery_status":"",
#     "pay_status":0,
#     "disable":0
# })

collection=db.admin
collection.insert_one({
    "nickname":"使用者",
    "email":"20230520",
    "password":"taiwan"
})
# collection=db.system
# collection.insert_one({
#     "name":"RWD響應式網站",
#     "start_time":"2023-05-17",
#     "expiration_date":"2033-05-17",
#     "status":1,
#     "cost":"0元/月",
# })

# print(list(collection.find({},{"order_id":1}).sort("order_id",-1))[0]["order_id"]+1)

# print(list(list(collection.find())[0].items()))
