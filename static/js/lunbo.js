//手动，鼠标点击
$(".number li").mouseover(function () {
    $(this).addClass("current").siblings().removeClass("current");
    var index = $(this).index();
    i = index;
    $(".img li").eq(index).fadeIn(500).siblings().fadeOut(500);
});
//自动轮播
var time = setInterval(move, 2500);
var i = 0;

function move() {
    //加入一个if判断，自动走完一遍，再来
    if (i == 3) {
        i = -1;
    }
    i++;
    $(".number li").eq(i).addClass("current").siblings().removeClass("current");
    $(".img li").eq(i).stop().fadeIn(500).siblings().stop().fadeOut(500);
}

function moveL() {
    if (i == 0) {
        i = 4;
    }
    i--;
    $(".number li").eq(i).addClass("current").siblings().removeClass("current");
    $(".img li").eq(i).stop().fadeIn(500).siblings().stop().fadeOut(500);
}

//给outer对象绑定事件，鼠标放上去停止轮转
$(".outer").hover(function () {
    clearInterval(time);
}, function () {
    time = setInterval(move, 1500)
});

//点击右边btn，往左轮
$(".right_btn").click(function () {
    move();
});

//点击左边btn，往右轮
$(".left_btn").click(function () {
    moveL();
});