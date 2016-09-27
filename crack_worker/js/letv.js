(
    function getRequest(e, vid)
    {
        if (typeof(e) != "undefined" && typeof(vid) != "undefined")
            return getKeyParam(e, vid); 
        else
            return getCookieParam(); 

        function getCookieParam()
        {
            for (var e = "", t = 32; t--; )
                e += Math.floor(16 * Math.random()).toString(16);
            return e
        }

        function getKeyParam(e, vid)
        {
            var S2v = {o: function(s, B) {
                return s >> B
            },x: function(s, B) {
                return s ^ B
            },f: function(s, B) {
                return s < B
            },Y: function(s, B) {
                return s > B
            },C: function(s, B) {
                return s != B
            },R: function(s, B) {
                return s !== B
            },h: function(s, B) {
                return s | B
            },b: function(s, B) {
                return s % B
            },z: function(s, B) {
                return s === B
            },X: function(s, B) {
                return s << B
            },Q: function(s, B) {
                return s & B
            },r: function(s, B) {
                return s == B
            },c: function(s, B) {
                return s - B
            }};


            var defi = 2
            var platid = 3
            var isDomain = !0 
            var pname = "MPlayer"
            var supportM3U8 = "0" 
            var forceMp4 = !1
            var location_host = "m.le.com"
            var document_domain = "letv.com"
			var detect_value = 0

            var t = isDomain ? "api.le.com" : "MPlayer" == pname ? "m.le.com" : "117.121.54.104";
            var a, i = "http://" + t + "/mms/out/video/playJsonH5", r = getMmsKey(e);
            var videoType = "" != supportM3U8 && "1" != supportM3U8 || forceMp4 ? "no" : "ios"
            if (1)
                try {
                    a = location_host
                } catch (d) {
                    a = "." + document_domain
                }
            var l = {1: "350",2: "1000",3: "1300",4: "720p"}, c = {platid: 3,splatid: "MPlayer" == pname ? "301" : "304",tss: videoType,id: vid,dvtype: l[defi] || "",accessyx: 1,domain: a,tkey: r,detect:detect_value};
            return JSON.stringify(c)

            function getMmsKey(e)
            {
                var _1 = "b", _2 = "rotateRight", _3 = "x";
				var t = 185025305 
				r = 8
				n = e
                n = rotateRight(n, r);
				var o = S2v[_3](n, t);
				return o
            }

            function rotateRight(e, t)
            {
				var _1 = "Y", _2 = "Q";
				for (var r, n = 0; S2v[_1](t, n); n++)
					r = S2v[_2](1, e), e >>= 1, r <<= 31, e += r;
				return e
            }
        }
    }
)
