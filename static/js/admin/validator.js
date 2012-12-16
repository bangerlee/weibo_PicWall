;
(function($) {
    $.fn.extend({
        getLength:function(){
            var sType = $(this).attr("type");
            var len = 0;
            switch(sType)
            {
                case "text":
                case "hidden":
                case "password":
                case "textarea":
                case "file":
                    var val = $(this).val();
                    len = val.length;
                    break;
                case "checkbox":
                case "radio":
                    len = $("input[type='"+sType+"'][name='"+$(this).attr("name")+"']:checked").length;
                    break;
                case "select-one":
                    len = $(this).options ? $(this).options.selectedIndex : -1;
                    break;
                case "select-multiple":
                    len = $("select[name="+$(this).attr("name")+"] option:selected").length;
                    break;
            }
            return len;
         }
    });

    $.fn.extend({
        isEmpty:function(){
            var sType = $(this).attr("type");
            return ($(this).empty && $(this).getLength()==0);
         }
    });

    $.fn.extend({
        isEmail:function(){
            return /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test($(this).val());
        }
    });

    $.fn.extend({
        isCardNo: function(){
            var C15ToC18 = function(c15) {
                var cId=c15.substring(0,6)+"19"+c15.substring(6,15);
                var strJiaoYan = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"];
                var intQuan =[7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
                var intTemp=0;
                for(i = 0; i < cId.length ; i++)
                intTemp +=  cId.substring(i, i + 1)  * intQuan[i];
                intTemp %= 11;
                cId+=strJiaoYan[intTemp];
                return cId;
            };

            var Is18IDCard=function(IDNum) {
                var aCity={11:"北京",12:"天津",13:"河北",14:"山西",15:"内蒙古",21:"辽宁",22:"吉林",23:"黑龙江",31:"上海",32:"江苏",33:"浙江",34:"安徽",35:"福建",36:"江西",37:"山东",41:"河南",42:"湖北",43:"湖南",44:"广东",45:"广西",46:"海南",50:"重庆",51:"四川",52:"贵州",53:"云南",54:"西藏",61:"陕西",62:"甘肃",63:"青海",64:"宁夏",65:"新疆",71:"台湾",81:"香港",82:"澳门",91:"国外"};

                var iSum=0,info="",sID=IDNum;
                if(!/^\d{17}(\d|x)$/i.test(sID)) {
                    return false;
                }
                sID=sID.replace(/x$/i,"a");

                if(aCity[parseInt(sID.substr(0, 2))]==null) {
                    return false;
                }

                var sBirthday=sID.substr(6,4)+"-"+Number(sID.substr(10,2))+"-"+Number(sID.substr(12,2));
                var d=new Date(sBirthday.replace(/-/g,"/"));

                if(sBirthday!=(d.getFullYear()+"-"+ (d.getMonth()+1) + "-" + d.getDate()))return false;

                for(var i=17; i>=0; i--) {
                    iSum += (Math.pow(2, i) % 11) * parseInt(sID.charAt(17 - i), 11);
                }

                if(iSum%11!=1) {
                    return false;
                }

                return true;
            };

            return this.val().length==15 ? Is18IDCard(C15ToC18(this.val())) : Is18IDCard(this.val());
        }
    });
})(jQuery);
