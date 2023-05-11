from crypt import methods
from imp import reload
from dotenv import load_dotenv
import pymongo,certifi,os

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