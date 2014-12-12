function post(URL, PARAMS) {
	var temp = document.createElement("form");
	temp.action = URL;
	temp.method = "post";
	temp.style.display = "none";
	for (var x in PARAMS) {
		var opt = document.createElement("textarea");
		opt.name = x;
		opt.value = PARAMS[x];
		// alert(opt.name)
		temp.appendChild(opt);
	}
	document.body.appendChild(temp);
	temp.submit();
	return temp;
}

function is_weixin() {
	return true;
}

function check() {
	if (!is_weixin()) {
		var errPage = "<div data-role='header'><h1>错误</h1></div><div data-role='content'><p style='color: #999'>您无法访问此页面</p></div>";
		$("#container").empty().append(errPage).trigger("create");;
	}
}

