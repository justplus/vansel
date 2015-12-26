/*
 * jQuery File Upload Plugin JS Example 8.9.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/* global $, window */

$(function () {
    'use strict';
    var file_data;
    $('#fileupload').fileupload({
        url: '/upload',
        dataType: 'json',
        autoUpload: false,
        maxFileSize: 5000000 // 5 MB
    }).on('fileuploadadd', function (e, data) {
        data.context = $('<div/>').appendTo('#files');
        $.each(data.files, function (index, file) {
            $('#file-name').html(file.name);
            if (!index) {
                $('#upload-btn').clone(true).data(data);
                $('#upload-btn').css('display', 'inline-block');
                $('#upload-btn').text('上传');
                $('#cancel-btn').text('取消上传');
                $('#add-btn').css('display', 'none');
            }
            file_data = data;
        });
    }).on('fileuploadprogressall', function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#upload-btn').text('上传中...'+progress+'%');
    }).on('fileuploaddone', function (e, data) {
        $('#message-text').attr('last_id', data['result']['last_id']);
        $('#upload-btn').text('上传完成');
        $('#cancel-btn').css('display', 'none');

    }).on('fileuploadfail', function (e, data) {
        $('#cancel-btn').text('上传失败');
        $('#upload-btn').css('display', 'none');
        $('#add-btn').css('display', 'inline-block');
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');


    $('#upload-btn').on('click', function () {
        var $this = $(this);
        $this.prop('disabled', true);
        $('#cancel-btn').css('display', 'inline-block');
        file_data.submit(function (e) {

        });
    });
    $('#cancel-btn').on('click', function(){
        file_data.abort();
        $('#cancel-btn').css('display', 'none');
        $('#upload-btn').text('上传');
        $('#upload-btn').prop('disabled', false);
        $('#upload-btn').css('display', 'inline-block');
        $('#add-btn').css('display', 'inline-block');
    });

    window.submit_modification = function(project_id) {
        $('#updateRequirementModal').modal('toggle');
        $.ajax({
                url: '/admin/pm/modify',
                data: {
                    'modification':$('#message-text').val(),
                    'project_id':project_id,
                    'last_id':$('#message-text').attr('last_id')
                },
                type: 'POST',
                success:function(data){
                    if(data['statusCode'] == 200){
                        location.reload(true);
                    }
                },
                error:function(err){
                    console.log(err);
                }
            });
    };
});
