$(document).ready(function () {
    var shopping_list=[]
    $.ajax({
        url: "/get_cart",
        type: "get",
        contentType: "application/json",
        data: {
        },
        success: function (response) {
            // alert("response"+JSON.parse(response))
            shopping_list=eval(JSON.parse(response))
            // alert("shopping_list"+JSON.stringify(shopping_list))
        }   
    }) 

        $("#shopping_cart").html("");
        setTimeout(() => {
            for (var i = 0; i < shopping_list.length ; i++) {
                $("#shopping_cart").append(`<tr><th scope="row">`+shopping_list[i].name+`</th><td>`+parseInt(shopping_list[i].price)+`</td><td>`+parseInt(shopping_list[i].number)+`</td><td>`+parseInt(shopping_list[i].price)*parseInt(shopping_list[i].number)+`</td><td><button class="btn btn-danger" onclick="location.href='/delete_cart?name=`+shopping_list[i].name+`'">刪除</td></tr>`)
                }
                $("#shopping_number").html(`<i class="fa fa-fw fa-cart-arrow-down text-dark mr-1"></i><span class="position-absolute top-0 left-100 translate-middle badge rounded-pill bg-light text-dark" >`+shopping_list.length+`</span>`)
        }, 500);
        


    $(".ajax_button").click(function () {
        $.ajax({
            url: "",
            type: "get",
            contentType: "application/json",
            data: {
                button_text: $(this).text(),
                button_class: $(this).attr('class')
            },
            success: function (response) {
                $('#add_'+response.id).html(`<a class="btn btn-success text-white mt-2" href="/add_to_cart?id=`+response.id+`&size=`+response.size+`" id=add_"`+response.id+`"><i class="fas fa-cart-plus"></i></a>`);
                $('#look_'+response.id).html(`<a class="btn btn-success text-white mt-2"  href="/shop_single?id=`+response.id+`&size=`+response.size+`" id=look_"`+response.id+`"><i class="far fa-eye"></i></a>`);
                $('#name_'+response.id).html(`<a  class="h3 text-decoration-none" style="font-weight:400 !important; font-size: large !important;" href="/shop_single?id=`+response.id+`&size=`+response.size+`">`+response.name+`（`+response.size+`）</a>`);
                $('#inventory_'+response.id).html(`<p class="text-center text-muted mb-0  " style="font-weight: 400 !important;">商品剩餘:`+response.inventory+`個`);
                $('#price_'+response.id).html(`<p class="text-center mb-0" style="font-size: medium !important;">$`+response.price);
            }   
        }) 
    })
    $(".item_button").click(function () {
        $.ajax({
            url: "",
            type: "get",
            contentType: "application/json",
            data: {
                button_text: $(this).text(),
                button_class: $(this).attr('class')
            },
            success: function (response) {
                $('#name_'+response.id).html(`<h1 style="display: none;" id="id">`+response.id+`</h1><h1 style="display: none;" id="product">`+response.name+`（`+response.size+`）</h1><h1 class="h2 text-400" id="name">`+response.name+`<span>（</span><span id="size">`+response.size+`</span><span>）</span></h1>`);
                $('#price_'+response.id).html(`<span class="h3 py-2">$</span><span class="h3 py-2" id="price">`+response.price+`</span>`);
                
            }   
        }) 
    })
    $(".add_to_cart_button").click(function () 
    {   
        if (shopping_list.length != 0){
            for (var i = 0; i < shopping_list.length ; i++) {
                if (shopping_list[i].name == $("#product").text()){
                    shopping_list[i].number+=parseInt($("#var-value").text())
                    var status="changed"
                    // alert(1)
                    break;
                }
              }    
            if (status!="changed"){
                shopping_list.push({id:parseInt($("#id").text()),name:$("#name").text(),size:$("#size").text(),price:parseInt($("#price").text()),number:parseInt($("#var-value").text())});
                // alert(2)
            }

        }
        else{
            // alert(3)
            shopping_list.push({id:parseInt($("#id").text()),name:$("#name").text(),size:$("#size").text(),price:parseInt($("#price").text()),number:parseInt($("#var-value").text())});
        }
        // alert("shopping_list"+JSON.stringify(shopping_list))
        $("#shopping_cart").html("");
        for (var i = 0; i < shopping_list.length ; i++) {
            $("#shopping_cart").append(`<tr><th scope="row">`+shopping_list[i].name+`</th><td>`+parseInt(shopping_list[i].price)+`</td><td>`+parseInt(shopping_list[i].number)+`</td><td>`+parseInt(shopping_list[i].price)*parseInt(shopping_list[i].number)+`</td><td><button class="btn btn-danger" onclick="location.href='/delete_cart?name=`+shopping_list[i].name+`'">刪除</td></tr>`)
            }
        $("#shopping_number").html(`<i class="fa fa-fw fa-cart-arrow-down text-dark mr-1"></i><span class="position-absolute top-0 left-100 translate-middle badge rounded-pill bg-light text-dark" >`+shopping_list.length+`</span>`)
        
        alert("產品成功")
        $.ajax({
            url: "/add_to_cart",
            type: "get",
            contentType: "application/json",
            data: {
                shop:JSON.stringify(shopping_list)
            },
            success: function (response) {
                // alert("ajax_success")
            }   
        }) 
    })


    $(".flush_button").click(function () {
        $.ajax({
            url: "/get_cart",
            type: "get",
            contentType: "application/json",
            data: {
            },
            success: function (response) {
                shopping_list=eval(JSON.parse(response))
            }   
        }) 

            $("#shopping_cart").html("");
            setTimeout(() => {
                for (var i = 0; i < shopping_list.length ; i++) {
                    $("#shopping_cart").append(`<tr><th scope="row">`+shopping_list[i].name+`</th><td>`+parseInt(shopping_list[i].price)+`</td><td>`+parseInt(shopping_list[i].number)+`</td><td>`+parseInt(shopping_list[i].price)*parseInt(shopping_list[i].number)+`</td><td><button class="btn btn-danger">刪除</td></tr>`)
                    }
                    $("#shopping_number").html(`<i class="fa fa-fw fa-cart-arrow-down text-dark mr-1"></i><span class="position-absolute top-0 left-100 translate-middle badge rounded-pill bg-light text-dark" >`+shopping_list.length+`</span>`)
            }, 500);
            

    })
});




