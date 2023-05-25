from dotenv import load_dotenv
from send_email import send_email
from datetime import date,datetime
import pymongo,certifi,os,random,string,pytz,requests

load_dotenv()
client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.shop

class System:
    def check_function():
        collection=db.system
        result=list(collection.find({}).sort("status",-1))
        return result

class Admin:
    def login(email,password):
        collection=db.admin
        result=collection.find_one({
            "$and":[
                {"email":email},
                {"password":password}
            ]
        })
        # print("result",result)
        if result==None:
            return False
        return result["nickname"]
    
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
        result=collection.find_one({"$and":[{"_id":int(id)},{"disable":0}]})
        if result==None:
            return None
        for i in range(0,len(result["size"])):
            if result["size"][i] == text:
                break
        # print(result,i)
        return (result,i)
    def get_photo(id):
        collection=db.product
        return collection.find_one({"_id":int(id)})["photo"]
        
    def update(id,name,price,size,photo,introduction,categories,inventory):
        collection=db.product
        collection.insert_one({
            "_id":int(id),
            "name":name,
            "price":price.split(" "),
            "size":size.split(" "),
            "photo":photo,
            "introduction":introduction,
            "categories":categories,
            "inventory":inventory.split(" "),
            "disable":0
        })
    def delete(id):
        collection=db.product
        collection.update_one({
        "_id":int(id)},
        {"$set":{"disable":1}})



class Order:
    def update(phone,email,address,account,price,shopping_list,delivery_fee):
        collection=db.order
        order_id=list(collection.find({},{"order_id":1}).sort("order_id",-1))[0]["order_id"]+1
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
        print("ep",email,password)
        print("os",order_id,shopping_list)
        print("pd",price,delivery_fee)
        send_email(email,password,order_id,shopping_list,price,delivery_fee)
        Order.notify("\n【編號】"+str(order_id)+"\n商品訂購成功\n查看連結:https://"+os.getenv("website")+"search_order?id="+str(order_id)+"&psw="+password+"&status=customer")

    def search(order_id,password):
        collection=db.order
        result=list(collection.find({
            "$and":[
                {"order_id":int(order_id)},
                {"password":password}
            ]
        }))[0]
        return result
    
    def not_paid():
        collection=db.order
        result=list(collection.find({"$and":[{"pay_status":0},{"disable":0}]}))
        return result
    
    def paid():
        collection=db.order
        result=list(collection.find({"$and":[{"pay_status":1},{"delivery_status":"準備中"},{"disable":0}]}))
        return result
    
    def delivery():
        collection=db.order
        result=list(collection.find({"$and":[{"delivery_status":"寄送中"},{"disable":0}]}))
        return result
    
    
    def check_paid(order_id):
        collection=db.order
        collection.update_one({
        "order_id":int(order_id)},
        {"$set":{"pay_status":1}})

    def check_delivery(order_id):
        collection=db.order
        collection.update_one({
        "order_id":int(order_id)},
        {"$set":{"delivery_status":"寄送中"}})

    def finish(order_id):
        collection=db.order
        collection.update_one({
        "order_id":int(order_id)},
        {"$set":{"delivery_status":"訂單完成","disable":1}})
    
    def notify(mesaage):
        token = os.getenv("line_notify")
        headers = { "Authorization": "Bearer " + token }
        data = { 'message': mesaage }
        requests.post("https://notify-api.line.me/api/notify",
            headers = headers, data = data)

        

