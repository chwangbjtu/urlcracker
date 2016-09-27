local cjson = require("cjson")
function getUrls(res)
    local resObj = cjson.decode(res) 
    if resObj.type == "0" then
        return res
    else
        local head = resObj['start']
        local tail = resObj['end']
        local segs = resObj['seg']

        if segs ~= nil and head ~= nil or tail ~= nil then
            for format, format_seg in pairs(segs) do
                for k, v in pairs(format_seg) do
                    url = getRealUrl(v['url'], head, tail)
                    if url ~= '' then
                        v['url'] = url
                    end
                end
            end
        end

        return cjson.encode(resObj)
    end
end


local ltn12 = require("ltn12")
local http = require("socket.http")
function http.get(u)
   local t = {}
   local r, c, h = http.request{
      url = u,
      sink = ltn12.sink.table(t)}
   return r, c, h, table.concat(t)
end

function getRealUrl(url, head, tail)
    res, code, headers, body = http.get(url)
    if code == 200 then
        local pos_h = string.find(body, head)
        local pos_b = string.len(head) + pos_h
        local pos_t = string.find(body, tail, pos_b)
        url = string.sub(body, pos_b, pos_t - 1)
        url_r, count = string.gsub(url, '\\', '')
        return url_r
    end

    return ""
end

