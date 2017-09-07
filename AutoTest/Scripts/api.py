#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json
import traceback
import requests
import time




FrontUrl = "http://10.66.30.71:8003"
url = FrontUrl + "/touring-car"
querystring  =  "{\r\n  \"paging\": {\r\n    \"pageIndex\": 1,\r\n " \
                "   \"pageSize\": 2000\r\n  },\r\n  \"condition\": {\r\n" \
                "    \"pickUpDate\": \"2017-08-19T07:12:15.022Z\",\r\n    " \
                "\"returnDate\": \"2017-08-31T07:12:15.022Z\",\r\n    " \
                "\"gearboxId\": null,\r\n    \"suitableNumber\": null,\r\n    " \
                "\"brandId\": null\r\n  }\r\n}"


headers = {
"Content-Type": "application/json",
'cache-control': "no-cache"
}

#Post接口调用
response = requests.request("POST",url, headers = headers,data = querystring)

#对返回结果进行转义成json串
results = json.loads(response.text)

#获取http请求的status_code
print("Http code:", response.status_code)

#返回结果验证
print (results)




