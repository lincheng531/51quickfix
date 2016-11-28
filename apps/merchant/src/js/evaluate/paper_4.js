/**
 * Created by xujingxiang on 16/11/4.
 */

Paper = function () {
    // stop refresh
    window.onbeforeunload = function () {
        return "You work will be lost.";
    };
    var extend_flag = null;
    // parts value2Arrayay
    // var part = MyUtils.shuffle([1, 2, 3, 4, 5]);
    var part = [1, 2, 3, 4, 5,6,7];
    // set part7 to end
    part.push(7);
    var part_index = 0;
    // var part_mapping = {
    //     1: '逻辑推理',
    //     2: '反应速度',
    //     3: '逻辑推理',
    //     4: '逻辑推理',
    //     5: '语义理解'
    // };
    var part_mapping = {
        1: '数字敏感',
        2: '逻辑推理',
        3: '空间感知',
        4: '反应速度',
        5: '记忆力模块',
        6: '语义理解'
    };
    // load question mapping
    var load_mapping = {
        1: load_question1,
        2: load_question2,
        3: load_question3,
        4: load_question4,
        5: load_question5,
        6: load_question6
    };

    // switch time ms
    var switch_time = 1000;
    // part time config
    var part_timer = {};
    var part_timer_default = 60 * 1000 * 2;

    var timer_id = null;
    // paper
    var paper_id = null;
    // current question
    var question = null;
    //currenr question id
    var currentid=null;
    // 1:demo 0:real
    var demo_status = null;
    // correct count
    var demo_count = 0;
    var demo_correct_count = 3;
    var random_name = [['n1', 'n2'], ['n2', 'n1']];

    this.bind_paper = function () {
        //在线测试环节的跳转
        $("#paper_desc").on('click', function () {
            $(this).hide();
            $("#paper_desc_2").fadeIn();
        });
        //开始测试按钮
        $("#start_btn").on('click', function () {
            if (screenfull.enabled) {
                $("#aside").addClass('hide');
                // $("#header_div").addClass('hide');
                $("#main_content").fadeOut().remove();
                // screenfull.request();
                start_part();
            }
        });
        bind_paper_show();
    };

    this.init_paper = function (key, flag) {
        // set global
        extend_flag = flag;
        // key is paper id
        // get paper basic info
        $.getJSON(API_HOST + 'evaluate/paper/' + key, function (resp) {
            if (resp.code == 0){
                var data = resp.data;
                paper_id = data.id;
                console.log(paper_id);
                var status = data.status;
                $("#paper_title").text(data.name);
                if (status == 1) {
                    $("#paper_desc").fadeIn();
                } else if (status == 2) {
                    $("#paper_end").fadeIn();
                } else if (status == 3) {
                    $("#main_content").fadeOut();
                    get_extend();
                }
            }
        });

        // load part timer config
        // $.getJSON(API_HOST + 'evaluate/timer/' + key, function (resp) {
        //     if (resp.code == 0) {
        //         var data = resp.data;
        //         for (var i in data) {
        //             part_timer[parseInt(data[i].part)] = data[i].timer * 60 * 1000;
        //         }
        //     }
        // });

    };

    function start_part() {
        var index = part[part_index];
        $("#part_" + index).fadeIn();


        // $("#part_2").fadeIn();



        window.setTimeout(function () {
            $('#part' + index + '_title').remove();
            $('#part' + index + '_show_1').fadeIn();


            // $('#part2_title').remove();
            // $('#part2_show_1').fadeIn();


        }, switch_time);
    };

    function load_question5() {
    //     $.getJSON(API_HOST + 'toc/topic/number?id=' + paper_id + '&demo=' + demo_status, function (resp) {
    //         toastr.clear();
    //         console.log(resp);
    //         if (resp.code == 0) {
    //             var data = resp.data;
    //             if(demo_status==1){
    //                 var value1=data[0].expression,value2=data[1].expression;
    //             }else{
    //                 var value1=data.data[0].expression,value2=data.data[1].expression;
    //                 currentid=data.id;
    //                 console.log(currentid);
    //             }
    //             question = data;
    //             question.msg_extend = resp.msg_extend;
    //             var html = [];
    //             html.push('<div  class="m-a font-mono"><div class="m-b-lg _700" style="font-size: 40px;margin-top: 50px;width: 100%;">');
    //             html.push('<span class="value1"></span><a style="margin: 0 50px;">(?)</a><span class="value2"></span>');
    //             html.push('</div><div class="viewbtn">');
    //             html.push('<button class="md-btn md-fab m-b-sm white _500 answer_btn" name="大于">大于</button>');
    //             html.push('<button class="md-btn md-fab m-b-sm white _500 answer_btn" name="小于">小于</button>');
    //             html.push('</div></div>');
    //             $("#part1_question").html(html.join('')).fadeIn();
    //             var value1Array=[],value2Array=[];
    //             for(var i=0;i<value1.length;i++){
    //                 if(value1[i]!='"'&&value1[i]!=','&&value1[i]!='“'&&value1[i]!=','){
    //                     value1Array.push(value1[i]);
    //                 }
    //             }
    //             for(var i=0;i<value2.length;i++){
    //                 if(value2[i]!='"'&&value2[i]!=','&&value2[i]!='“'&&value2[i]!=','){
    //                     value2Array.push(value2[i])
    //                 }
    //             }
    //             for(var i=0;i<value1Array.length;i++){
    //                 if(value1Array[i]=="*"){
    //                     if(value1Array[i+1]=="*"){
    //                         if(value1Array[i+2]=="2"){
    //                             value1Array.splice(i,3,"&sup2;")
    //                         }else if(value1Array[i+2]=="3"){
    //                             value1Array.splice(i,3,"&sup2;")
    //                         }else if(value1Array[i+3]=="1"){
    //                             if(value1Array[i+3]=="/"){
    //                                 if(value1Array[i+3]=="2"){
    //                                     value1Array.splice(i,5,"<sup>&frac12;</sup>")
    //                                 }
    //                             }
    //                         }
    //                     }
    //                 }else if(value1Array[i]=="3"){
    //                     if(value1Array[i+1]=="."){
    //                         if(value1Array[i+2]=="1"){
    //                             value1Array.splice(i,4,"&pi;")
    //                         }
    //                     }
    //                 }else if(value1Array[i]=="/"){
    //                     if(value1Array[i+1]=="/"){
    //                         if(value1Array[i+2]=="1"){
    //                             value1Array.splice(i,5,"<sup>&frac13;</sup>")
    //                         }else if(value1Array[i+2]=="0.5"){
    //                             value1Array.splice(i,5,"<sup>&frac12;</sup>")
    //                         }
    //                     }
    //                 }
    //             };
    //             for(var key in value1Array){
    //                 $(".value1").append(value1Array[key]);
    //             }
    //             for(var i=0;i<value2Array.length;i++){
    //                 if(value2Array[i]=="*"){
    //                     if(value2Array[i+1]=="*"){
    //                         if(value2Array[i+2]=="2"){
    //                             value2Array.splice(i,3,"&sup2;")
    //                         }else if(value2Array[i+2]=="3"){
    //                             value2Array.splice(i,3,"&sup2;")
    //                         }else if(value2Array[i+3]=="1"){
    //                             if(value2Array[i+3]=="/"){
    //                                 if(value2Array[i+3]=="2"){
    //                                     value2Array.splice(i,5,"<sup>&frac12;</sup>")
    //                                 }
    //                             }
    //                         }
    //                     }
    //                 }else if(value2Array[i]=="3"){
    //                     if(value2Array[i+1]=="."){
    //                         if(value2Array[i+2]=="1"){
    //                             value2Array.splice(i,4,"&pi;")
    //                         }
    //                     }
    //                 }else if(value2Array[i]=="/"){
    //                     if(value2Array[i+1]=="/"){
    //                         if(value2Array[i+2]=="1"){
    //                             value2Array.splice(i,5,"<sup>&frac13;</sup>")
    //                         }else if(value2Array[i+2]=="0.5"){
    //                             value2Array.splice(i,5,"<sup>&frac12;</sup>")
    //                         }
    //                     }
    //                 }
    //             };
    //             for(var key in value2Array){
    //                 $(".value2").append(value2Array[key]);
    //             }
    //         }
    //     });
    }


    function load_question2() {
        $.getJSON(API_HOST + 'toc/topic/logic?id=' + paper_id + '&demo=' + demo_status, function (resp) {
            toastr.clear();
            console.log(resp);
            if (resp.code == 0) {
                var data = resp.data;
                question = data;
                question.msg_extend = resp.msg_extend;
                currentid=data.id;
                console.log(data.premise)
                console.log(data.conclusion)
                var html = [];
                html.push('<div class="m-a font-mono text-lg">');
                html.push('<div class="m-b-lg _500">'+data.premise+','+data.conclusion+'</div>');
                html.push('<div class="viewbtn">');
                html.push('<button class="md-btn md-fab m-b-sm white answer_btn"  name="true">是</button> ');
                html.push('<button class="md-btn md-fab m-b-sm white answer_btn" name="false" >否</button></div></div>');
                $("#part2_question").html(html.join('')).fadeIn();
            }
        });
    }

    function load_question3(){
        var n = random_name[Math.floor(Math.random() * 2)];
            $.getJSON(API_HOST + 'toc/topic/space?id=' + paper_id + '&demo=' + demo_status, function (resp) {
                toastr.clear();
                if(resp.msg =="请求成功"){
                    var data = resp.data;
                    var image_url=IMAGE_HOST+data.image_url;
                    question = data;
                    question.msg_extend = resp.msg_extend;
                    currentid=data.id;
                    var html = [];
                    html.push('<div class="row"><div class="col-lg-7 col-md-7 col-sm-12 col-xs-12 ">');
                    html.push('<img src="'+image_url+'"/>');
                    html.push('</div><div class="col-lg-5 col-md-5 col-sm-12 col-xs-12 ">');
                    html.push('<h2 class="m-b-lg">谁更多?</h2>');
                    html.push('<span class="answer_btn" name="yellow"><button class="btn btn-lg btn-outline text-lg btn-yellow"></button></span>');
                    html.push('<span class="answer_btn" name="blue"><button class="btn btn-lg btn-outline text-lg btn-blue"></button></span>');
                    html.push('</div></div>');
                    $("#part3_question").html(html.join('')).fadeIn();
                }
            });

    }
    var size=18;
    function load_question4() {
        console.log("正式的进来了");
        $.getJSON(API_HOST + 'toc/topic/react?id=' + paper_id + '&demo=' + demo_status+'&size='+size, function (resp) {
            toastr.clear();
            console.log(resp);
            if (resp.code == 0) {
                if(demo_status==1){
                    var data = $.parseJSON(resp.data.description);
                }else{
                    var data = resp.data.description;
                }
                console.log(data);
                question = data;
                question.msg_extend = resp.msg_extend;
                currentid=resp.data.id;
                console.log(currentid);
                var html = [];
                html.push('<div class="row"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 ">');
                html.push('<canvas height="400" width="600" id="mycanvas"></canvas>');
                html.push('</div></div>');
                $("#part4_question").html(html.join('')).fadeIn();
                drawImage(data)
            }
        });
    }

    //创建记忆力模块所需的几个全局变量
    //   demoTest 判断是否是模拟环节    wordArray 新建一组随机单词数组     newWordArray 已出现的数组队列   currentValue  当前选中的单词
    var demoTest=true,wordArray=['disgruntled','overemphasize','illustrate,ambidextrous','illustrate','ambidextrous','ramshackle'],newWordArray=[],currentValue=null;
    function load_question1() {
        if(demoTest){
            $.getJSON(API_HOST + 'toc/topic/memory?id=' + paper_id + '&demo=' + demo_status, function (resp) {
                toastr.clear();
                if (resp.code == 0) {
                    console.log(resp);
                    var data = resp.data;
                    var html = [];
                    var c = data.description;
                    html.push('<div class="m-a font-mono"><div >');
                    html.push('<h1 class="m-b-lg _700">该单词是新出现的还是已经看到过的</h1></div>');
                    html.push('<div class="m-b-lg _700" style="font-size: 40px;margin-top: 50px;">');
                    if(demo_status==1){
                        for(var i=0;i<data.length;i++){
                            newWordArray.push(data[i].word);
                            if(wordArray.indexOf(data[i].word)){
                                wordArray.push(data[i].word);
                            }
                            html.push('<p style="margin:0;">'+data[i].word+'</p>');
                        }
                    }else{
                        currentid=data.id;
                        console.log(currentid);
                        html.push('<p style="margin:0;">'+data.word+'</p>');
                    }
                    html.push('</div><div class="viewbtn">');
                    html.push('<button class="md-btn md-fab m-b-sm white answer_btn" name="seen">SEEN</button>');
                    html.push('<button class="md-btn md-fab m-b-sm white  answer_btn" name="new">NEW</button>');
                    html.push('</div></div>');
                    $("#part1_question").html(html.join('')).fadeIn();
                }
            });
        }else{
            //创建一个随机数
            var randomNum=Math.floor(Math.random() * (wordArray.length-1));
            console.log(randomNum);
            currentValue=wordArray[randomNum];
            console.log(currentValue);
            if(newWordArray.indexOf(currentValue)<0){
                newWordArray.push(currentValue);
            }
            console.log(newWordArray);
            var html = [];
            html.push('<div class="m-a font-mono"><div >');
            html.push('<h1 class="m-b-lg _700">该单词是新出现的还是已经看到过的</h1></div>');
            html.push('<div class="m-b-lg _700" style="font-size: 40px;margin-top: 50px;">');
            html.push('<p style="margin:0;">'+currentValue+'</p>');
            html.push('</div><div class="viewbtn">');
            html.push('<button class="md-btn md-fab m-b-sm white answer_btn" name="seen">SEEN</button>');
            html.push('<button class="md-btn md-fab m-b-sm white  answer_btn" name="new">NEW</button>');
            html.push('</div></div>');
            $("#part1_question").html(html.join('')).fadeIn();
        }
    }
    function load_question6() {
        $.getJSON(API_HOST + 'toc/space?paper=' + paper_id + '&demo=' + demo_status, function (resp) {
            toastr.clear();
            if (resp.code == 0) {
                var data = resp.data;
                question = data;
                question.msg_extend = resp.msg_extend;
                var html = [];
                var c = data.description;
                for (var i in c) {
                    html.push('<div class="label-lte m-a">');
                    $.each(c[i], function (k, v) {
                        html.push('<img src="' + v + '" class="r_img">');
                        html.push('<br>');
                    });
                    html.push('</div>');
                }
                html.push('<h1 class="m-b m-t">');
                html.push('<button class="btn md-btn md-flat m-b-sm w-xs answer_btn">0</button>');
                html.push('<button class="btn md-btn md-flat m-b-sm w-xs answer_btn">1</button>');
                html.push('<button class="btn md-btn md-flat m-b-sm w-xs answer_btn">2</button>');
                html.push('</h1>');
                $("#part6_question").empty().append(html.join('')).fadeIn();
            }
        });
    }

    //插入图片
    var r=0,remove_num=0,imgSrc=null,current_num=0,answerArray=[],valueArray=[];
    function drawImage(data) {
        console.log(data);
        for(var i=0;i<data.length;i++){
            var name=eval(data[i].color+data[i].direction);
            answervalue2Arrayay.push(data[i].color+data[i].direction);
            // console.log(answervalue2Arrayay);
            drawBaseImage(name);
        }
        drawBorder();
    }
    //绘制图片
    var white0=new Image();
    white0.src="../../static/image/candidate/white-0.png";
    var white90=new Image();
    white90.src="../../static/image/candidate/white-90.png";
    var white180=new Image();
    white180.src="../../static/image/candidate/white-180.png";
    var white270=new Image();
    white270.src="../../static/image/candidate/white-270.png";
    var black0=new Image();
    black0.src="../../static/image/candidate/black-0.png";
    var black90=new Image();
    black90.src="../../static/image/candidate/black-90.png";
    var black180=new Image();
    black180.src="../../static/image/candidate/black-180.png";
    var black270=new Image();
    black270.src="../../static/image/candidate/black-270.png";
    //加载箭头
    function drawBaseImage(imgsrc){
        r++;
        var mycanvas=document.getElementById("mycanvas");
        var ctx=mycanvas.getContext("2d");
        if(r<7){
            ctx.drawImage(imgsrc,30+100*(r-1),200);
        }else if(r>=7&&r<13){
            ctx.drawImage(imgsrc,30+100*(r-7),270);
        }else{
            ctx.drawImage(imgsrc,30+100*(r-13),340);
        }
    }

    //绘制border
    function drawBorder() {
        remove_num++;
        var mycanvas=document.getElementById("mycanvas");
        var ctx=mycanvas.getContext("2d");
        ctx.strokeStyle="rgb(170,193,57)";
        ctx.lineWidth=3;
        if(remove_num==1){
            ctx.beginPath();
            ctx.arc(55,225,33,0,2*Math.PI);
            ctx.stroke();
        }else if(remove_num<7){
            console.log(remove_num);
            ctx.clearRect(15+100*(remove_num-2),185,80,80);
            ctx.beginPath();
            ctx.arc(55+100*(remove_num-1),225,33,0,2*Math.PI);
            ctx.stroke();
        }else if(remove_num>=7&&remove_num<13){
            ctx.clearRect(15,185,600,80);
            ctx.clearRect(15+100*(remove_num-8),255,80,80);
            ctx.beginPath();
            ctx.arc(55+100*(remove_num-7),295,33,0,2*Math.PI);
            ctx.stroke();
        }else if(remove_num>=13&&remove_num<19){
            ctx.clearRect(15,255,600,80);
            ctx.clearRect(15+100*(remove_num-14),325,80,80);
            ctx.beginPath();
            ctx.arc(55+100*(remove_num-13),365,33,0,2*Math.PI);
            ctx.stroke();
        }else if(remove_num==19){
            ctx.clearRect(15,325,600,80);
            ctx.beginPath();
            ctx.arc(55+100*6,365,33,0,2*Math.PI);
            ctx.stroke();
            if(demo_status=1){
                var title = part_mapping[2];
                $("#part4_question").hide();
                $("#part4_show_3").fadeIn();
                $("#pape4_promotion").text(title + '-正式').fadeIn();
                question = null;
                demo_status = 0;
            }
            // else{
                // 再次加载新的试题
                // load_func();
            // }
            remove_num=0;answerArray=[];current_num=0;r=0;
        }
    }

    //绘制答对时的动画
    function drawCorrect() {
        console.log(272);
        var mycanvas=document.getElementById("mycanvas");
        var ctx=mycanvas.getContext("2d");
        var img=new Image();
        img.src="../../static/image/candidate/correct.png";
        img.onload=function () {
            ctx.drawImage(img,275,50)
        };
        var timer=setTimeout(function () {
            ctx.clearRect(0,0,600,180);
        },500)

    }
    //绘制答错时的动画
    function drawWrong() {
        console.log(278);
        var mycanvas=document.getElementById("mycanvas");
        var ctx=mycanvas.getContext("2d");
        ctx.clearRect(0,0,600,180);
        var img=new Image();
        img.src="../../static/image/candidate/wrong.png";
        img.onload=function () {
            ctx.drawImage(img,275,50)
        };
        var timer=setTimeout(function () {
            ctx.clearRect(0,0,600,180);
        },500)
    }

    //添加键盘事件
    $(document).bind("keydown",function (e) {
        console.log(327);
        var key = e.which,data;
        switch(key){
            case 37:
                current_num++;deleteImage(37);break;
            case 38:
                current_num++;deleteImage(38);break;
            case 39:
                current_num++;deleteImage(39);break;
            case 40:
                current_num++;deleteImage(40);break;
        }

    });
    //删除图像
    function deleteImage(key) {
        //确定当前答案是否✔️
        var value=answerArray[current_num-1];
        if(value){
            var submitValue=value.slice(5);
        }
        console.log(submitValue);
        if(key==37){
            drawBorder();
            if(demo_status==0){answerArray.push(submitValue)}
            if(value=="white270"||value=="black90"){
                drawCorrect();
            }else{
                drawWrong();
            }
        }else if(key==38){
            drawBorder();
            if(demo_status==0){answerArray.push(submitValue)}

            if(value=="white0"||value=="black180"){
                drawCorrect();
            }else{
                drawWrong();
            }
        }else if(key==39){
            drawBorder();
            if(demo_status==0){answerArray.push(submitValue)}

            if(value=="white90"||value=="black270"){
                drawCorrect();
            }else{
                drawWrong();
            }
        }else{
            drawBorder();
            if(demo_status==0){answerArray.push(submitValue)}
            if(value=="white180"||value=="black0"){
                drawCorrect();
            }else{
                drawWrong();
            }
        }
        console.log(answerArray.join(","));
        if(answerArray.length==18){
            console.log("提交数据一次！！！！！！！！！！！！！！！！！")
            submit_answer(answerArray.join(","),4);
            answerArray=[];
            $("#part4_show_3").hide();
        }
    }



    function bind_paper_show() {
        index = part[part_index];
        // index=2;

        var title = part_mapping[part[part_index]];
        console.log(title);
        var load_func = load_mapping[part[part_index]];

        // var load_func = load_mapping[2];

        $("#part" + index + "_show_1").on('click', function () {
            $(this).hide();
            $("#paper_promotion").text(title + '-演示').fadeIn();
            $("#part" + index + "_demo").fadeIn();
        });

        $("#part" + index + "_show_2").on('click', function () {
            $(this).hide();
            console.log(index);
            $("#part" + index + "_question").fadeIn();
            demo_status = 1;
            try {
                load_func();
            } catch (err) {

            }
        });
        if(index!=4){
            $("#part" + index + "_show_3").on('click', function () {
                $(this).hide();
                demo_status = 0;
                console.log(index+"hehe");
                // start real timer for partX
                toastr.clear();
                set_timer();
                try {
                    load_func();
                } catch (err) {

                }
            });
        }else{
            //反应速度模块     正式开始
            $("#part4_show_3").on('click', function () {
                $(this).hide();
                demo_status = 0;
                valuevalue2Arrayay=[];
                // start real timer for partX
                toastr.clear();
                set_timer();
                try {
                    load_func();
                } catch (err) {

                }
            });

        }


        //





        // $("#part" + index + "_demo").on('click', '.demo_div', function () {
        //     console.log(270);
        //     var div = $(this);
        //     //反应模块点击进入模拟阶段
        //     console.log(index);
        //     if(index==4){
        //         $("#part" + index + "_demo").hide();
        //         $("#paper_promotion").text(title + '-模拟').fadeIn();
        //         $("#part" + index + "_show_2").fadeIn();
        //     }else{
        //         $(div.hide().next()[0]).fadeIn();
        //     }
        // });

        $("#part" + index + "_demo").on('click', 'span', function () {
            console.log(277);
            if ($(this).children().attr('data-next')) {
                console.log(280);
                $("#part" + index + "_demo").hide();
                $("#paper_promotion").text(title + '-模拟').fadeIn();
                $("#part" + index + "_show_2").fadeIn();
            }
        });

        $("#part" + index + "_question").on('click', '.part1_desc', function () {
            $(this).hide();
            $("#part" + index + "_question_body").fadeIn();
        });

        $("#part" + index + "_question").on('click', '.answer_btn', function () {
            var btn = $(this);
            btn.removeClass('answer_btn').prop('disabled', true);
            var answer = btn.attr("name");
            console.log(answer);
            if (null != demo_status && demo_status == 1) {
                // demo
                if (check_answer(answer)){
                    demo_count++;
                }
                if (demo_count >= demo_correct_count) {
                    // end demo status
                    console.log(312);
                    demoTest=true;
                    $("#part" + index + "_question").hide();
                    $("#part" + index + "_show_3").fadeIn();
                    $("#paper_promotion").text(title + '-正式').fadeIn();
                    question = null;
                    demo_status = 0;
                } else {
                    try {
                        load_func();
                    } catch (err) {

                    }
                }
            } else {
                // real
                console.log("正式提交代码："+327);
                submit_question(answer, index)
            }
        });
    }

    function check_answer(answer) {
        //记忆力模块单词出现次数的判断；
        if(index==1){
            demoTest=false;
            if(demo_count==0){
                toastr.success('恭喜，答对了！');
                return true;
            }else{
                if(newWordArray.indexOf(currentValue)&&answer=="seen"){
                    toastr.success('恭喜，答对了！');
                    return true;
                }else{
                    toastr.warning('抱歉，答错了！');
                    return false;
                }
            }
        }else{
            if (answer.toString() == question.msg_extend.toString()) {
                toastr.success('恭喜，答对了！');
                return true;
            }
            toastr.warning('抱歉，答错了！');
            return false;
        }

    }

    //反应模块提交答案
    function submit_answer(answer, index) {
        console.log("这么快就提交数据了？"+current_num);
        console.log(answer);
        console.log(index);
        console.log(currentid);
        var load_func = load_mapping[index];
            $.ajax({
                type: 'POST',
                async: false,
                url: API_HOST + 'toc/topicspace',
                data: {
                    answer: answer,
                    id:currentid
                },
                error: function () {
                    question = null;
                    load_func();
                }
            }).done(function (resp) {
                load_func();
            });
    }


    function submit_question(answer, index) {
        console.log("这么快就提交数据了？")
        console.log(answer);
        console.log(index);
        console.log(currentid);
        switch (index){
            case 1:
                currenturl=API_HOST + 'toc/topic/number';break;
            case 2:
                currenturl=API_HOST + 'toc/topic/logic';break;
            case 3:
                currenturl=API_HOST + 'toc/topic/space';break;
            case 4:
                currenturl=API_HOST + 'toc/topic/react';break;
            case 5:
                currenturl=API_HOST + 'toc/topic/memory';break;
            case 6:
                currenturl=API_HOST + 'toc/topic/space';break;
        }
        var load_func = load_mapping[index];
            if(demo_status==0){
                $.ajax({
                    type: 'POST',
                    async: false,
                    url:currenturl,
                    data: {
                        answer: answer,
                        id:currentid
                    },
                    error: function () {
                        question = null;
                        console.log("报错进来了");
                        load_func();
                    }
                }).done(function (resp) {
                    console.log("数据提交成功！！！");
                    try {
                        load_func();
                    } catch (err) {
                        question = null;
                    }
                });
            }
    }

    function next_part() {
        try {
            $("#paper_promotion").fadeOut();
            $("#part_" + part[part_index - 1]).remove();
            $("#part_" + part[part_index]).fadeIn();
            if (part_index >= (part.length - 1)) {
                $.ajax({
                    type: 'POST',
                    url: API_HOST + 'toc/' + paper_id,
                }).done(function (resp) {
                    // set button
                    if (extend_flag) {
                        var flag = false;
                        if (resp.code == 0) {
                            var data = resp.data;
                            var extend = data.extend;
                            flag = data.extend_flag;
                            function sortNumber(a, b) {
                                return a - b
                            }

                            var rank = [];
                            var tmp = {};
                            for (var i in extend){
                                var d = extend[i];
                                d.part = i;
                                rank.push(d.rank);
                                tmp[d.rank] = d;
                            }
                            rank = rank.sort(sortNumber);
                            if (rank.length > 0) {
                                data.part1 = part_mapping[parseInt(tmp[rank[rank.length - 1]].part)];
                                data.part2 = part_mapping[parseInt(tmp[rank[0]].part)];
                                $.each($(".auto_fill"), function () {
                                    var s = $(this);
                                    s.text(data[s.attr('data-id')]);
                                });
                            }
                        }
                        var btn = $("#back_btn");
                        // if pass
                        if (flag) {
                            $(".go-next").removeClass('hide');
                            btn.text('通关密码');
                            btn.on('click', function () {
                                get_extend();
                            });
                        } else {
                            $(".no-pass").removeClass('hide');
                            btn.text('返回');
                            btn.on('click', function () {
                                window.location.href = "/view/candidate/paper.html";
                            });
                        }
                        btn.removeClass('hide');
                    } else {
                        $("#back_btn").on('click', function () {
                            window.location.href = "/view/candidate/paper.html";
                        });
                    }
                });
                return;
            }
            demo_count = 0;
            bind_paper_show();
            start_part();
        } catch (err) {
        }
    }

    function clock() {
        window.clearInterval(timer_id);
        part_index++;
        next_part();
    }

    function set_timer() {
        // console.log(part_timer[part_index + 1]);
        timer_id = window.setInterval(function () {
            clock();
        }, MyUtils.get_value(part_timer[part_index + 1], part_timer_default));
    }

    function bind_extend(){
        $("#extend_ul select.select_textarea").on('change', function () {
            var dom = $(this);
            var text = dom.siblings('textarea');
            text.attr('placeholder', dom.val());
            text.focus();
        });
    }

    function get_extend() {
        $.ajax({
            type: 'GET',
            url: API_HOST + 'toc/extend?paper=' + paper_id,
            statusCode: {
                400: function (resp) {
                    $.pjax({
                        url: '/view/candidate/paper.html',
                        container: '#view',
                        fragment: '#view'
                    });
                }
            }
        }).done(function (resp) {
            set_extend(resp.data);
            $("#part_6").fadeOut();
            $("#part_extend").fadeIn();
            $('#timer').startTimer({
                onComplete: function (element) {
                    element.addClass('is-complete');
                    submit_extend();
                }
            });
            $("#timer_div").removeClass('hide');
        });
    }

    function set_extend(data) {
        var extend_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D'};
        var ul = $("#extend_ul");
        for (var i in data) {
            var d = data[i];
            var index = parseInt(i) + 1;
            var html = [];
            var type = d.topic.description.type;
            html.push('<li class="list-item">');
            html.push('<div class="list-body" id="radio_div_' + index + '">');
            html.push('<div class="text p-b-xs">' + index + '. ' + d.topic.description.desc + '</div>');
            var option = d.topic.description.option;
            if (type == 'radio') {
                if (option && option.length > 0) {
                    $.each(option, function (k, v) {
                        html.push('<div class="p-t-xs">');
                        html.push('<label class="md-check p-r-lg">');
                        html.push('<input type="radio" value="' + extend_mapping[k] + '" name="radio_' + d['id'] + '">');
                        html.push('<i class="blue"></i>');
                        html.push(extend_mapping[k] + '. ' + v);
                        html.push('</label>');
                        html.push('</div>');
                    });
                }
            } else if (type == "select_text") {
                html.push('<div class="text p-t-xs">');
                html.push('<select class="form-control c-select select_textarea" name="select_' + d['id'] + '" required>');
                if (option && option.length > 0) {
                    $.each(option, function (k, v) {
                        html.push('<option value="' + v + '">' + v + '</option>');
                    });
                }
                html.push('</select>');
                html.push('<textarea name="textarea_' + d['id'] + '" class="form-control m-t-sm select_textarea" required  maxlength="5120" placeholder="高考之前需要学习12年，你觉得是不是太长了？" rows="10"></textarea>');
                html.push('</div>');
            }
            html.push('</div>');
            html.push('</div>');
            html.push('</li>');
            ul.append(html.join(''));
        }
        bind_extend();
        var form = $('#extend_form');
        form.parsley().on('form:submit', function () {
            $("#confirm_modal").modal('show');
            return false;
        });

        $("#confirm_btn").on('click', function () {
            $("#confirm_modal").modal('hide');
            submit_extend();
        });
    }

    function submit_extend() {
        $("#submit_btn").prop('disabled', true);
        $("#timer_div").hide();
        var form = $('#extend_form');
        var data = form.serializevalue2Arrayay();
        var answer = {};
        for (var i in data) {
            var d = data[i];
            var name = d.name;
            name = name.split('_')[1];
            var t = answer[name] || [];
            t.push(d.value);
            answer[name] = t;
        }
        $.ajax({
            type: 'POST',
            url: API_HOST + 'toc/extend',
            data: {answer: JSON.stringify(answer), paper: paper_id},
        }).done(function (resp) {
            $("#submit_btn").prop('disabled', false);
            $("#part_extend").fadeOut();
            $("#part_finally").fadeIn();
        });
    }

};





