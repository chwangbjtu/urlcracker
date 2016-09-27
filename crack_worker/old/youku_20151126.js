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

    

    U = function(a) {
        this._randomSeed = a;
        this.cg_hun()
    };

    U.prototype.get_info = function()
    {
        return this._randomSeed+"-:-"+this._cgStr+"--len--" + this._cgStr.length;
    }

    U.prototype.cg_hun = function() 
        {
            this._cgStr = "";
            
            for (var a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\\:._-1234567890", c = a.length, b = 0; b < c; b++) {
                var f = parseInt(this.ran() * a.length);
                this._cgStr += a.charAt(f);
                a = a.split(a.charAt(f)).join("")
                //this._cgStr = a
            }
        }

        U.prototype.cg_fun = function(a) 
        {
            for (var a = a.split("*"), c = "", b = 0; b < a.length - 1; b++)
                c += this._cgStr.charAt(a[b]);
            return c
        }

        U.prototype.ran = function() 
        {
            tinfo = this._randomSeed + ":" + (211 * this._randomSeed + 30031) + ":"+(211 * this._randomSeed + 30031) % 65536
            this._randomSeed = (211 * this._randomSeed + 30031) % 65536;
            return this._randomSeed / 65536.0
        }
    
    T = function(a, c,sid,token) 
    {
        this._seed = a["seed"];
        this._fileType = c;
        this._sid = sid;
        this._token = token;
        this._totaltime = 0;
        this.src_list = []
        this.src_num = 0
        var b = new U(this._seed);

        this.tmp01 = ""
        this.tmp02 = ""
        this.tmp0 = ""
        this.tmp1 = ""
        this.tmp2 = ""
        this.tmp3 = ""
        this.tmp4 = ""

        this._streamFileIds = a["streamfileids"];
        this._videoSegsDic = {};

        //for (c in a["segs"]) {
        if (c in a["segs"]){
                this.tmp01 += c+":" + a["segs"][c].length
            for (var f = [], i = 0, g = 0; g < a["segs"][c].length; g++) {
                this.tmp02 +=   a["segs"][c][g]["k"]
                var h = a["segs"][c][g], p = {};
                p.no = h.no;
                p.size = h.size;
                p.seconds = h["seconds"];
                h.k && (p.key = h["k"]);
                this.tmp0 =  c +","+ parseInt(g)
                p.fileId = this.getFileId(a["streamfileids"], c, parseInt(g), b);
                this.tmp1 += p.fileId
                p.type = c;
                p.src = this.getVideoSrc(h["no"], a, c, p.fileId);
                this.src_list.push(p.src)
                this.src_num+=1
                this.tmp2 += p.src
                f[i++] = p
            }
            this._videoSegsDic[c] = f
            //#####
            //break;
        }
    }

    T.prototype.get_info = function()
    {
        //return "T info:"  + this._seed +"," +this._fileType+ "," +this._sid+","+this._token+","+this._streamFileIds["mp4"] + "," +this._videoSegsDic["mp4"].length+
","+ this._videoSegsDic["mp4"]
        return "T info:" + this.tmp01 +","  + this.tmp02 +","  + this.tmp0 +","+ this.tmp1+","+this.tmp2+","+this.tmp3+","+this.tmp4
    }

    //T.prototype = {

        T.prototype.get_urls = function()
        {
            //this._videoSegsDic["mp4"]["src"];
            //t = ""
            //for(i=0;i<this.src_list.length;i++)
            //    t += this.src_list[i]
            //return this.src_list+":"+this.src_num
            return this.src_list+","+this._fileType+","+this.src_list.length
            //return this.src_num
            //return "null"
        }

        T.prototype.getFileId = function(a, c, b, f) 
        {
            for (var d in a)
                if (d == c) {
                    streamFid = a[d];
                    break
                }
            if ("" == streamFid)
                return "";
            c = f.cg_fun(streamFid);
            a = c.slice(0, 8);
            b = b.toString(16);
            1 == b.length && (b = "0" + b);
            b = b.toUpperCase();
            c = c.slice(10, c.length);
            return a + b + c
        }
        T.prototype.getVideoSrc = function(a, c, e, f, i, g) 
        {
            if (!c.videoid || !e)
                return "";
            var h = {flv: 0,flvhd: 0,mp4: 1,hd2: 2,"3gphd": 1,"3gp": 0}[e], p = {flv: "flv",mp4: "mp4",hd2: "flv","3gphd": "mp4","3gp": "flv"}[e], k = a.toString(16)
;
            1 == k.length && (k = 
            "0" + k);
            var l = c.segs[e][a].seconds, a = c.segs[e][a].k;
            this.tmp3 = l
            if ("" == a || -1 == a)
                a = c.key2 + c.key1;
            e = "";
            ip = c.ip
            c.show && (e = c.show.show_paid ? "&ypremium=1" : "&ymovie=1");
            c = "/player/getFlvPath/sid/" + this._sid + "_" + k + "/st/" + p + "/fileid/" + f + "?K=" + a + "&hd=" + h + "&myp=0&ts=" + l + "&ypp=0" + e;
            this.tmp4=c
            //f = encodeURIComponent(E(F(G("boa4poz1", [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]).toString(), this._sid + "_" + f + "_" + this._token)));
            f = encodeURIComponent(Ee(F(G("boa4poz1", [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]).toString(), this._sid + "_" + f + "_" + this._token)));
            c = c + ("&ep=" + f) + "&ctype=12&ev=1" + ("&token=" + this._token);
            //c += "&oip=" + b.v.data[0].ip;
            c += "&oip=" + ip;
            return "http://k.youku.com" + (c + ((i ? "/password/" + i : "") + (g ? g : "")))
        }
    //}
    //};

    //injson = eval(sinjson)
    //injson = eval(sinjson.options)
    injson = JSON.parse(sinjson);
    //return injson["ep"]
    //injson["ep"] = "PwXTSA8aL7nd1PLE8+JxB9H8uBI71wnIWBg="
    strna = pa(injson["ep"])
    //return strna
    
    videotype = ""
    videoinfo = injson["streamfileids"]//get videotype:flv/mp4/hd2...

    tq = {"flv":"flv","mp4":"mp4","hd2":"flv","3gphd":"mp4","3gp":"flv"}
    types = ["mp4","flv","hd2","3gp"]
    typeslen = types.length 

    for (i=0;i<types.length;i++)
    {
        if (types[i] in videoinfo)
        {
            videotype = types[i]
            break;
        }
    }

    //return videotype

    para = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]
    var f1 = "b4eto0b4"
    //G is F
    strg = G(f1,para)
    //return strg
    //return strg.length+":"+strna.length
    stre = F(strg,strna)
    sid = stre.split("_")[0]
    token = stre.split("_")[1]
    total_time = parseInt(injson["seconds"])

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
    info = tt.get_info()
    urls = tt.get_urls()
    return urls

    //var b = new U(injson["seed"]);
    //var b = new U(7187);
    //var info = b.get_info()
    return info+""
    
    return "122"

}
)
