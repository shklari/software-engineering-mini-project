

function send_msg(msg)
{
    //print("coco");
    websocket = new WebSocket("wss://10.100.102.6:6789");
    websocket.onopen = () => websocket.send('hello');
    console.log("try to send ....");
    websocket.send(JSON.stringify(msg));
    websocket.onmessage = function (event) {
        data = JSON.parse(event.data);
        switch (data.action) {
            case 'success':
                console.log("1");
                break;
            case 'failed':
                console.log("2");
                break;
            default:
                console.error(
                    "unsupported event", data);
        }
    };
}