from crypt import methods
from imp import reload
from flask import*
from unittest import result
from requests import Session
from dotenv import load_dotenv


from model import *

import pymongo ,certifi,math,os

load_dotenv()
#初始化資料庫連線
client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.shop
print('\x1b[6;30;42m' + 'x資料庫連線成功'.center(87) + '\x1b[0m')

#初始化 flask 伺服器
app=Flask(
    __name__,
    static_folder="assets",
    static_url_path="/assets"
)
app.secret_key="any string"
shopping_dict=[""]
@app.route("/")
def index():
    related_product_list=[]
    collection=db.product
    product_result=list(collection.find())
    for i in product_result:
        related_product_list.append(Product(i["_id"],i["name"],i["price"],i["size"],i["photo"],i["introduction"],i["categories"],i["inventory"],i["disable"]))
        if len(related_product_list)>=3:
            break
    return render_template("index.html",related_product_list=related_product_list)

@app.route("/shop")
def shop_page():
    #get_product_information
    if request.is_json:
        result=Product.get_inform(request.args.get("button_text"),request.args.get("button_class").split()[7])
        return jsonify(id=result[0]["_id"],size=result[0]["size"][result[1]],inventory=result[0]["inventory"][result[1]],price=result[0]["price"][result[1]],name=result[0]["name"])
    
    #get_product_list_page
    product_list=[]
    if not request.args.get("categories"):
        collection=db.product
        product_result=list(collection.find())
        page_number=math.ceil(len(product_result)/9)
    else:
        collection=db.product
        product_result=list(collection.find({"categories":request.args.get("categories")}))
        page_number=math.ceil(len(product_result)/9)

    if not request.args.get("page"):
        current_page=1
    else:
        current_page=int(request.args.get("page"))
    items=0
    for i in product_result:
        print(current_page*9,current_page*9-9,items)
        if items<current_page*9 and items>=current_page*9-9:
            product_list.append(Product(i["_id"],i["name"],i["price"],i["size"],i["photo"],i["introduction"],i["categories"],i["inventory"],i["disable"]))
        items+=1
    return render_template("shop.html",product_list=product_list,page_number=page_number,current_page=current_page)


@app.route("/shop_single")
def shop_single():
    #get_product_information
    if request.is_json:
        result=Product.get_inform(request.args.get("button_text"),request.args.get("id"))
        return jsonify(id=result[0]["_id"],size=result[0]["size"][result[1]],inventory=result[0]["inventory"][result[1]],price=result[0]["price"][result[1]],name=result[0]["name"])
    
    #get_each_product_page
    result=Product.get_inform(request.args.get("size"),request.args.get("id"))
    focus_item=Product(result[0]["_id"],result[0]["name"],result[0]["price"][result[1]],result[0]["size"][result[1]],result[0]["photo"],result[0]["introduction"],result[0]["categories"],result[0]["inventory"],result[0]["disable"])
    
    related_product_list=[]
    collection=db.product
    product_result=list(collection.find())
    for i in product_result:
        related_product_list.append(Product(i["_id"],i["name"],i["price"],i["size"],i["photo"],i["introduction"],i["categories"],i["inventory"],i["disable"]))
        if len(related_product_list)>8:
            break
    return render_template("shop-single.html",focus_item=focus_item,size_list=result[0]["size"],related_product_list=related_product_list)

@app.route("/add_to_cart")
def add_to_cart():
    session["shopping_list_python"]=list(json.loads(request.args.get("shop")))
    session["shopping_list"]=json.dumps(request.args.get("shop"))
    return "此功能尚未開放"

@app.route("/get_cart")
def get_cart():
    if request.is_json: 
        if not session["shopping_list"]:
            return "error"
        else:
            return session["shopping_list"]
    
@app.route("/delete_cart")
def delete_cart():
    print(session["shopping_list_python"])
    print(request.args.get("name"))
    for i in range(0,len(session["shopping_list_python"])):
        if session["shopping_list_python"][i]["name"]==request.args.get("name"):
            del session["shopping_list_python"][i]
            break
    session["shopping_list"]=json.dumps(session["shopping_list_python"])
    return redirect("/shop")

@app.route("/buy")
def buy():
    try:
        print("HERE",session["shopping_list_python"][0]["number"])
    except:
        print("IM")
        return render_template("error.html",message=["您的購物車沒有商品","快把喜歡的商品帶回家～"])
    print(session["shopping_list_python"])
    shopping_list=session["shopping_list_python"]
    number=0
    cost=0
    delivery_fee=0
    for i in shopping_list:
        number+=1
        cost+=i["number"]*i["price"]
        i["photo"]=Product.get_photo(i["id"])
        i["serial_number"]=number
    if cost<3000:
        delivery_fee=245
        cost=cost+delivery_fee
    session["cost"]=cost
    session["delivery_fee"]=delivery_fee

    return render_template("shop-cart.html",shopping_list=shopping_list,list_len=len(shopping_list),cost=cost,delivery_fee=delivery_fee)

@app.route("/finish_buying",methods=["POST"])
def finish_buying():
    Order.update(request.form.get("phone"),request.form.get("email"),request.form.get("address"),request.form.get("account"),session["cost"],session["shopping_list_python"])
    session.clear()
    return render_template("error.html",message=["商品訂購成功","請檢查電子郵件訊息"])

@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")

# @app.route("/test",methods=["GET","POST"])
# def test():
#     if request.is_json:
#         text=request.args.get("button_text")
#         text_1=request.args.get("button_class")
#         print(text_1)
#         data_list=[0,1,2,3,4,5]
#         collection=db.product
#         product_result=list(list(collection.find())[0].items())
#         return jsonify(seconds=text,number=random.randint(1,10),length=len(data_list),data_list=data_list,product_result=product_result)
#         # return jsonify(product_result=product_result,length=len(product_result))
#     return render_template("home.html")

if __name__=='__main__':
    app.run(port=5000,debug=True)