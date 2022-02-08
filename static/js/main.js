var home_route = "http://127.0.0.1:5000/";
var focuscolor = "yellow";
var isEdit = false;
var longpress;
var selectedItem;

var nav_bar =  document.getElementById('nav_bar')
var home = document.getElementById('home');
var add = document.getElementById('add')
var edit = document.getElementById('edit');

var debtadder = document.getElementById('debtadder');
var debtoradder = document.getElementById('debtoradder');

// detect longpress
function start_longpress(id) {
	if(isEdit==false && nav_bar.className == "") {
		longpress = setTimeout(
		
		function() {
			selectedItem = document.getElementById(id);
			selectedItem.style.background = "rgb(160,160,160)"
			edit.style.display = "inline-block";
			isEdit = true;
			add.style.transform = "rotate(45deg)";
		}
		
		,100);
	}
}

function stop_longpress() {
	clearTimeout(longpress);
}


function showlist(id) {
	if(isEdit == false) {
		window.location.href = home_route + 'list/' + id;
	}
}

home.onclick = function () {
	window.location.href = home_route;
}

add.onclick = function () {
	if(isEdit) {
		isEdit = false;
		edit.style.color = "white";
		if(window.location.href == home_route) {
			debtorediter.style.top = "-50%";
		} else if(window.location.href != home_route) {
			debtediter.style.top = "-50%";
		}
		nav_bar.className = "";
		add.style.transform = "rotate(-90deg)";
		selectedItem.style.background = "transparent";
		selectedItem = null;
		edit.style.display = "none";
	} else if(window.location.href != home_route) {
		if(nav_bar.className == "add") {
			add.style.color = "white";
			debtadder.style.top = "-50%";
			nav_bar.className = "";
		} else {
			add.style.color = focuscolor;
			debtadder.style.top = "47px";
			nav_bar.className = "add";
		}
	} else if(window.location.href == home_route) {
		if(nav_bar.className == "add") {
			add.style.color = "white";
			debtoradder.style.top = "-50%";
			nav_bar.className = "";
		} else {
			add.style.color = focuscolor;
			debtoradder.style.top = "47px";
			nav_bar.className = "add";
		}
	}
}

edit.style.display = "none";
edit.onclick = function () {
	if(window.location.href != home_route) {
		if(nav_bar.className == "add") {
			edit.style.color = "white";
			debtediter.style.top = "-50%";
			nav_bar.className = "";
		} else {
			edit.style.color = focuscolor;
			debtediter.style.top = "47px";
			nav_bar.className = "add";
			
			var debt_id = document.getElementById("debt_id");
			var edit_item = document.getElementById("edit_item");
			var edit_price = document.getElementById("edit_price");
			var edit_qtt = document.getElementById("edit_qtt");
			
			debt_id.value = selectedItem.id;
			edit_qtt.value = selectedItem.childNodes[3].innerText;
			edit_item.value = selectedItem.childNodes[1].innerText;
			
			edit_price.value = selectedItem.childNodes[5].innerText;
		}
	} else if(window.location.href == home_route) {
		if(nav_bar.className == "add") {
			edit.style.color = "white";
			debtorediter.style.top = "-50%";
			nav_bar.className = "";
		} else {
			edit.style.color = focuscolor;
			debtorediter.style.top = "47px";
			nav_bar.className = "add";
			
			var debtor_id = document.getElementById("debtor_id");
			var new_nm = document.getElementById("new_nm");

			debtor_id.value = selectedItem.id;
			new_nm.value = selectedItem.innerText;
			new_nm.focus();
			
		}
	}
}

