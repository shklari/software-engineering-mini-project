//const WebSocket = require('ws');

function send_msg(msg, onsuccess , onfailure)
{

    try {
        websocket = new WebSocket("ws://192.168.0.125:6789");
        //websocket = new WebSocket("ws://192.168.0.53:6789");
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
                case 'notify' :
                    alert(data.message);
                case 'success':
                    console.log('success');
                    onsuccess(data.message,data.return_val );
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

function load_inventory(){
    var storename = getElementById("store_name").value;

    var onfailure = (ret) => {
     alert(res);
        window.location.href = '/';
    }
    var onsuccess = (message, val) => {
        inventory = val['inventory'];
        var i = 0;
        var table = document.getElementById('products');
        inventory.forEach((item)=>{
              var newRow = table.insertRow(table.length);
              var newCell = newRow.insertCell(i++);
              newCell.innerHTML = item['name'];
              newCell = newRow.insertCell(i++);
              newCell.innerHTML = item['price'];
              newCell = newRow.insertCell(i++);
              newCell.innerHTML = item['category'];
              newCell = newRow.insertCell(i++);
              newCell.innerHTML = item['quantity'];
        }
    }

    send_msg({action: "get_store", store_name: storename}, onsuccess, onfailure)
}

