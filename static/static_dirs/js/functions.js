
function CustomAlert(){
    this.render = function(dialog){
        $("#box").fadeIn(1000).show();
        var mes = '<strong class="pull-left primary-font">Name</strong>\n' +
            '        <small class="pull-right text-muted">\n' +
            '           <span class="glyphicon glyphicon-time"></span>7 mins ago</small>\n' +
            '        </br>\n' +
            '        <li class="ui-state-default">'+dialog+'</li>\n' +
            '        ';
        document.getElementById('sortable').innerHTML=mes;
        document.getElementById('footer').innerHTML= '<button class="btn btn-primary" onclick="Alert.ok()">OK</button>';
    }
	this.ok = function(){
		document.getElementById('box').style.display = "none";
	}
}
var Alert = new CustomAlert();