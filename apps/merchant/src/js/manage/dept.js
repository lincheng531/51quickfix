/**
 * Created by ZoeAllen on 16/8/26.
 */
/**
 * 部门管理
 * @constructor
 */
ManageDept = function () {

    var last_dept_ref = null;
    var tree = null;
    var data_table = null;

    this.init_dept = function () {
        $("#tree").fancytree({
            activeVisible: true,
            extensions: ["filter", "dnd", "edit"],
            quicksearch: true,
            source: {
                url: API_HOST + 'user/dept'
            },
            postProcess: function (event, data) {
                var orgResponse = data.response;
                data.result = orgResponse.data;
            },
            init: function (event, data) {
                last_dept_ref = tree.toDict(true).children;
                // expand all
                var root = tree.getRootNode();
                root.visit(function (node) {
                    node.setExpanded(true);
                });
            },
            filter: {
                autoApply: true,
                counter: true,
                fuzzy: false,
                hideExpandedCounter: true,
                highlight: true,
                mode: "dimm"
            },
            dnd: {
                autoExpandMS: 400,
                focusOnClick: true,
                preventVoidMoves: true, // Prevent dropping nodes 'before self', etc.
                preventRecursiveMoves: true, // Prevent dropping nodes on own descendants
                dragStart: function (node, data) {
                    /** This function MUST be defined to enable dragging for the tree.
                     *  Return false to cancel dragging of node.
                     */
                    return true;
                },
                dragEnter: function (node, data) {
                    /** data.otherNode may be null for non-fancytree droppables.
                     *  Return false to disallow dropping on node. In this case
                     *  dragOver and dragLeave are not called.
                     *  Return 'over', 'before, or 'after' to force a hitMode.
                     *  Return ['before', 'after'] to restrict available hitModes.
                     *  Any other return value will calc the hitMode from the cursor position.
                     */
                    // Prevent dropping a parent below another parent (only sort
                    // nodes under the same parent)
                    /*           if(node.parent !== data.otherNode.parent){
                     return false;
                     }
                     // Don't allow dropping *over* a node (would create a child)
                     return ["before", "after"];
                     */
                    return true;
                },
                dragDrop: function (node, data) {
                    /** This function MUST be defined to enable dropping of items on
                     *  the tree.
                     */
                    data.otherNode.moveTo(node, data.hitMode);
                }
            },
            edit: {
                triggerStart: ["f2", "dblclick", "shift+click", "mac+enter"],
                beforeEdit: function (event, data) {
                    // Return false to prevent edit mode
                },
                edit: function (event, data) {
                    // Editor was opened (available as data.input)
                },
                beforeClose: function (event, data) {
                    // Return false to prevent cancel/save (data.input is available)
                    // console.log(event.type, event, data);
                    if (data.originalEvent.type === "mousedown") {
                        // We could prevent the mouse click from generating a blur event
                        // (which would then again close the editor) and return `false` to keep
                        // the editor open:
//                  data.originalEvent.preventDefault();
//                  return false;
                        // Or go on with closing the editor, but discard any changes:
//                  data.save = false;
                    }
                },
                save: function (event, data) {
                    // Save data.input.val() or return false to keep editor open
                    // We return true, so ext-edit will set the current user input
                    // as title
                    update_dept(data.node.key, {name: data.input.val()});
                    return true;
                },
                close: function (event, data) {
                    // Editor was removed
                    if (data.save) {
                        // Since we started an async request, mark the node as preliminary
                        $(data.node.span).addClass("pending");
                    }
                }
            },
            activate: function (event, data) {
                $("#parent_name").text(data.node.title);
                init_data_table();
            },
        });
        // set global
        tree = $("#tree").fancytree("getTree");

        /*
         * Event handlers
         */
        $("#search").keyup(function (e) {
            var n,
                opts = {
                    autoExpand: true,
                    leavesOnly: false
                },
                match = $(this).val();

            if (e && e.which === $.ui.keyCode.ESCAPE || $.trim(match) === "") {
                $("#reset_search").click();
                return;
            }
            if ($("#regex").is(":checked")) {
                // Pass function to perform match
                n = tree.filterNodes(function (node) {
                    return new RegExp(match, "i").test(node.title);
                }, opts);
            } else {
                // Pass a string to perform case insensitive matching
                n = tree.filterNodes(match, opts);
            }
            $("#reset_search").attr("disabled", false);
            $("span#matches").text("(" + n + " matches)");
        }).focus();

        $("#reset_search").click(function (e) {
            $("#search").val("");
            $("span#matches").text("");
            tree.clearFilter();
        }).attr("disabled", true);

    }

    this.bind_event = function () {
        $("#add_ref_btn").click(function () {
            var node = tree.getActiveNode();
            var p = '无';
            if (null != node) {
                p = node.title;
            }
            $("#parent_name").text(p);
            toggle_btn_div();
        });
        $("#close_btn").click(function () {
            toggle_btn_div();
        });
        $('#update_ref_btn').on('click', function () {
            var data = tree.toDict(true).children;
            if (JSON.stringify(last_dept_ref) != JSON.stringify(data)) {
                var paths = parse_path(data, '');
                $.ajax({
                    type: 'PUT',
                    url: API_HOST + 'manage/dept',
                    data: {sort: JSON.stringify(paths)}
                }).done(function () {
                    last_dept_ref = data;
                });
            }
        });
        $("#delete_ref_btn").click(function () {
            var node = tree.getActiveNode();
            if (null == node) {
                toastr.warning("请选择部门");
            }
            // delete dept
            $.ajax({
                type: 'DELETE',
                url: API_HOST + 'manage/dept/' + node.key,
            }).done(function () {
                node.remove();
            });
        });
    }

    this.validate_form = function (form_id) {
        // MyUtils.form_elements(form_id);
        var form = $('#' + form_id);
        form.parsley().on('form:submit', function () {
            var data = form.serializeArray();
            var node = tree.getActiveNode();
            add_dept(node, data);
            return false;
        });
    }

    function init_data_table() {
        if (null == data_table) {
            $("#table_div").removeClass('hide');
            data_table = $('#data_table').DataTable({
                'language': DATATABLE_LANGUAGE,
                "paging": true,
                "pageLength": 50,
                "searching": true,
                "ordering": true,
                "info": false,
                "autoWidth": true,
                "responsive": true,
                "select": {
                    style: 'single'
                },
                "order": [[0, "desc"]],
                "ajax": {
                    "url": API_HOST + "manage/dept/ref",
                    "dataSrc": "data"
                },
                "columns": [
                    {
                        "data": "user.username", "name": "user.username"
                    },
                    {
                        "data": "user", "name": "user",
                        'mRender': function (data, type, full) {
                            return (data.last_name + data.first_name) || data.username;
                        }
                    },
                    {
                        "data": "dept.name", "name": "dept.name"
                    },
                    {
                        "data": "role", "name": "role"
                    },
                    {
                        "data": "level", "name": "level",
                        "mRender": function (data, type, full) {
                            return data;
                        }
                    },
                    {
                        "data": "is_leader", "name": "is_leader",
                    }
                ],
                "fnServerParams": function (aoData) {
                    var node = tree.getActiveNode();
                    aoData.push({"name": "dept", "value": node.key});
                    aoData.push({"name": "is_leader", "value": $("#leader_select").val()});
                }
            });
        } else {
            data_table.ajax.reload();
        }

        $("#leader_select").on('change', function () {
            if (data_table) {
                data_table.ajax.reload();
            }
        });
    }

    function toggle_btn_div() {
        $("#dept_form").toggleClass('hide');
        $("#btn_div").toggleClass('hide');
    }

    /**
     * parse dept path
     * @param data
     * @param p_id
     * @returns {Array}
     */
    function parse_path(data, p_id) {
        var res = [];
        for (var i in data) {
            var d = data[i];
            var id = d.key;
            var path = p_id + '/' + id;
            res.push({'path': path, 'id': id});
            var childs = d.children;
            if (childs && childs.length > 0) {
                // combine data
                res = res.concat(parse_path(childs, path));
            }
        }
        return res;
    }

    /**
     * 新增部门
     */
    function add_dept(parent, data) {
        if (null != parent) {
            data.push({name: 'parent', value: parent.key});
        }
        $.ajax({
            type: 'POST',
            url: API_HOST + 'manage/dept',
            data: data
        }).done(function (resp) {
            var d = resp.data;
            if (null == parent) {
                parent = tree.getRootNode();
            }
            d.title = d.name;
            d.key = d.id;
            parent.addChildren(d);
            // clean form
            $("#dept_form")[0].reset();
        });
    }

    /**
     * 修改部门名称
     */
    function update_dept(key, data) {
        $.ajax({
            type: 'PATCH',
            url: API_HOST + 'manage/dept/' + key,
            data: data
        }).done(function (resp) {

        });
    }

}
