//const WebSocket = require('ws');

function send_msg(msg, onsuccess , onfailure)
{

    try {
        websocket = new WebSocket("ws://1132.73.211.37:6789");
        //websocket = new WebSocket("ws://192.168.0.53:6789");
        console.info("try to send ....");
        var json = JSON.stringify(msg);
        console.log(json);
        websocket.onopen = () => websocket.send(json);
        websocket.onerror = error => {
            console.log(`WebSocket error: ${error}`)
        };
        websocket.onmessage = function (event) {

            data = JSON.parse(event.data);
            console.log("bbbbbbbbbbbbbbbb " + data);
            switch (data.action) {
                case 'notify' :
                    alert(data.message);
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
        //websocket.onclose = () => console.log("exiting");
    }catch (e) {
        console.log("error : ", e.message);
    }

}

