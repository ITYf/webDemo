// 封装Ajax对象的整体框架
// function Ajax() {
//     var ajax = new Objext();
//     // 封装 get请求的方法
//     ajax.get = function () {}
//     // 封装 post请求的方法
//     ajax.post = function () {}
//     return ajax; //返回AJAX对象
// }


// 下面我们一步一步实现 get和 post的封装
// 说白了，封装 Ajax的本质就是，创建一个 XMLHttpRequest对象，然后调用这个对象的一系列方法，实现对 get和 post的封装

function Ajax(dataType, async) {
    var ajax = new Object();

    // 第一步，创建 XMLHttpRequest对象，
    ajax.createXMLHttpRequest = function () {
        // 首先定义一个空的 xmlRequest对象
        var xmlRequest = false;
        if (window.XMLHttpRequest) {
            // 主流浏览器创建 XMLHTTPRequest对象
            xmlRequest = new XMLHttpRequest();
        } else if (window.ActiveXObject) {
            // IE5 、IE6创建 XMLHTTPRequest对象
            xmlRequest = new ActiveXObject('Microsoft.XMLHTTP');
        }
        return xmlRequest;
    }

    // 调用函数创建 XMLHTTPRequest，把创建好的 XMLHTTPRequest对象赋值给Ajax的一个属性
    ajax.xmlRequest = ajax.createXMLHttpRequest();

    // 第二步是初始化 AJAX的基本配置，
    // 一是： Ajax在请求资源时，是同步还是异步。
    // 二是： 服务器返回数据的类型是文本格式还是 JSON格式或是 XML格式（不推荐使用）

    // 处理数据类型，设定数据类型，就用设定的；没有设定，则默认是HTML
    ajax.dataType = dataType ? dataType.toUpperCase() : 'HTML';

    // 处理同步异步
    if (typeof (bool) == 'undefined') {
        // 如果没有设定同步异步的参数，默认异步
        ajax.async = true;
    } else {
        // 否则用设定好的
        ajax.async = async;
    }

    // 第三步：配置onreadystatechange事件调用的函数
    ajax.changeFunction = function () {
        // alert(ajax.xmlRequest.readyState);
        // 判断服务器响应状态，只有状态200并且 readyState=4的时候，才是响应成功
        if (ajax.xmlRequest.readyState == 4 && ajax.xmlRequest.status == 200) {
            // 根据用户设定的数据类型返回响应的格式数据
            if (ajax.dataType == 'HTML') {
                // HTML数据格式
                ajax.callback(ajax.xmlRequest.responseText)
            } else if (ajax.dataType == 'JSON') {
                // JSON数据格式,通过 JSON.parse全局函数把返回的字符串转 JSON对象
                ajax.callback(JSON.parse(ajax.xmlRequest.responseText))
            } else if (ajax.dataType == 'XML') {
                // XML数据格式
                ajax.callback(ajax.xmlRequest.responseXML)
            }
        }
    }


    // 前戏做完，现在就是重头戏了，封装 get()方法，注意观察是如何搭配
    // ajax.callback()、ajax.changeFunction()、xmlRequest.onreadystatechange之间的逻辑关系

    /** Ajax中get请求方法
     * @param string url请求的 URL
     * @param function callback 用来接受服务器返回数据的回掉函数
     */

    ajax.get = function (url, callback) {
        //  判断是否有回调函数，若有，要调用 onreadystatechange事件函数
        if (callback != null) {
            // 把传递过来的回调函数给 ajax的一个属性，
            // 便于 onreadystatechange事件函数调用
            ajax.callback = callback;
            // 调用 onreadystatechange事件函数，把服务器返回的数据给回调函数
            ajax.xmlRequest.onreadystatechange = ajax.changeFunction;
        }
        // 然后初始化请求参数
        ajax.xmlRequest.open('GET', url, ajax.async);
        // 发送请求
        ajax.xmlRequest.send();
    }

    /**Ajax中 post请求方法
     * @param string url 请求的url
     * @param string/onbect sendString post 请求携带的参数 字符串或者JSON对象
     * @param function callback 用来接受服务器返回的回调函数
     */

    ajax.post = function (url, sendString, callback) {
        //  处理要向服务器提交的参数为 XML支持的格式
        if (typeof (sendString == 'object')) {
            // 如果是 JSON对象，转化为字符串
            var str = '';
            // 循环遍历这个 JSON对象
            for (var key in sendString) {
                // 把JSON对象转换成 name=Tom&age=19的形式
                str += key + '=' + sendString[key] + '&';
            }
            // 删除字符串最后一个字符'&
            sendString = str.substr(0, str.length - 1);
        }
        // 判断是否有回调函数，有回调函数的话要调用onreadystatechange 事件函数
        if (callback != null) {
            // 把传递过来的回调函数给ajax的一个属性
            // 便于onreadystatechange事件函数使用
            ajax.callback = callback;
            //调用onreadystatechange事件函数，把服务器返回的数据给回调函数
            ajax.xmlRequest.onreadystatechange = ajax.changeFunction;
        }
        // 然后初始化 post请求
        ajax.xmlRequest.open('POST', url, ajax.async);
        // 设置POST请求头信息
        ajax.xmlRequest.setRequestHeader('COntent-Type', 'application/x-www-form-urlencoded');
        ajax.xmlRequest.send(sendString); //发送请求
    }

    /**
     * JSONP跨域请求
     * @param string url  请求的url
     * @param function callback  用来接受服务器返回数据的回调函数
     */

    ajax.jsonp = function (url, callback) {
        // 动态创建 script标签，用于 JSON请求远程服务器资源
        var script = document.createElement('script');
        // 随机生成函数名，不然会读取本地缓存的js文件
        var time = new Date();
        var funcName = 'jsonp' + time.getTime();

        // 拼接 URL，判断 url中是否传有参数
        if (url.indexOf('?') > 0) {
            url = url + '&callback=' + funcName;
        } else {
            // 如果 URL中没有传递参数就这样拼接
            url = url + '?callback' + funcName
        }

        // 注册回调函数到全局
        window[funcName] = function (data) {
            callback(data);
            // 把数据给回调函数之后销毁我们注册的函数和创建的 script标签
            delete window[funcName]; //删除函数
            script.parentNode.removeChild //删除script标签
        }

        // 设置 script标签的 src属性
        script.setAttribute('src', url);

        // 把 script标签加入 head，请求服务器得到数据
        document.getElementsByTagName('head')[0].appendChild(script);
    }

    return ajax; //返回 ajax对象
}