//const WebSocket = require('ws');
const websocket = new WebSocket('ws://localhost:6789');

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
        var mes = JSON.stringify({action:'ping'});
        websocket.send(mes);
        keepAlive = setTimeout(function () {

           /// ---connection closed ///


    }, 3000);
}

websocket.onopen = () => {
    setInterval(ping, 30000);
    console.log('connecting to server...');
};
websocket.onerror = error => {
    console.log(`WebSocket error: ${error}`)
};

websocket.onclose = () => {
    clearTimeout(this.pingTimeout);
    //console.log("exiting");
    //alert('closing');
};

function send_msg(msg, onsuccess , onfailure)
{

    try {
        websocket.onmessage = function (event) {

            data = JSON.parse(event.data);
            //console.log("bbbbbbbbbbbbbbbb " + data);
            switch (data.action) {
                case 'pong':
                     var mes = JSON.stringify({action:'ping'});
                     clearTimeout(keepAlive);
                     setTimeout(() => websocket.send(mes), 3 * 1000);
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

        console.info("try to send ....");
        var json = JSON.stringify(msg);
        console.log(json);
        websocket.send(json);
        //websocket = new WebSocket("ws://10.100.102.5:6789");
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