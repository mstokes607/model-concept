function validate() {   
    var val = document.getElementsByClassName("inputs")
    var msg = document.getElementById("message1");
    var msg2 = document.getElementById("message2");
    var num = [];
    var OK = [];
    //pattern to detect decimal entry 
    var patt = /^\d*\.?\d*$/;
    var i;
    //vars to count number of good inputs
    var noerrcnt = 0;
    var noerrcnt2 = 0;
    for (i = 0; i < val.length; i++) {
        num[i] = parseFloat(val[i].value);
        OK[i] = patt.exec(val[i].value); 
      //   alert(OK);
        if (val[i].value == "" | OK[i] == null ) {
            val[i].style.border = "1px solid red";
            //val[i].focus();
            val[i].style.backgroundColor = "#FBB0B0";
            msg.style.color = "red";
            }
            // isNaN(num[i])
        else if (num[i] > 1 | num[i] <= 0) {
            val[i].style.border = "1px solid red";
            //val[i].focus();
            val[i].style.backgroundColor = "#FBB0B0";
            val[i].style.border = "1px solid red";
            msg.style.color = "red";
        }
        else if (num[i] <= 1 & num[i] > 0) {
            noerrcnt += 1;
            val[i].style.backgroundColor = "white";
            val[i].style.border = "1px solid #e6e6e6";
            //when all of the inputted data are good; 
            if (noerrcnt == 13) {
                 msg.style.color = "black";
            }
        }
    }
    //validation for cost inputs
    var cst = document.getElementsByClassName("inpt_cost");
    var cst_num = [];
    var i; 
    for (i = 0; i < cst.length; i++) {
        cst_num[i] = parseFloat(cst[i].value);
    
        if (cst[i].value == "") {
            cst[i].style.border = "1px solid red";
            //cst[i].focus();
            cst[i].style.backgroundColor = "#FBB0B0";
            cst[i].style.border = "1px solid red";
            msg2.style.color = "red";
        }
        else if (cst_num[i] < 0 | isNaN(cst_num[i]) ) {
            cst[i].style.border = "1px solid red";
            //cst[i].focus();
            cst[i].style.backgroundColor = "#FBB0B0";
            cst[i].style.border = "1px solid red";
            msg2.style.color = "red";
        }
        else if (cst_num[i] >= 0) {
            noerrcnt2 += 1;
            cst[i].style.backgroundColor = "white";
            cst[i].style.border = "1px solid #e6e6e6";
            //when all of the inputted data are good; 
            if (noerrcnt2 == 4) {
                 msg2.style.color = "black";
            }
        }
        
    }
    //alert(noerrcnt2);
}

validate();
