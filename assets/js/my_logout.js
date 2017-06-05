$(document).ready(function(){
    var options = {
      url : '/logout',
      dataType:'json',
      beforeSubmit: showRequest1,
      success : showResponse2,
    };
    $('#my_logout').submit(function(){
      $(this).ajaxSubmit(options);
      return false;
    });
});


function showRequest1(formData,jqForm,options){
  $('body').addClass("loading"); 
  return true
}
function showResponse2(json){
  $('body').removeClass("loading");
  if(json.bay){
    alert(json.bay);
    location.reload();
  };
};