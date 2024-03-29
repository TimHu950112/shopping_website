from flask import*
from dotenv import load_dotenv
from model import *
from datetime import date,datetime
import pymongo ,certifi,math,os,pytz

load_dotenv()
#初始化資料庫連線
client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.shop
print('\x1b[6;30;42m' + 'x資料庫連線成功'.center(87) + '\x1b[0m')

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(os.getenv('line_access'))
handler = WebhookHandler(os.getenv('line_secret'))

#初始化 flask 伺服器
app=Flask(
    __name__,
    static_folder="assets",
    static_url_path="/assets"
)
app.secret_key=os.getenv("secret_key")
shopping_dict=[""]



        
    
@app.route("/")
def index():
    related_product_list=[]
    collection=db.product
    product_result=list(collection.find({"disable":0}))
    for i in product_result:
        related_product_list.append(Product(i["_id"],i["name"],i["price"],i["size"],i["photo"],i["introduction"],i["categories"],i["inventory"],i["disable"]))
        if len(related_product_list)>=3:
            break
    # return '此網站已停用，請聯繫客服'
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
        product_result=list(collection.find({"disable":0}))
        page_number=math.ceil(len(product_result)/9)
    else:
        collection=db.product
        product_result=list(collection.find({"$and":[{"categories":request.args.get("categories")},{"disable":0}]}))
        page_number=math.ceil(len(product_result)/9)

    if not request.args.get("page"):
        current_page=1
    else:
        current_page=int(request.args.get("page"))
    items=0
    for i in product_result:
        # print(current_page*9,current_page*9-9,items)
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
    if result==None:
        return redirect("/error?msg=商品已不存在")
    focus_item=Product(result[0]["_id"],result[0]["name"],result[0]["price"][result[1]],result[0]["size"][result[1]],result[0]["photo"],result[0]["introduction"],result[0]["categories"],result[0]["inventory"],result[0]["disable"])
    
    related_product_list=[]
    collection=db.product
    product_result=list(collection.find({"disable":0}))
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
        try:
            if not session["shopping_list"]:
                return "error"
            else:
                return session["shopping_list"]
        except:
            return "error"
    
@app.route("/delete_cart")
def delete_cart():
    # print(session["shopping_list_python"])
    # print(request.args.get("name"))
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
    # print(session["shopping_list_python"])
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
    Order.update(request.form.get("phone"),request.form.get("email"),request.form.get("address"),request.form.get("account"),session["cost"],session["shopping_list_python"],session["delivery_fee"])
    session.clear()
    return render_template("error.html",message=["商品訂購成功","請檢查電子郵件訊息"])

@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")

@app.route("/search_order")
def search_order():
    try:
        order_result=Order.search(request.args.get("id"),request.args.get("psw"))
    except:
        return redirect("/error?msg=發生錯誤，請稍後再試")
    if request.args.get("status")=="customer":
        return render_template("order-cart.html",shopping_list=order_result["shopping_list"],data_result=order_result)
    else:
        return render_template("admin-cart.html",shopping_list=order_result["shopping_list"],data_result=order_result)


@app.route("/admin_page")
def admin_page():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    not_paid=Order.not_paid()
    paid=Order.paid()
    delivery=Order.delivery()
    return render_template("admin.html",nickname=session["member_data"]["nickname"],not_paid=not_paid,paid=paid,delivery=delivery,not_paid_len=len(not_paid),paid_len=len(paid),delivery_len=len(delivery))

@app.route("/function",methods=["POST"])
def function():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    try:
        result=request.form["function"]
    except:
        flash("請選擇功能")
        return redirect("/admin_page")
    if result=="order-list":
        return redirect("/admin_page")
    elif result=="add-product":
        return redirect("/add_product_page")
    elif result=="manage-product":
        return redirect("/manage_product_page")
    elif result=="website-function":
        return redirect("/website_function")
    elif result=="logout":
        session.clear()
        return redirect("/error?msg=登出成功")
    
@app.route("/check_paid")
def check_paid():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    Order.check_paid(request.args.get("id"))
    flash("付款成功")
    return redirect("/admin_page")

@app.route("/check_delivery")
def check_delivery():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    Order.check_delivery(request.args.get("id"))
    flash("寄送成功")
    return redirect("/admin_page")

@app.route("/check_arrived")
def check_arrived():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    Order.finish(request.args.get("id"))
    flash("完成訂單")
    return redirect("/admin_page")

@app.route("/login_page")
def login_page():
    if "member_data" in session:
        return redirect("/admin_page")
    return render_template("login.html")

@app.route("/login",methods=["GET","POST"])
def login():
    result=Admin.login(request.form["email"],request.form["password"])
    if result == False:
        Order.notify("\n"+ "【帳號密碼輸入錯誤】")
        flash("帳號或密碼錯誤")
        return render_template("login.html")
    session["member_data"]={"email":request.form["email"],"password":request.form["password"],"nickname":result}
    return redirect("/admin_page")

@app.route("/logout")
def logout():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    session.clear()

