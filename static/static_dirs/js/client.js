//const WebSocket = require('ws');

function send_msg(msg, ev)
{

    try {
        websocket = new WebSocket("ws://10.100.102.7:6789");
        console.info("try to send ....");
        var json = JSON.stringify(msg);
        console.log(json);
        websocket.onopen = () => websocket.send(json);
        websocket.onerror = error => {
            console.log(`WebSocket error: ${error}`)
        }
        websocket.onmessage = function (event) {

            data = JSON.parse(event.data);
            switch (data.action) {
                case 'success':
                    console.log('success');
                    ev(data.message);
                    break;
                case 'fail':
                    console.log('fail');
                    ev(data.message);
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