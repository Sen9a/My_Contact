$(document).ready(function(){
    var options = {
      url : '/login',
      dataType:'json',
      beforeSubmit: showRequest,
      success : showResponse,
    };
    $('#my_login').submit(function(){
      $(this).ajaxSubmit(options);
      return false;
    });
});


function showRequest(formData,jqForm,options){
  $('body').addClass("loading"); 
  return true
}
function showResponse(json){
  $('body').removeClass("loading");
  if(json.username){
    alert('Welkome '+json.username);
    location.reload();
  };
  if(json.user_error){
    alert(json.user_error);
  };
};

