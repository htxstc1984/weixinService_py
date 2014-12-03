/**
 * Created by hu on 2014/12/3.
 */
function dateFormat(date){
    return date.formatDate("yyyy-MM-dd hh:mm:ss");
}

//把时间格式字符串转化为时间
//如下格式
//2006
//2006-01
//2006-01-01
//2006-01-01 12
//2006-01-01 12:12
//2006-01-01 12:12:12
function parseDate(dateStr) {
    var regexDT = /(\d{4})-?(\d{2})?-?(\d{2})?\s?(\d{2})?:?(\d{2})?:?(\d{2})?/g;
    var matchs = regexDT.exec(dateStr);
    var date = new Array();
    for (var i = 1; i < matchs.length; i++) {
        if (matchs[i] != undefined) {
            date[i] = matchs[i];
        } else {
            if (i <= 3) {
                date[i] = '01';
            } else {
                date[i] = '00';
            }
        }
    }
    return new Date(date[1], date[2] - 1, date[3], date[4], date[5], date[6]);
}

//为date类添加一个format方法
//yyyy 年
//MM 月
//dd 日
//hh 小时
//mm 分
//ss 秒
//qq 季度
//S  毫秒
Date.prototype.formatDate = function (format) //author: meizz
{
    var o = {
        "M+": this.getMonth() + 1, //month
        "d+": this.getDate(),    //day
        "h+": this.getHours(),   //hour
        "m+": this.getMinutes(), //minute
        "s+": this.getSeconds(), //second
        "q+": Math.floor((this.getMonth() + 3) / 3),  //quarter
        "S": this.getMilliseconds() //millisecond
    }
    if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
        (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o) if (new RegExp("(" + k + ")").test(format))
        format = format.replace(RegExp.$1,
            RegExp.$1.length == 1 ? o[k] :
                ("00" + o[k]).substr(("" + o[k]).length));
    return format;
}