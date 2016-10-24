    KindEditor.ready(function(K) {
            window.editor = K.editor({
                    height:'500px',
                    uploadJson : '/api/v1/upload/?category=product',
                    fileManagerJson : '../asp/file_manager_json.asp',
                    allowFileManager : false,
                });

                K('#id_logo').click(function() {
                    editor.loadPlugin('image', function() {
                        editor.plugin.imageDialog({
                            imageUrl : K('#id_logo').val(),
                            clickFn : function(url, title, width, height, border, align) {
                                K('#id_logo').val(url);
                                editor.hideDialog();
                            }
                        });
                    });
                });

    });
