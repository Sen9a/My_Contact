var btnCust = '<button type="button" class="btn btn-default " title="Add picture tags" ' + 
    'onclick="my_foto_delete()">' +
    '<i class="glyphicon glyphicon-tag"></i>' +
    '</button>'; 
$("#id_image").fileinput({
    overwriteInitial: true,
    maxFileSize: 1500,
    showClose: false,
    showCaption: false,
    browseLabel: '',
    removeLabel: '',
    browseIcon: '<i class="glyphicon glyphicon-folder-open"></i>',
    removeIcon: '<i class="glyphicon glyphicon-remove"></i>',
    removeTitle: 'Cancel or reset changes',
    elErrorContainer: '#kv-avatar-errors-1',
    msgErrorClass: 'alert alert-block alert-danger',
    defaultPreviewContent: '<img src='+ image_value +'/>',
    layoutTemplates: {main2: '{preview} ' +  btnCust + ' {remove} {browse}'},
    allowedFileExtensions: ["jpg"]
});

function my_foto_delete(){
    if ($('#for_delete').val()){
        $('#for_delete').remove();
        $('#kv-avatar-errors-1').attr('style','display:none');
    }else{
        $('#photo').remove();
        $('<input id="for_delete" value=1 name="delete_foto" type="hidden">').insertBefore("div.sen");
        $('#kv-avatar-errors-1').attr('style','width:500px').prepend("<ul id=photo class = 'error'><li>Your avatar will be deleted</li></ul>");
    }
}