var tDirect = {t:false,r:false,b:false,l:false},tAc = 'stop',tStartX = 0,tStartY = 0,tMoveX = 0, tMoveY = 0,tEndX = 0,tEndY = 0,tCountX = 0,tCountY = 0,tSTime = 0,tETime = 0;
var tMaxTime = 500,tMinTime = 30,tMinX = 10,tMinY = 50;
if('ontouchstart' in document){
	var touchstart = 'touchstart',touchend = 'touchend',touchmove = 'touchmove';
}else{
	var touchstart = 'mousedown',touchend = 'mouseup',touchmove = 'mousemove';
}
document.addEventListener(touchstart,function(e){
	tSTime = new Date().getTime();
	if(tETime>0 && (tSTime-tETime<tMinTime)){
		return;
	}
	tAc = 'start';
	if('touchstart'==touchstart){
		var touchers = e.changedTouches||e.targetTouches,toucher = touchers[0];
		tStartX = toucher.pageX,tStartY = toucher.pageY;
	}else{
		tStartX = e.clientX,tStartY = e.clientY;
	}
},true);
document.addEventListener(touchmove,function(e){
	e.preventDefault();
},true);
document.addEventListener(touchend,function(e){
	if(tAc != 'start'){
		tAc = 'start';
		return;
	}
	tAc = 'stop';
	if('touchstart'==touchstart){
		var touchers = e.changedTouches||e.targetTouches,toucher = touchers[0];
		tEndX = toucher.pageX,tEndY = toucher.pageY;
	}else{
		tEndX = e.clientX,tEndY = e.clientY;
	}
	tCountX = Math.abs(tEndX-tStartX),tCountY = Math.abs(tEndY-tStartY);
	tETime = new Date().getTime();
	if((tCountY>tMinY) && (tETime-tSTime<tMaxTime)){
		tDirect.l = tStartX>tEndX?true:false,tDirect.r = tStartX<tEndX?true:false;
		tDirect.t = tStartY>tEndY?true:false,tDirect.b = tStartY<tEndY?true:false;
		tAction();/*Run this function*/
	}
},true);

function tAction(action){
	if(tDirect.t){
		prevNext('next');
	}else if(tDirect.b){
		prevNext('prev');
	}
}

function prevNext(action){
		if(noTouch){
			return;
		}
		
		var onshow = $('div.onshow');
		var next = onshow.next('div.wp');
		var prev = onshow.prev('div.wp');
		if(action=='next'){
			if(next.attr('id')){
				$('#next').css({display:next.next('div.wp').attr('id')?'':'none'});
				$('#prev').css({display:next.prev('div.wp').attr('id')?'':'none'});
				
				next.addClass('onshow');
				onshow.removeClass('onshow');
				onshow.slideUp();
				//onshow.css({'-webkit-animation':'hide .5s forwards'});
			}
		}else if(action == 'prev'){
			if(prev.attr('id')){
				$('#next').css({display:prev.next('div.wp').attr('id')?'':'none'});
				$('#prev').css({display:prev.prev('div.wp').attr('id')?'':'none'});
				onshow.removeClass('onshow');
				prev.addClass('onshow');
				prev.slideDown();
				//prev.css({'-webkit-animation':'show .5s forwards'});
			}
		}
		$('#next').removeClass('slight');
		hidedetail();
	}

	function showdetail(id,loc,obj){
		
		$("#detail_cover").removeClass("detail_hide");
		$("#"+id).addClass("detail");
		
		if (loc) {
			//alert(obj.offsetTop+","+document.body.clientHeight);
			//var disX = e.clientX;
			//var disY = e.clientY;
			//var divX = $("#"+id).css("width").substring(0,$("#"+id).css("width").length-2) ;
			//var divY = $("#"+id).css("height").substring(0,$("#"+id).css("height").length-2) ;
			
			var disX = 0;
			var disY = obj.offsetTop+document.body.clientHeight*0.2;
			
			if(loc=='right'){
				disX = document.body.clientWidth*0.35;
			}
			if(loc=='left'){
				disX = document.body.clientWidth*0.05;
			}
			//alert(e.clientX+","+e.clientY);
			//alert($("#"+id).css("width")+","+$("#"+id).css("height"));
			$("#"+id).css({left:disX,top:disY});
		}
		
		$("#"+id).removeClass("detail_hide");
		noTouch = true;
	}
	
	function hidedetail(id){
		$(".detail").addClass("detail_hide");
		$(".detail_hide").removeClass("detail");
		//$("#"+id).removeClass("detail");
		//$("#"+id).addClass("detail_hide");
		$("#detail_cover").addClass("detail_hide");
		noTouch = false;
	}

	$('#prev').on("click",function(){prevNext('prev')});
	$('#next').on("click",function(){prevNext('next')});
