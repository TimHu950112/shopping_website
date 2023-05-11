from crypt import methods
from imp import reload
from dotenv import load_dotenv
import pymongo,certifi,os,random,string

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
    def update(phone,email,address,account,price,shopping_list):
        collection=db.order
        order_id=list(collection.find({},{"order_id":1}).sort("order_id",-1))[0]["order_id"]+1
        letters = string.ascii_uppercase + string.digits
        password= ''.join(random.choice(letters) for i in range(5))
        collection.insert_one({
            "order_id":order_id,
            "phone":phone,
            "email":email,
            "address":address,
            "account":account,
            "price":int(price),
            "password":password,
            "shopping_list":shopping_list,
            "delivery_status":"準備中",
            "pay_status":0,
            "disable":0
        })
        Order.email(email,password)
        
    def email(email_address,password):
        import email.message,smtplib
        msg=email.message.EmailMessage()
        msg["From"]=os.getenv("FROM_EMAIL")
        msg["To"]=email_address
        msg["Subject"]="產品訂購成功通知"
        msg.add_alternative("<h3>您的密碼是：</h3>"+password,subtype="html") #HTML信件內容

        server=smtplib.SMTP_SSL("smtp.gmail.com",465) #建立gmail連驗
        server.login(os.getenv("FROM_EMAIL"),os.getenv("GOOGLE_PASSWORD"))
        server.send_message(msg)
        server.close() #發送完成後關閉連線
        print("發送成功")

