
#统一下单支付接口
def payOrder(request,user_id):
    import time
    if request.method == 'POST':
        #获取价格
        price=request.POST.get("price")
 
        #获取客户端ip
        client_ip,port=request.get_host().split(":")
 
        #获取小程序openid
        openid=MyUser.objects.get(id=user_id).openid
 
        #请求微信的url
        url=configuration.order_url
 
        #拿到封装好的xml数据
        body_data=pay.get_bodyData(openid,client_ip,price)
 
        #获取时间戳
        timeStamp=str(int(time.time()))
 
        #请求微信接口下单
        respone=requests.post(url,body_data.encode("utf-8"),headers={'Content-Type': 'application/xml'})
 
        #回复数据为xml,将其转为字典
        content=pay.xml_to_dict(respone.content)
 
        if content["return_code"]=='SUCCESS':
            #获取预支付交易会话标识
            prepay_id =content.get("prepay_id")
            #获取随机字符串
            nonceStr =content.get("nonce_str")
 
            #获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
            paySign=pay.get_paysign(prepay_id,timeStamp,nonceStr)
 
            #封装返回给前端的数据
            data={"prepay_id":prepay_id,"nonceStr":nonceStr,"paySign":paySign,"timeStamp":timeStamp}
 
            return HttpResponse(packaging_list(data))
 
        else:
            return HttpResponse("请求支付失败")
    else:
        return HttpResponse(request_code())