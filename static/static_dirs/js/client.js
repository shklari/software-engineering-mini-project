

function send_msg(msg)
{
    //print("coco");
    websocket = new WebSocket("wss://192.168.0.12:6789");
    websocket.onopen = () => websocket.send('hello');
    console.log("try to send ....");
    websocket.send(JSON.stringify(msg));
    websocket.onmessage = function (event) {
        let data = JSON.parse(event.data);
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