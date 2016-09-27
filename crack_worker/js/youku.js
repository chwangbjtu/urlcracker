(
function cal(sinjson)
{
    Ee = function(a) {
        if (!a)
            return "";
        var a = a.toString(), c, b, f, d, g, h;
        f = a.length;
        b = 0;
        for (c = ""; b < f; ) {
            d = a.charCodeAt(b++) & 255;
            if (b == f) {
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(d >> 2);
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((d & 3) << 4);
                c += "==";
                break
            }
            g = a.charCodeAt(b++);
            if (b == f) {
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(d >> 
                2);
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((d & 3) << 4 | (g & 240) >> 4);
                c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((g & 15) << 2);
                c += "=";
                break
            }
            h = a.charCodeAt(b++);
            c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(d >> 2);
            c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((d & 3) << 4 | (g & 240) >> 4);
            c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((g & 15) << 2 | (h & 192) >> 6);
            c += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(h & 63)
        }
        return c
    };

    function F(a, c) 
    {
        for (var b = [], f = 0, i, e = "", h = 0; 256 > h; h++)
            b[h] = h;
        for (h = 0; 256 > h; h++)
            f = (f + b[h] + a.charCodeAt(h % a.length)) % 256, i = b[h], b[h] = b[f], b[f] = i;
        for (var m = f = h = 0; m < c.length; m++)
            h = (h + 1) % 256, f = (f + b[h]) % 256, i = b[h], b[h] = b[f], b[f] = i, e += String.fromCharCode(c.charCodeAt(m) ^ b[(b[h] + b[f]) % 256]);
        return e
    };

    function G(a, c) 
    {
        for (var b = [], f = 0; f < a.length; f++) {
            for (var d = 0, d = "a" <= a[f] && "z" >= a[f] ? a[f].charCodeAt(0) - 97 : a[f] - 0 + 26, g = 0; 36 > g; g++)
                if (c[g] == d) {
                    d = g;
                    break
                }
            b[f] = 25 < d ? d - 26 : String.fromCharCode(d + 97)
        }
        return b.join("")
    }

    function pa(a) {
        if (!a)
            return "";
        var a = a.toString(), c, b, f, i, e, h = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
 -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6,
 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1];
        i = a.length;
        f = 0;
        shi=0
        for (e = ""; f < i; ) {
            do
                c = h[a.charCodeAt(f++) & 255];
            while (f < i && -1 == c);

            if (-1 == c)
                break;
            do
                b = h[a.charCodeAt(f++) & 255];
            while (f < i && -1 == b);
            if (-1 == b)
                break;
            e += String.fromCharCode(c << 2 | (b & 48) >> 4);
            do {
                c = a.charCodeAt(f++) & 255;
                if (61 == c)
                    return e;
                c = h[c]
            } while (f < i && -1 == c);
            if (-1 == c)
                break;
            e += String.fromCharCode((b & 15) << 4 | (c & 60) >> 2);
            do {
                b = a.charCodeAt(f++) & 255;
                if (61 == b)
                    //return e.length;
                    return e;
                b = h[b]
            } while (f < i && -1 == b);
            if (-1 == b)
                break;
            e += String.fromCharCode((c & 3) << 6 | b)
        }
        return e.length
        return e
    };

    Conv = function(a)
    {
        var b = a;
            switch (a) {
            case "m3u8":
                b = "mp4";
                break;
            case "3gphd":
                b = "3gphd";
                break;
            case "flv":
                b = "flv";
                break;
            case "flvhd":
                b = "flv";
                break;
            case "mp4hd":
                b = "mp4";
                break;
            case "mp4hd2":
                b = "hd2";
                break;
            case "mp4hd3":
                b = "hd3"
            }
            return b
    }

    RandomProxy = function(a) {
        this._randomSeed = a;
        this.cg_hun()
    };

    RandomProxy.prototype.get_info = function()
    {
        return this._randomSeed+"-:-"+this._cgStr+"--len--" + this._cgStr.length;
    }

    RandomProxy.prototype.cg_hun = function() 
    {
        this._cgStr = "";
        for (var a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\\:._-1234567890", c = a.length, b = 0; b < c; b++) {
            var f = parseInt(this.ran() * a.length);
            this._cgStr += a.charAt(f);
            a = a.split(a.charAt(f)).join("")
            //this._cgStr = a
            }
        }

        RandomProxy.prototype.cg_fun = function(a) 
        {
        for (var a = a.split("*"), c = "", b = 0; b < a.length - 1; b++)
            c += this._cgStr.charAt(a[b]);
            return c
        }

        RandomProxy.prototype.ran = function() 
        {
            tinfo = this._randomSeed + ":" + (211 * this._randomSeed + 30031) + ":"+(211 * this._randomSeed + 30031) % 65536
            this._randomSeed = (211 * this._randomSeed + 30031) % 65536;
            return this._randomSeed / 65536.0
        }
    
    T = function(a, c,sid,token) 
    {
        this.tmp1 = ""
        this.tmp1 = "111"
        b = a["stream"]
        //this._seed = a["seed"];
        this._fileType = c;
        this._sid = sid;
        this._token = token;
        this._totaltime = 0;
        this.src_list = []
        this.src_num = 0
        //var b = new U(this._seed);
        
        var e = (new RandomProxy,[]),f=[];
        this.tmp1 = "222"
        f.streams = {},
        f.logos = {},
        f.typeArr = {},
        f.totalTime = {};

        this.tmp01 = ""
        this.tmp02 = ""
        this.tmp0 = ""
        this.tmp2 = ""
        this.tmp3 = ""
        this.tmp4 = ""

        //this._streamFileIds = a["streamfileids"];
        this._videoSegsDic = {};

        for (var g = 0; g < b.length; g++) {
            for (var h = b[g].audio_lang, i = !1, j = 0; j < e.length; j++)
                if (e[j] == h) {
                    i = !0;
                    break
                }
            i || e.push(h)
        }

        for (var g = 0; g < e.length; g++) {
            for (var k = e[g], l = {}, m = {}, n = [], j = 0; j < b.length; j++) {
                var o = b[j];
                this.tmp1 = "222.1"
                if (k == o.audio_lang) {
                    var p = Conv(o.stream_type)
                      , q = 0;
                    "none" != o.logo && (q = 1),
                    m[p] = q;
                    var r = !1;
                    for (var s in n)
                        p == n[s] && (r = !0);
                    r || n.push(p);
                    var t = o.segs;
                    if (null  == t)
                        continue;var u = [];
                    r && (u = l[p]);
                    this.tmp1 = "222.1.5" + t.length
                    for (var v = 0; v < t.length; v++) {
                        var w = t[v];
                        if (null  == w)
                            break;
                        var x = {};
                        x.no = v,
                        x.size = w.size,
                        x.seconds = Number(w.total_milliseconds_video) / 1e3,
                        x.milliseconds_video = Number(o.milliseconds_video) / 1e3,
                        x.key = w.key,
                        x.fileId = this.getFileId(o.stream_fileid, v);
                        x.src = this.getVideoSrc(j, v, a, o.stream_type, x.fileId,sid,token);
                        x.type = p;
                        u.push(x);
                    }
                    l[p] = u
                }
            }
            //var y = this.langCodeToCN(k).key;
            var y = "test";
            f.logos[y] = m,
            f.streams[y] = l,
            f.typeArr[y] = n
           
        }
        this._videoSegsDic = f;
       
        this.tmp1 = f;
    }

    T.prototype.get_info = function()
    {
        return "T info:" + this.tmp01 +","  + this.tmp02 +","  + this.tmp0 +","+ this.tmp1+","+this.tmp2+","+this.tmp3+","+this.tmp4
    }


        T.prototype.get_urls = function()
        {
            //return this.tmp1
            //return this._videoSegsDic["mp4"]["0"]["src"]
            //var last = this._videoSegsDic.toJSONString();
            //var last = this._videoSegsDic["streams"]["test"].toJSONString();
            //var last = stringify(this._videoSegsDic);
             //var str1 = '{ "name": "cxh", "sex": "man" }';
            //var obj = str1.parseJSON();
            //return "111"
            obj = this._videoSegsDic["streams"]["test"];
            //var last=obj.toJSONString(); 
            var last =  JSON.stringify(obj);
            return last;
            return this._videoSegsDic["streams"]["test"]
            return this._videoSegsDic["streams"]["test"]["3gphd"][0]["src"]
            return this._videoSegsDic["test"]["mp4"]["0"]["src"]
            //this._videoSegsDic["mp4"]["src"];
        }

        //T.prototype.getFileId = function(a, c, b, f) 
        //T.prototype.getFileId = function(a, b,sid,token) 
        T.prototype.getFileId = function(a, b) 
        {
            if ( null == a || "" == a)
                return "";
            var c = "",d = a.slice(0,8),e = b.toString(16);
            1 == e.length && (e="0"+e),e = e.toUpperCase();
            var f = a.slice(10,a.length);
            return c = d+e+f;
        }
        //T.prototype.getVideoSrc = function(a, c, e, f, i, g) 
        T.prototype.getVideoSrc = function(a, b, c, d, e, sid,token) 
        {
            var h = c.stream[a],i = c.video.encodeid;
            if ( !i || !d)
                return "";
            var j = {flv:0,flvhd:0,mp4:1,hd2:2,"3gphd":1,"3gp":0},
                k = j[d],
                l = {flv:"flv",mp4:"mp4",hd2:"flv",mp4hd:"mp4",mp4hd2:"mp4","3gphd":"mp4","3gp":"flv",flvhd:"flv"},
                m = l[d],n = b.toString(16);
            1 == n.length && (n = "0" + n);
            var o = h.segs[b].total_milliseconds_video / 1e3
              , p = h.segs[b].key;
            ("" == p || -1 == p) && (p = h.key2 + h.key1);
            var q = "";
            c.show && (q = c.show.pay ? "&ypremium=1" : "&ymovie=1");
            var r = "/player/getFlvPath/sid/" + sid + "_" + n + "/st/" + m + "/fileid/" + e + "?K=" + p + "&hd=" + k + "&myp=0&ts=" + o + "&ypp=0" + q;
            var s = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26];
            var t = encodeURIComponent(Ee(F(G("boa4poz1", s).toString(), sid + "_" + e + "_" + token)));
            r += "&ep=" + t;
            r += "&ctype=12";
            r += "&ev=1";
            r += "&token=" + token;
            r += "&oip=" + c["security"]["ip"];
            return "http://k.youku.com" + r;
        }

    //injson = eval(sinjson)
    //injson = eval(sinjson.options)
    //type,mp4hd/mp4hd2/mp4hd3
    gru = function get_r_url(tinjson, type)
    {
        drurls = {}
        videoinfo = tinjson["stream"]
        vinfo={}
        for ( i=0;i<videoinfo.length;i++)
        {
            if ( type == videoinfo[i]["video_type"])
                vinfo = videoinfo[i]
        }
        //if "segs" not in vinfo:
        //    return drurls

        
    }
    injson = JSON.parse(sinjson);
    id = injson["id"]


    //return injson["ep"]
    //injson["ep"] = "PwXTSA8aL7nd1PLE8+JxB9H8uBI71wnIWBg="
    strna = pa(injson["security"]["encrypt_string"])
    //strna = pa("NQXURgkdI73d0vPI9uJxVNOgvUE41w7JXh4=")
    //return strna
    
    videotype = ""
    videoinfo = injson["stream"]//get videotype:flv/mp4/hd2...

    tq = {"flv":"flv","mp4":"mp4","hd2":"flv","3gphd":"mp4","3gp":"flv"}
    types = ["mp4","flv","hd2","3gp"]
    typeslen = types.length 
    stream_len = videoinfo.length

    for (i=0;i<types.length;i++)
    {
        for ( j = 0;j<stream_len;j++)
        {
            if (types[i] in videoinfo)
            {
                videotype = types[i]
                break;
            }
        }
    }


    para = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]
    var f1 = "b4eto0b4"
    //G is F
    strg = G(f1,para)
    //return strg
    //return strg.length+":"+strna.length
    stre = F(strg,strna)
    sid = stre.split("_")[0]
    token = stre.split("_")[1]
    //return sid+":"+token
    //total_time = parseInt(injson["seconds"])

    //return stre
    //return videotype
    //return total_time
    //return sid+":"+token

    //injson["ip"] = 2130706433
    /*
    videotype = "mp4"
    sid = "843624927525612ea8116"
    token = "4307"
    injson["seed"] = 7187
    injson["videoid"] = "76534322"
    injson["ip"]= 2102959564
    injson["streamfileids"]["mp4"] = "55*36*55*55*55*41*55*9*55*55*18*3*7*33*44*9*24*36*18*41*53*24*55*18*35*7*18*3*28*9*36*18*31*36*7*9*12*9*63*33*55*55*24*63*44*35
*41*55*63*31*28*24*18*63*55*44*12*53*35*12*7*33*31*28*41*55*"

     tmp4={}
        tmp4["no"]=0
        tmp4["size"]="24018349"
        tmp4["seconds"]=349
        tmp4["k"]="a4f21ea33b8adfdd261e709d"
        tmp4["k2"]="102042f4ed53cfc5b"
        tmp4_0=[tmp4]
        //tmp4_0.append(tmp4)
        tmp4_0_1 = {}
        tmp4_0_1["mp4"]=tmp4_0
        injson["segs"]=tmp4_0_1
    */
    //return ":----"+injson["segs"]["hd2"][0]["k"]
    //return ":----"+injson["ip"]
    
    //return "len is:"+injson["segs"]["mp4"].length

    var tt = new T(injson,videotype,sid,token)
    //info = tt.get_info()
    urls = tt.get_urls()
    //return "aaa"    
    return urls

    //var b = new U(injson["seed"]);
    //var b = new U(7187);
    //var info = b.get_info()
    return info+""
    
    return "122"

}
)