@app.route("/website_function")
def website_function():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    website_functions=System.check_function()
    return render_template("website-function.html",website_functions=website_functions,website_functions_len=len(website_functions),nickname=session["member_data"]["nickname"])



@app.route("/add_product_page")
def add_product_page():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    collection=db.product
    product_id=int(list(collection.find({},{"_id":1}).sort("_id",-1))[0]["_id"])+1
    return render_template("add-product.html",product_id=product_id)

@app.route("/add_product",methods=["POST"])
def add_product():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    Product.update(request.form["_id"],request.form["product_name"],request.form["price"],request.form["size"],session["photo"],request.form["introduction"],request.form["categories"],request.form["inventory"])
    flash("產品新增成功")
    return redirect("/add_product_page")

@app.route("/upload_image")
def upload_image():
    if request.is_json:
        session["photo"]=request.args.get("image_url")
        return "圖片上傳成功"

@app.route("/manage_product_page")
def manage_product_page():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    #get_product_list_page
    product_list=[]
    if not request.args.get("categories"):
        collection=db.product
        product_result=list(collection.find({"disable":0}))
        page_number=math.ceil(len(product_result)/9)
    else:
        collection=db.product
        product_result=list(collection.find({"$and":[{"categories":request.args.get("categories")},{"disable":0}]}))
        page_number=math.ceil(len(product_result)/9)

    if not request.args.get("page"):
        current_page=1
    else:
        current_page=int(request.args.get("page"))
    items=0
    for i in product_result:
        # print(current_page*9,current_page*9-9,items)
        if items<current_page*9 and items>=current_page*9-9:
            product_list.append(Product(i["_id"],i["name"],i["price"],i["size"],i["photo"],i["introduction"],i["categories"],i["inventory"],i["disable"]))
        items+=1
    return render_template("manage-product.html",product_list=product_list,page_number=page_number,current_page=current_page)

@app.route("/delete")
def delete():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    Product.delete(request.args.get("id"))
    flash("刪除成功")
    return redirect("/manage_product_page")
@app.route("/error")
def error():
    return render_template("error.html",message=["系統提示",request.args.get("msg")])
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

@app.route("/notify")
def route_notify():
    if not "member_data" in session:    
        flash("請先登入")
        return render_template("login.html")
    Order.notify(request.args.get('notify'))
    return "success"

#linebot
# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.text=='今日貨態查詢':
            reply=KOFU.search(datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d'))
            if reply!=False:
                text='【今日貨態查詢】'
                text_value=[]
                zone=''
                for i in reply:
                    text_value.append([i['date'],i['time'],i['location'],i['product'],i['zone']])
                for i in text_value:
                    if i[4]!=zone:
                        zone=i[4]
                        text+='\n\n-----------------\n    ✲'+zone+'✲\n-----------------\n【日期】: '+i[0]+'\n【時間】: '+i[1]+'\n【地點】: '+i[2]+'\n【產品與數量】: 芼荷'+i[3]+'對'
                    else:
                        text+='\n\n【日期】: '+i[0]+'\n【時間】: '+i[1]+'\n【地點】: '+i[2]+'\n【產品與數量】: 芼荷'+i[3]+'對'
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage('尚未送達或無訂單'))
        elif '/送達' in event.message.text:
            text=event.message.text.split()
            KOFU.update(text[1],text[2])
            # line_bot_api.broadcast(TextSendMessage(text='【商品送達通知】\n【日期】:'+datetime.now(pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d')+'\n【時間】:'+datetime.now(pytz.timezone('Asia/Taipei')).strftime('%H:%M')+'\n【地點】: ' + text[1] + '\n【產品與數量】: 芼荷' + text[2]+'對'))
            line_bot_api.reply_message(event.reply_token,TextSendMessage('登記成功'))
        elif '/維護通知' in event.message.text:
            line_bot_api.broadcast(TextMessage(text='【系統維護通知】\n 目前系統維護中，將暫時關閉送達通知功能，但您仍可以利用下方貨態查詢按鍵查詢。造成您的不便，敬請見諒'))
        elif '-' in event.message.text:
            try:
                reply=KOFU.search(event.message.text)
                if reply!=False:
                    text='【指定日期貨態查詢】'
                    text_value=[]
                    zone=''
                    for i in reply:
                        text_value.append([i['date'],i['time'],i['location'],i['product'],i['zone']])
                    for i in text_value:
                        if i[4]!=zone:
                            zone=i[4]
                            text+='\n\n-----------------\n    ✲'+zone+'✲\n-----------------\n【日期】: '+i[0]+'\n【時間】: '+i[1]+'\n【地點】: '+i[2]+'\n【產品與數量】: 芼荷'+i[3]+'對'
                        else:
                            text+='\n\n【日期】: '+i[0]+'\n【時間】: '+i[1]+'\n【地點】: '+i[2]+'\n【產品與數量】: 芼荷'+i[3]+'對'
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text))
                else:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage('查無訂單'))
            except:
                line_bot_api.reply_message(event.reply_token,TextSendMessage('發生錯誤，請檢查格式'))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage('很抱歉，您的回覆超出了我的能力範圍'))
    return 200



if __name__=='__main__':
    app.run(port=5500,debug=True)