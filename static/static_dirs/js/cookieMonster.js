
function read_cookie(key)
{
    var b = document.cookie.match('(^|[^;]+)\\s*' + key + '\\s*=\\s*([^;]+)');
    return b ? b.pop() : '';
}

function write_cookie(key,val)
{
    document.cookie = key+' = '+val+'; path=/;';
}


function checkExpire() {
    var current = read_cookie("expire");
    if(current==''){
        document.cookie='';
        return;
    }
    else {

        var now = new Date();
        var time = now.getTime();
        var extime = Number(current);
        if(time>extime){
            document.cookie='';
            var expireTime = time + 1000 * 36000;
        //now.setTime(expireTime);
        //var tempExp = 'Wed, 31 Oct 2012 08:50:17 GMT';
        document.cookie = 'expires=' + time+';';
        }
        return ;

    }
  //console.log(document.cookie);
}