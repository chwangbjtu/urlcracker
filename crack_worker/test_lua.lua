require("json2lua")

res = [[
{
    "end": "\"",
    "vid": "3",
    "url": "http://m.iqiyi.com/v_19rro2q4mg.html",
    "site": "iqiyi",
    "seg": [
        {
            "url": "http://g3.letv.cn/vod/v2/MTUzLzM4LzIxL2xldHYtdXRzLzE0L3Zlcl8wMF8yMi0zMjM4NDk2NzYtYXZjLTIyNTMyNC1hYWMtMzIwMDAtMjcwMzAwMC04OTkyNzM4My03NTNhOTQ0NzM3ZjgzYjg1MDYwN2E2MzI1ZTJkYjhiOS0xNDM3NzI1OTc0MDA4Lm1wNA==?b=266&mmsid=33603109&tm=1440487357&key=ddcc23ccde1c26b82ec2d176822d60b6&platid=3&splatid=304&playid=0&tss=no&vtype=21&cvid=841608052359&payff=0&pip=4dca0db9c30c8c0d8adb05394f76cf1c&format=1&expect=3&p1=0&p2=04&termid=2&ostype=android&hwtype=un&uuid=1440487357452",
            "duration": "" 
        }
    ],
    "start": "\"location\": \"",
    "type": "1" 
}
]]

res_sh = [[
{
    "end": "",
    "vid": 1234,
    "format": [
        "high"
    ],
    "url": "http://tv.sohu.com/20140522/n399900251.shtml",
    "site": "sohu",
    "seg": {
        "high": [
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/243/108/Q9pzc3Bo3MakNS2Q1Uhxw3.mp4&vid=1782553&plat=17&mkey=ZlelshhrDIlyFL0WSsjxatwRA8jjSu_v&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/76/132/mYrYf92RIfe2MXoja1eLX1.mp4&vid=1782553&plat=17&mkey=82j82BZSvhLHBcdRgOThk3YZJF4m1LIp&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/196/180/pE1p2FK1rgdKxKhJsNlKV.mp4&vid=1782553&plat=17&mkey=AumlK_JsENGFVZBE7V0nzGyYPdV-MmMi&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/147/210/fQ3qlFY9d4sjKL5wrY8E53.mp4&vid=1782553&plat=17&mkey=QlxwU7C7qJ_i9m43pqrozvN8BzqdeHLg&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/11/194/ZSVG1PxfyecyuRwpAx7xV7.mp4&vid=1782553&plat=17&mkey=ZXXkCkfe5XUmfWUKtj4FxQ5bGddEg9H4&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/194/64/QIPgH9tTtA3wKfS0wJ5rv4.mp4&vid=1782553&plat=17&mkey=46vrIM3w1xFhKeAKaIcW0x-HWtn1gCRF&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/62/29/TDZcSy5bEgdXex1EBsXIp4.mp4&vid=1782553&plat=17&mkey=J3Dk-7CmDG150BEmFI1thdAH14SQ6WMu&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/16/67/mzFb8u1ylHlSPR5FJ6i932.mp4&vid=1782553&plat=17&mkey=tY4znbg4DEs250ggjgfUl8l0Q86mCEPh&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/143/75/nYWBrHsk68w2QZ6ltHX262.mp4&vid=1782553&plat=17&mkey=2-PqG3ri2f8sEyKVmH6LDcwGFDZAtfE2&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/24/213/IvHgDqLuGeQmVHK1Q4l5D6.mp4&vid=1782553&plat=17&mkey=-vBPtBXzAneBh8xnm6udL4qqryJZ9wpD&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/155/62/tF2ZvIa1qORsVXtugh7nW3.mp4&vid=1782553&plat=17&mkey=WGSfLNCCjl6HcBSYgTXH6GDgOe0HpQ9i&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/138/82/GuNCkem8AzNCfQNxDYN3c3.mp4&vid=1782553&plat=17&mkey=vqAcvqTr36JxrPaILT5NSnm9wLDzaj49&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/160/138/9rbdsW2ty3dgfLzF00ctU.mp4&vid=1782553&plat=17&mkey=eWBg4fnJ7JrmbrQPV7HW-w1nQgvNGODQ&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/175/62/sPX9SgLj6yaDUXakwTxQx6.mp4&vid=1782553&plat=17&mkey=qfuY8ardpSiAqA8gdmFPiZZxS41QP3Ng&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/212/20/vN3W9ltvYj7IEBjZkxtEN3.mp4&vid=1782553&plat=17&mkey=Vshs_XfMpFSStIZXh5NQzYpgv4dxbQaS&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/227/105/gfeSYTngGG1Zjo9L6Jh0R3.mp4&vid=1782553&plat=17&mkey=Dy24xB9PiVNyTqDwNfsNlZ6Ugn-gFla4&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/203/0/t5RCnaNQeW7DkvdyD6DwM3.mp4&vid=1782553&plat=17&mkey=YG0XDjuwbVFKBOvrC4rdfnTI8ubZhufr&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/124/157/Vd6AXJqSCIbUVcXsb11d6.mp4&vid=1782553&plat=17&mkey=u6SYV56XdYLty5vhT5Mflzq1lj236gK2&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/240/109/Ya8kh2jtNoAQap8qRnOjM3.mp4&vid=1782553&plat=17&mkey=13wCYgltSK5W24N2yb84mJ9nwE1-Pxs2&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/15/168/aX4lybr7JYGUPuCn9PpaQ7.mp4&vid=1782553&plat=17&mkey=R7dFl1h1_5MIn1sZVz770F6TBS940I8J&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/136/166/OqoNtvwLcj2f5EwIUBukH1.mp4&vid=1782553&plat=17&mkey=L_LMtpWUqp8-mnZNWbfSL-gKbKIP3LQF&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/208/209/K5GaK3Sja4A6mxik0PJxG7.mp4&vid=1782553&plat=17&mkey=eykfOwEeaU4nMTfQlNwe1uvHtybWpDW4&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "300",
                "url": "http://data.vod.itc.cn/?new=/7/227/MmBbPeQHuS4z80b2e8Tqf2.mp4&vid=1782553&plat=17&mkey=1GUq1uBgIPJU8TtzE_waNqNFree9r6K7&ch=tv&plat=17&prod=h5"
            },
            {
                "duration": "258",
                "url": "http://data.vod.itc.cn/?new=/26/236/VP1p4YfIPBoxg56aCgv05.mp4&vid=1782553&plat=17&mkey=mBxjOYl95OIisEmjSh0ih3mFvlrz_0vj&ch=tv&plat=17&prod=h5"
            }
        ]
    },
    "start": "",
    "type": "0"
}
]]

