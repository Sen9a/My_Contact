$(document).ready(function(){
    var options = {
      url : edit_url,
      dataType:'json',
      beforeSubmit: showRequest_edit,
      success : showResponse_edit,
    };
    $('#my_add_info').submit(function(){
      $(this).ajaxSubmit(options);
      return false;
    });
});


function showRequest_edit(formData,jqForm,options){
  $('body').addClass("loading"); 
  return true
}

function showResponse_edit(json){
  $('body').removeClass("loading");
  if (json.ok){
    if(!alert(json.ok)){document.location = 'http://127.0.0.1:8000/'};
  }else{
    $('ul.error').remove()
    for (var i in json){
      $('<ul class="error"><li>'+json[i]+'</li></ul>').insertBefore('[for=id_'+i);
    }; 
  }
}
