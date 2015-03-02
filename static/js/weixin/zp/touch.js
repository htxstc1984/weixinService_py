var tDirect = {t:false,r:false,b:false,l:false},tAc = 'stop',tStartX = 0,tStartY = 0,tMoveX = 0, tMoveY = 0,tEndX = 0,tEndY = 0,tCountX = 0,tCountY = 0,tSTime = 0,tETime = 0;
var tMaxTime = 500,tMinTime = 30,tMinX = 5,tMinY = 5;
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
	if((tCountX>tMinX || tCountY<tMinY) && (tETime-tSTime<tMaxTime)){
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
}
$('#prev').on(touchstart,function(){prevNext('prev')});
$('#next').on(touchstart,function(){prevNext('next')});
$('.box').each(function(){$(this).css({marginTop:'-'+$(this).outerHeight()/2+'px'});});