res_hn = [[
{"vid": "12345", "format": ["high"], "url": "http://www.hunantv.com/v/1/1/f/1742233.html", "site": "hunantv", "seg": {"high": [{"url": "http://pcfastvideo.imgo.tv/ba5f2ed48b884f863bd99407f3c2e2c8/55ed3985/c1/2014/zongyi/kuailedabenying/20150801f9ecb74f-b096-44a9-8b07-9c3abbc632d9.fhv.mp4?uuid=5d419e39c9d742948504f162ffd5049a", "duration": ""}]}, "type": "0"}
]]

res_le = [[
{"end": "\"", "vid": "12345", "format": ["high"], "url": "http://www.letv.com/ptv/vplay/23195473.html", "site": "letv", "seg": {"high": [{"url": "http://g3.letv.cn/vod/v2/MTU1LzIwLzM0L2xldHYtdXRzLzE5L3Zlcl8wMF8yMi0zMjQzNjI2MDktYXZjLTEyODEyOC1hYWMtMzIwMDAtNDk2NTkzMi0xMDQ5MDMzMzUtMmRmNzM3M2FlZTg4NDNjOWIyODM3Mzg0ZTVlMDIyZDktMTQzODU2MTk3NDg2NC5tcDQ=?b=168&mmsid=33717902&tm=1441610068&key=c843d8cb30a8ecdba3a9b774134cd81f&platid=3&splatid=301&playid=0&tss=no&vtype=9&cvid=2043162788582&payff=0&pip=01c2489f9a20ea6de86eef8572c8de30&p2=04&p1=02&uuid=&format=1&hwtype=un&termid=2&expect=3&jsonp=&ostype=android&", "duration": ""}]}, "start": "\"location\": \"", "type": "1"}
]]

res_yk = [[
{
    "end": "",
    "vid": 2233,
    "format": [
        "high"
    ],
    "url": "http://v.youku.com/v_show/id_XMTI1ODc5MjU2NA==.html",
    "site": "youku",
    "seg": {
        "high": [
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_00/st/mp4/fileid/0300080B005577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=2050166a762d276a241254bd&hd=1&myp=0&ts=376&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQALshTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "376"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_01/st/mp4/fileid/0300080B015577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=bfd3c7619c36a577261e8d3b&hd=1&myp=0&ts=363&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQALohTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "363"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_02/st/mp4/fileid/0300080B025577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=34e4ea47294436b1241254bd&hd=1&myp=0&ts=382&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQALkhTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "382"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_03/st/mp4/fileid/0300080B035577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=ee8a7b94de00877d261e8d3b&hd=1&myp=0&ts=397&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQALghTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "397"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_04/st/mp4/fileid/0300080B045577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=47646aac88cbbe1d241254bd&hd=1&myp=0&ts=374&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQAL8hTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "374"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_05/st/mp4/fileid/0300080B055577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=85e61a8dfb7e087e241254bd&hd=1&myp=0&ts=374&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQAL4hTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "374"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_06/st/mp4/fileid/0300080B065577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=25b8dc735797f096261e8d3b&hd=1&myp=0&ts=410&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQAL0hTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "410"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_07/st/mp4/fileid/0300080B075577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=b14de0de8cb5a20b241254bd&hd=1&myp=0&ts=384&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQALwhTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "384"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_08/st/mp4/fileid/0300080B085577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=aef6e3ec8a6b7035261e8d3b&hd=1&myp=0&ts=391&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQALMhTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "391"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_09/st/mp4/fileid/0300080B095577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=83980d0b9dde498e282ac5b9&hd=1&myp=0&ts=303&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQALIhTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "303"
            },
            {
                "url": "http://k.youku.com/player/getFlvPath/sid/54416095065621256ce65_10/st/mp4/fileid/0300080B0A5577ED5F563B2E10BECFC3C9330F-92FE-723F-D919-BD74F9C6A276?K=60cbc4a00cb6dc98241254bd&hd=1&myp=0&ts=342&ypp=0&ymovie=1&ep=dyaQG0%2BNX8sA4ybZij8bYiqxIXEKXP4J9h%2BFidIQAMohTe%2B47ErUsZi2TY1AY%2FgZAFd1Zpjy2NnkaUBiYflB3x0Q2EyrT%2FqU9%2FHq5d8nw5R2b2owA8%2FQslSfRTf4&ctype=12&ev=1&token=1679&oip=1780930298",
                "duration": "342"
            }
        ]
    },
    "start": "",
    "type": "0"
}
]]

res_er = [[
{"code": "2", "error": 1}
]]

print(getUrls(res_sh))
print(getUrls(res_hn))
print(getUrls(res_yk))
print(getUrls(res_le))
print(getUrls(res_er))
