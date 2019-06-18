//const WebSocket = require('ws');
var websocket =undefined;

function read_cookie(key)
{
    var b = document.cookie.match('(^|[^;]+)\\s*' + key + '\\s*=\\s*([^;]+)');
    return b ? b.pop() : '';
}

function getwebsocket() {
    if(this.websocket == undefined || websocket.readyState == 3)
        this.websocket = new WebSocket('ws://localhost:6789');
    return this.websocket;
}

function noop() {}
var keepAlive = true
function heartbeat() {
  clearTimeout(this.pingTimeout);

  // Use `WebSocket#terminate()` and not `WebSocket#close()`. Delay should be
  // equal to the interval at which your server sends out pings plus a
  // conservative assumption of the latency.
  this.pingTimeout = setTimeout(() => {
    //this.terminate();
  }, 30000 + 1000);
}
function ping() {
        var ws = getwebsocket();
        var mes = JSON.stringify({action:'ping',username:read_cookie('username')});
        if (ws.readyState == WebSocket.OPEN){
            WebSocket.CLOSING;
            WebSocket.CONNECTING;
            ws.send(mes);
            keepAlive = setTimeout(function () {

           /// ---connection closed ///


    }, 6000);
            }

}

getwebsocket().onclose = () => {
    clearTimeout(this.pingTimeout);
    //console.log("exiting");
    //alert('closing');
};

function send_msg(msg, onsuccess , onfailure,onerror)
{

    try {
        var ws = getwebsocket();
        if(onerror!=undefined)
            ws.onerror = onerror;
        ws.onmessage = function (event) {

            data = JSON.parse(event.data);
            //console.log("bbbbbbbbbbbbbbbb " + data);
            switch (data.action) {
                case 'pong':
                     var mes = JSON.stringify({action:'ping',username:read_cookie('username')});
                     //setInterval(ping, 6000);
                     break;
                case 'notify' :
                    print('got it')
                    alert('notify')
                    $(document).ready(function() {
                     $("#notify").fadeIn(1000).show();
                    });
                    break;
                case 'success':
                    console.log('success');
                    onsuccess(data.message,data.return_val);
                    break;
                case 'fail':
                    console.log('fail');
                    onfailure(data.message);
                    break;
                default:
                    console.log(
                        "unsupported event", data);
            }

        };

        getwebsocket().onopen = () => {
        //setInterval(ping, 6000);
        console.log('connecting to server...');
            var json = JSON.stringify(msg);
            console.log(json);
            ws.send(json);
        };
        if(ws.readyState == WebSocket.OPEN) {
            console.info("try to send ....");
            var json = JSON.stringify(msg);
            console.log(json);
            ws.send(json);
            //setInterval(ping, 6000);
        }

    }catch (e) {
        console.log(e);
    }
}

function read(key)
{
    var b = document.cookie.match('(^|[^;]+)\\s*' + key + '\\s*=\\s*([^;]+)');
    return b ? b.pop() : '';
}

function write(key,val)
{
    document.cookie = key+' = '+val+'; path=/;';
}