/**
 * Created by higgstech on 16/10/28.
 */
// create by xjx  2016年10月28日17:23:46
    // 获取当前时间
    function isLeap(year) {
        return year % 4 == 0 ? (year % 100 != 0 ? 1 : (year % 400 == 0 ? 1 : 0)) : 0;
    }
    var i, k,weekly,monthly,
        today = new Date(),                 //获取当前日期
        y = today.getFullYear(),            //获取日期中的年份
        m = today.getMonth(),               //获取日期中的月份(需要注意的是：月份是从0开始计算，获取的值比正常月份的值少1)
        d = today.getDate(),                //获取日期中的日(方便在建立日期表格时高亮显示当天)
        week=today.getDay(),changeM=m,changeY=y,
        weekArray=["周日","周一","周二","周三","周四","周五","周六"],
        monthArray=["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"];
        weekly=weekArray[week];monthly=monthArray[m];
        if(d<10){d="0"+d}
        $(".content-right h5").html(y+"年"+(m+1)+"月"+d+" "+weekly);
        $(".tool-f span").html(monthly+" "+y);

    getMonthDate(y+""+((changeM+1)<10?"0"+(changeM+1):(changeM+1)));

    // 默认获取当天打卡信息
    $.ajax({
        type:"GET",
        url: API_HOST+'attendance/detail',
        data: {
            date:y+"-"+(m+1)+"-"+d
        },
        success:function (date) {
            var detailDate=date.data;
            console.log("获取当天的成功的数据为："+date);
            if(detailDate.checkin){
                $("#checkin").attr("disabled","disabled");
            }
            dealDate(detailDate);
        },
        error:function (date){
            $("#checkinbtn").removeAttr("disabled");
            $(".checkinfo>input").show();
        }
    });



    //查询某一天的页面信息
    function checkcurrentTime(changeY,changeM,day) {
        console.log("当前日期为：");
        console.log(changeY+"+"+(changeM+1)+"+"+day);
        if(changeY>y||(changeY==y&&changeM>m)||(changeY==y&&changeM==m&&day>d)){
            setEmpty()
        }else{
            $.ajax({
                type:"GET",
                url: API_HOST+'attendance/detail',
                data: {
                    date:changeY+"-"+(changeM+1)+"-"+day
                },
                success:function (date){
                    var detailDate=date.data;
                    console.log("获取成功的数据为：");
                    console.log(date);
                    if(detailDate.checkin){
                        $("#checkin").attr("disabled","disabled");
                    }
                    dealDate(detailDate);
                },
                error:function (date) {
                    console.log("获取数据失败");
                    dealDate(date.statusText);
                }

            });

        }
    }

    // 单击查看指定日期签到详情
    $(document).on("click",".tableList1 tbody  td",function () {
        // $(this).css("background","#f0f0f0").siblings().css("background","none");
        // var day=$(this).children().html();
        var day=$(this).children().html();
        if(changeY>y||((changeY==y)&&(changeM>m))||((changeY==y)&&(changeM==m)&&day>d)){
            setEmpty()
        }
        if(day<10){day="0"+day};
        var dt = new Date(changeY, changeM, day);
        var detail=weekArray[dt.getDay()];
        console.log(detail);
        $(".content-right h5").html(changeY+"年"+(changeM+1)+"月"+day+" "+detail);
        checkcurrentTime(changeY,changeM,day);
    });

    //设置当日详情信息为空;
    function setEmpty() {
        $("#checkinTime").html(" ");
        $("#checkoutTime").html(" ");
        $(".checkinfo>p").html(" ");
        $("#totalTime").html(" ");
    }

    //添加某年某月份的动态数据
    function getMonthDate(dateTime) {
        console.log(dateTime);
        $.ajax({
            type:"GET",
            url: API_HOST+'attendance',
            data: {
                month:dateTime
            },
            success:function (date){
                var detailDate=date.data;
                console.log(detailDate);
                addDateToWeb(detailDate);
            },
            error:function (date) {
                console.log("获取数据失败");
                // dealDate(date.statusText);
                setEmpty();
            }
        })
    }


    function addDateToWeb(detailDate) {
        // 确定正常考勤和迟到早退的次数    dayNum   normalNum
        var dayNum=detailDate.length,normalNum=0,righticon="<i class='material-icons md-24'>&#xe5ca;</i>",flowericon='<i class="material-icons md-24 ">&#xe545;</i>';
        console.log(dayNum);
        for(var i=0;i<detailDate.length;i++){
            var checkin1=detailDate[i].checkin;
            var checkinNote=detailDate[i].checkin_note;
            var checkout1=detailDate[i].checkout;
            var checkout1Note=detailDate[i].checkout_note;
            var date=Number(detailDate[i].date.slice(-2));
            var totalTime=detailDate[i].duration;
            if(checkout1){
                var checkoutTimeH=checkout1.slice(0,2);
            }
            if(checkin1){
                var checkinTimeH=checkin1.slice(0,2);
                var checkinTimeM=checkin1.slice(3,5);
            }
            // 将后台的数据反馈到列表内
            var tableList1=$(".tableList1 .currentList_"+date);
            var tableList2=$(".tableList2 .list_"+date);
            if (checkinTimeH>=13||checkoutTimeH<=12){
                totalTime_note=parseInt(totalTime/60)+"小时"+totalTime%60+"分";
                if(totalTime/60<8){
                    tableList2.next().next().next().css("color","red");
                    tableList1.addClass("unnormal")
                }else{normalNum++}
            }else{
                totalTime_note=parseInt(totalTime/60-1)+"小时"+totalTime%60+"分";
                if((totalTime/60-1)<8){
                    tableList2.next().next().next().css("color","red");
                }else{
                    normalNum++;
                    tableList1.addClass("normal")
                }
            }
            if(checkinTimeH>"09"&&checkinTimeM>="10"){
                tableList2.next().css("color","red")
            }
            if(checkoutTimeH<"18"){
                tableList2.next().next().css("color","red")
            }
            //列表中确定周末加班  添加小红花样式
            var weekend=tableList2.text();
            if(weekend.indexOf("六")>=0||weekend.indexOf("日")>=0){
                tableList2.append(flowericon);
            }
            //日历上确定周末是否加班   添加小红花样式
            var dt = new Date(changeY, changeM, date);
            var detail=weekArray[dt.getDay()];
            if(detail=="周六"||detail=="周日"){
                tableList1.append(flowericon);
            }
            // else{
            //     //确定日历页面上打卡数据是否正常
            //     if((checkinTimeH>"09"&&checkinTimeM>="10")||checkoutTimeH<"18"){
            //         tableList1.addClass("unnormal")
            //     }else{
            //         tableList1.addClass("normal")
            //     }
            // }

            if(checkinNote||checkout1Note){
                tableList2.next().next().next().next().append(righticon);
                tableList1.parent().append("<i></i>");
            }
            tableList2.next().html(checkin1).next().html(checkout1).next().html(totalTime_note);

            $("#normalDays").html(normalNum);
            $("#unnormalDays").html(dayNum-normalNum);
        }
    }



    // 处理页面反馈的数据
    function  dealDate(detailDate) {
        console.log("正在处理数据是：");
        console.log(detailDate);
        if(detailDate=="Not Found"){
            setEmpty();
        }else{
            $("#checkinbtn").attr("disabled","disabled");
            var checkin=detailDate.checkin.slice(0,5);
            var checkin_note=detailDate.checkin_note;
            var checkout_note=detailDate.checkout_note;
            if(checkin_note){
                $("#checkinNote+p").html(checkin_note).show();
            }else{
                $("#checkinNote").show();
            }
            if(checkout_note){
                $("#checkoutNote+p").html(checkin_note).show().siblings().hide();
            }else{
                $("#checkoutNote").show();
            }
            $("#checkinTime").html(checkin);
            if(detailDate.checkout){
                var checkout=detailDate.checkout.slice(0,5);
                if(checkout_note){
                    $("#checkoutNote+p").html(checkout_note).show();
                }else{
                    $("#checkoutNote").show();
                }
                var totalTime=detailDate.duration;

                var checkinTime=detailDate.checkin.slice(0,2);
                if(detailDate.checkout) {
                    var checkoutTime = detailDate.checkout.slice(0, 2);
                }
                if (checkinTime>=13||checkoutTime<=12){
                    totalTime_note=parseInt(totalTime/60)+"小时"+totalTime%60+"分";
                }else{
                    totalTime_note=parseInt(totalTime/60-1)+"小时"+totalTime%60+"分";
                }
                $("#checkoutTime").html(checkout);
                $("#totalTime").html(totalTime_note);
            }
        }
    }


    // 更新页面日历信息
    function updateCalendar(y,m,d){
        var tableTbodyNote=$(".tableList1 table tbody");
        var tableTbodyList=$(".tableList2 table tbody");
        tableTbodyNote.html(" ");
        tableTbodyList.html(" ");
        //更新日历
        var firstday = new Date(y, m, 1);            //获取当月的第一天
        var dayOfWeek = firstday.getDay();          //判断第一天是星期几(返回[0-6]中的一个，0代表星期天，1代表星期一，以此类推)
        var days_per_month = new Array(31,28+isLeap(y),31,30,31,30,31,31,30,31,30,31);
        var num=dayOfWeek-1;
        var str_nums = Math.ceil((dayOfWeek + days_per_month[m]) / 7);                        //确定日期表格所需的行数
        var frag='',fragList="";
        for (i = 0; i < str_nums; i++){         //二维数组创建日期表格
            frag+="<tr>";
            for (k = 0; k < 7; k++) {
                var idx = 7 * i + k;             //为每个表格创建索引,从0开始
                var date = idx - dayOfWeek + 1;  //将当月的1号与星期进行匹配
                (date <= 0 || date > days_per_month[m]) ? date = ' ': date = idx - dayOfWeek + 1;  //索引小于等于0或者大于月份最大值就用空表格代替
                date == d ? frag+='<td><span class="current currentList_'+date+'">' + date + '</span></td>' : frag+='<td><span class="currentList_'+date+'">' + date + '</span></td>';  //高亮显示当天
            }
            frag+="</tr>";
        }
        tableTbodyNote.append(frag);
        //更新列表
        var strList_num=days_per_month[m];
        for(var j=1;j<=strList_num;j++){
            var weekNum=upWeekNum();
            fragList+="<tr>";
            if(j==Number(d)){
                fragList+="<td class='list_"+j+"'><span class='current'>"+j+"</span>"+weekNum+"</td>";
            }else{
                fragList+="<td class='list_"+j+"'><span>"+j+"</span>"+weekNum+"</td>";
            }
            fragList+="<td>--</td>";
            fragList+="<td>--</td>";
            fragList+="<td>--</td>";
            fragList+="<td></td>";
            fragList+="</tr>";
        }
        tableTbodyList.append(fragList);
        function upWeekNum() {
                num++;
            if(num>6){num=0}
            weekArray=["周日","周一","周二","周三","周四","周五","周六"];
            return (weekArray[num]);
        }
    }
    updateCalendar(y,m,d);


    // 上班签到
    $("#checkinbtn").click(function () {
        $.ajax({
            type: 'POST',
            url: '/attendance',
            data: {
                signin:true
            },
            success:function (date) {
                $(this).attr("disabled","disabled");
                var dateT=$.parseJSON(date);
                console.log(dateT);
                if(dateT.date.checkin){
                    var currentTime=dateT.date.checkin.slice(0,5);
                }
                console.log(currentTime);
                $("#checkinTime").html(currentTime);
            },
            error:function (date) {
                setEmpty();
            }
        })
    });
    // 添加备注信息
    $(".checkinfo input").bind("keydown",function (e) {
        var key = e.which,data;
        var value=$(this).val();
        if (key == 13) {
            $(this).hide().next().show().html(value);
            if($(this).attr("id")=="checkinNote"){
                $("#checkinNote").next().html(value);
                data={"checkin_note":value}
            }else{
                $("#checkoutNote").next().html(value);
                data={"checkout_note":value}
            }
            $.ajax({
                type: 'POST',
                url: '/attendance',
                data:data,
                success:function (date) {
                    console.log("已成功提交备注信息");
                    console.log(date)
                }
            })
        }
    });
    // 下班签退
    $("#checkoutbtn").click(function () {
        $.ajax({
            type: 'POST',
            url: '/attendance',
            data: {
                signin:false
            },
            success:function (date) {
                var totalTime_note;
                var dateT=$.parseJSON(date);
                var currentTime=dateT.data.checkout.slice(0,5);
                $("#checkoutTime").html(currentTime);
                if(!dateT.data.checkin){
                    $("checkin").attr("disabled","disabled");
                }
                var totalTime=dateT.data.duration;
                var checkinTime=dateT.data.checkin.slice(0,2);
                var checkoutTime=dateT.data.checkout.slice(0,2);
                if (checkinTime>=13||checkoutTime<=12){
                    totalTime_note=parseInt(totalTime/60)+"小时"+totalTime%60+"分";
                }else{
                    totalTime_note=parseInt(totalTime/60-1)+"小时"+totalTime%60+"分";
                }
                $("#totalTime").html(totalTime_note);
            }
        })
    });


    // 切换到上一个月
    $("#prevMonth").click(function () {
        changeM--;
        var changeNewM=changeM+1;
        if(changeM<0){changeM=11;changeY--;}
        if(changeNewM<1){changeNewM=12;}
        if(changeNewM<10){changeNewM="0"+changeNewM};
        getMonthDate(changeY+""+changeNewM);
        $(".tool-f span").html(monthArray[changeM]+" "+changeY);
        if(changeM==m&&changeY==y){
            updateCalendar(changeY,changeM,d)
        }else{
            updateCalendar(changeY,changeM,32)
        }
    });


    // 切换到下一个月
    $("#nextMonth").click(function () {
        changeM++;
        if(changeM>11){
            changeM=0;
            changeY++;
        }
        var changeNewM=changeM+1;
        if(changeNewM>12){changeNewM=1;}
        if(changeNewM<10){changeNewM="0"+changeNewM};
        getMonthDate(changeY+""+changeNewM);

        $(".tool-f span").html(monthArray[changeM]+" "+changeY);
        if(changeM==m&&changeY==y){
            updateCalendar(changeY,changeM,d)
        }else{
            updateCalendar(changeY,changeM,32)
        }
    });

    // 切换日志和列表页面
    $("#type").change(function () {
        var value=$(this).val();
        if(value=="列表"){
            $(".tableList2").show().prev().hide();
        }else{
            $(".tableList1").show().next().hide();
        }
    });



