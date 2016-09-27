require("crack2")
p1 = [[
{"vid":"1234567", "url":"http://v.pptv.com/show/NBYCgOhOvvxf3UU.html","site":"pptv","os":"web"}
]]

p2 = [[
{"vid":"6299470", "url":"http://m.hunantv.com/#/play/553185","site":"hunantv","os":"aphone"}
]]

resp1 = ck(p1)
resp2 = ck(p2)
print(resp1)
print(resp2)
