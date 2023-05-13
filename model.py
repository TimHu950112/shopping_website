from crypt import methods
from imp import reload
from dotenv import load_dotenv
from send_email import send_email
from datetime import date,datetime
import pymongo,certifi,os,random,string,pytz

load_dotenv()
client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.shop

class Test:
    def _init_(self):
        pass

class Product:
    def __init__(self,id,name,price,size,photo,introduction,categories,inventory,disable):
        self.id=id
        self.name=name
        self.price=price
        self.size=size
        self.photo=photo
        self.introduction=introduction
        self.categories=categories
        self.inventory=inventory
        self.disable=disable
    def get_inform(text,id):
        collection=db.product
        result=collection.find_one({"_id":int(id)})
        for i in range(0,len(result["size"])):
            if result["size"][i] == text:
                break
        return (result,i)
    def get_photo(id):
        collection=db.product
        return collection.find_one({"_id":int(id)})["photo"]
        
    def update():
        pass
    def delete():
        pass

class Order:
    def update(phone,email,address,account,price,shopping_list,delivery_fee):
        collection=db.order
        # order_id=list(collection.find({},{"order_id":1}).sort("order_id",-1))[0]["order_id"]+1
        order_id=0
        letters = string.ascii_uppercase + string.digits
        password= ''.join(random.choice(letters) for i in range(5))
        date=datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d').split("-")
        collection.insert_one({
            "order_id":order_id,
            "phone":phone,
            "email":email,
            "address":address,
            "account":account,
            "price":int(price),
            "date":date,
            "password":password,
            "shopping_list":shopping_list,
            "delivery_status":"準備中",
            "pay_status":0,
            "disable":0
        })
        send_email(email,password,order_id,shopping_list,price,delivery_fee)

    def search(order_id,password):
        collection=db.order
        result=list(collection.find({
            "$and":[
                {"order_id":int(order_id)},
                {"password":password}
            ]
        }))[0]
        return result
        

