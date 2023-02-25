import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

"""
			//fiddler 脚本
		//过滤无关请求，只关注特定请求
		if (oSession.fullUrl.Contains("website/parse/rest.q4w"))
		{

			var html = oSession.GetResponseBodyAsString()
			if(html.Contains("result")){
				//数据统计开始：把内容通过ajax http发送其它地方
				var _xhr = new ActiveXObject('Microsoft.XMLHTTP');
				var url = 'http://127.0.0.1:8000/sendData';
				//发送的数据参数
				var jsonString = oSession.GetResponseBodyAsString();
				var requestHeaders = oSession.oRequest.headers.ToString();
				var responseHeaders=oSession.oResponse.headers.ToString();

				var str='{}';//构造自己的JSON http请求的信息及返回的结果
				var data = Fiddler.WebFormats.JSON.JsonDecode(str);

				data.JSONObject["requestHeaders"]=requestHeaders;
				data.JSONObject["responseHeaders"]=responseHeaders;
				data.JSONObject["responseBody"] = jsonString;
				data.JSONObject["url"] = oSession.fullUrl;
				data.JSONObject["response_code"] = oSession.responseCode;

				if(oSession.oRequest.headers.Exists("Cookie")){
					data.JSONObject["requestCookie"] = oSession.oRequest.headers['Cookie'];
				}else{
					data.JSONObject["requestCookie"] = 'request no Cookie';
				};

				if(oSession.oResponse.headers.Exists("Cookie")){
					data.JSONObject["responseCookie"] = oSession.oResponse.headers['Cookie'];	
				}else{
					data.JSONObject["responseCookie"] = 'response no Cookie';
					};


				jsonString = Fiddler.WebFormats.JSON.JsonEncode(data.JSONObject)

				FiddlerObject.log(jsonString);

				_xhr.onreadystatechange=function(){
						if (_xhr.readyState==4){
							FiddlerObject.log(_xhr.responseText);
						}	
						};
				_xhr.open('POST', url, true);
				_xhr.send(jsonString);
				//----数据统计结束-----
			}else{
				 //弹窗报错
				FiddlerObject.alert("抓取出错！");
			} // if end


		} // if controll end
"""
import time


class Item(BaseModel):
    url: str
    response_code: str
    responseBody: str
    requestHeaders: str
    responseHeaders: str
    requestCookie: str
    responseCookie: str


urls = []

app = FastAPI()


@app.post("/sendData")
async def post_info1(request_data: Item):
    print("url:", request_data.url)
    print("response_code:", request_data.response_code)
    print("responseBody:", request_data.responseBody)
    print('requestHeaders:', request_data.requestHeaders)
    print('responseHeaders:', request_data.responseHeaders)
    print('requestCookie:', request_data.requestCookie)
    print('responseCookie:', request_data.responseCookie)
    # 保存数据 数据清洗 保存本地

    return 'ok'


if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=9999)
