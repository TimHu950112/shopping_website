$('.imgur').change(function() {
    var reader = new FileReader();
    reader.onload = function(e) {
    var iurl = e.target.result.substr(e.target.result.indexOf(",") + 1, e.target.result.length);
    var clientId = "3328cf6f44c685f";               
    $.ajax({
     url: "https://api.imgur.com/3/upload",
     type: "POST",
     datatype: "json",
     data: {
     'image': iurl,
     'type': 'base64'
     },
     success: fdone,
     error: function(){alert("圖片上傳失敗，請稍後再試")},
     beforeSend: function (xhr) {
         xhr.setRequestHeader("Authorization", "Client-ID " + clientId);
     }
 });
 };
  reader.readAsDataURL(this.files[0]);
 });

 function fdone(data)
{
   $.ajax({
    url: "/upload_image",
    type: "get",
    contentType: "application/json",
    data: {
        image_url:data.data.link
    },
    success: function (response) {
        // alert("response"+JSON.parse(response))
        console.log(data.data.link)
        alert(response)
        // alert("shopping_list"+JSON.stringify(shopping_list))
    }   
})    
}
                    
//  
//                                  _oo8oo_
//                                 o8888888o
//                                 88" . "88
//                                 (| -_- |)
//                                 0\  =  /0
//                               ___/'==='\___
//                             .' \\|     |// '.
//                            / \\|||  :  |||// \
//                           / _||||| -:- |||||_ \
//                          |   | \\\  -  /// |   |
//                          | \_|  ''\---/''  |_/ |
//                          \  .-\__  '-'  __/-.  /
//                        ___'. .'  /--.--\  '. .'___
//                     ."" '<  '.___\_<|>_/___.'  >' "".
//                    | | :  `- \`.:`\ _ /`:.`/ -`  : | |
//                    \  \ `-.   \_ __\ /__ _/   .-` /  /
//                =====`-.____`.___ \_____/ ___.`____.-`=====
//                                  `=---=`
//  
//  
// 
//                          佛祖保佑         永无bug
//                          