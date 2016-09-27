import base64
import time
import urllib
import math
import re
class get_url(object):
    def initialize(self):
        self.Z = ["slice", "call", "querySelectorAll", "length", "push", "shift", "indexOf", "document", "innerHTML", "match", "forEach","1f"]
        self.C=1732584193
        self.S=-271733879
        self.M = [self.C , self.S , ~self.C, ~self.S]
        self.A = []
        self.e = None
        self.count = 0
    def K(self,n):
        return true
    def R(self,n, e):
        d1 = n >> 1
        d2=e >> 1
        d3=self.leftmove((d1+d2),1)
        return d3+(n & 1) + (e & 1)
    def reverse(self,alist):
        tmp = list(alist)
        tmp.reverse()
        return "".join(tmp)
            
    def leftmove(self,data,n):
        flag = True
        if data <0:
            flag = False
        data = abs(data)
        bin_str = bin(data)
        bin_str = bin_str.replace('0b','')
        for i in range(n):
            bin_str = bin_str+'0'
        if len(bin_str) < 32:
            if flag:
                return int(bin_str,2)
            return 0-int(bin_str,2)
        s = bin_str[len(bin_str)-32:]
        if s[0] == '1': 
            tmp=''
            s=s[1:]
            #print s
            for i in range(0,len(s)):
                if s[i]=='0':
                    tmp=tmp+'1'
                else:
                    tmp=tmp+'0'
            s = self.reverse(tmp)
            #print s
            tmp=''
            for i in range(len(s)):
                if s[i]=='0':
                    tmp=tmp+'1'
                    tmp=tmp+s[i+1:]
                    break
                else:
                    tmp=tmp+'0'
            s=self.reverse(tmp)
            if flag:
                return 0-int(s,2)
            return int(s,2)
            #print s
        else:
            s=s[1:]
            if flag:
                return int(s,2)
            return 0-int(s,2)
            
    def Logical_shift(self,data,n):
        if data>0 or data==0:
            return data>>n
        data = -data
        s = bin(data)
        s = s.replace('0b','')
        tmp=''
        for i in range(len(s)):
            if s[i]=='1':
                tmp = tmp+'0'
            else:
                tmp = tmp+'1'
        s = self.reverse(tmp)
        tmp=''
        for i in range(len(s)):
            if s[i]=='0':
                tmp=tmp+'1'
                tmp=tmp+s[i+1:]
                break
            else:
                tmp=tmp+'1'
        s=self.reverse(tmp)
        if len(s)<32:
            l=len(s)
            for i in range(0,32-l):
                s='1'+s
        else:
            s=s[len(s)-32:]
        s=s[:32-n]
        return int(s,base=2)
    def out(self):
        print "self.count:",self.count
        #print "self.url:",self.url
        #print "self.mid:",self.mid
        #print "self.vid:" ,self.vid
        print "self.M:" ,self.M   #[self.C , self.S , ~self.C, ~self.S]
        print "self.A:" ,self.A 
        #print "self.e: ",self.e
        #print "self.m:",self.m
        #print "self.n:",self.n
        print "self.M:",self.M
        print "self.C:",self.C
        print "self.S:",self.S
         
    def T(self,r, t, a, o):
        self.count=self.count+1
        #self.out()
        
        #print "r:",r,";t:",t,";a:",a,";o:",o
        if r>0 and r<5:
            if a>=0:
                if t < (self.m<<6):
                    #o = [o[3], R(o[1], (C = R(R(o[0], [o[1] & o[2] | ~o[1] & o[3], o[3] & o[1] | ~o[3] & o[2], o[1] ^ o[2] ^ o[3], o[2] ^ (o[1] | ~o[3])][S = a >> 4]), R(Math.abs(Math.sin(a + 1)) * 4294967296 | 0, A[[a, 5 * a + 1, 3 * a + 5, 7 * a][S] % 16 + (t++ >>> 6)]))) << (S = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21][4 * S + a % 4]) | C >>> 32 - S), o[1], o[2]];
                    o0 = o[0]
                    o1 = o[1]
                    o2 = o[2]
                    o3 = o[3]
                    self.S = a >> 4
                    tmp1 = self.R(o0, [o1 & o2 | ~o1 & o3, o3 & o1 | ~o3 & o2, o1 ^ o2 ^ o3, o2 ^ (o1 | ~o3)][self.S])
                    d = ([a, 5 * a + 1, 3 * a + 5, 7 * a][self.S] % 16) + self.Logical_shift(t,6)
                    t=t+1
                    if len(self.A)>d:
                        tmp2 = self.R(int(abs(math.sin(a+1))*4294967296)-2**32,self.A[d])
                    else:
                        tmp2 = self.R(int(abs(math.sin(a+1))*4294967296)-2**32,0)
                    self.C=self.R(tmp1,tmp2)
                    self.S = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21][4 * self.S + a % 4]
                    data = self.R(o1,self.leftmove(self.C,self.S)|self.Logical_shift(self.C,32-self.S))
                    o = [o3,data,o1,o2]
                    if not (t&63):
                        self.M = [self.R(o[0], self.M[0]), self.R(o[1], self.M[1]), self.R(o[2], self.M[2]), self.R(o[3], self.M[3])]
                        self.T(r, (t+(15 << 6)) , t & 63, self.M)
                    else:
                        self.T(r, t, t & 63, o)
                else:
                    self.A=[]
                    self.m=""
                    self.T(r, 0, -3, o)
            elif a<0 and a>-3:
                if t<len(o):
                    tmp = (t % 4)
                    if len(o)>t: 
                        data = ord(o[t]) << 8 * tmp
                    else:
                        data = 0<<8*tmp
                    num=t>>2
                    if len(self.A) >num:
                        self.A[num] = self.A[num]|data
                    else:
                        length = len(self.A) 
                        for i in range(length,num+1):
                            self.A.append(0)
                        self.A[num] = data
                    t=t+1
                    self.T(3, t, -1, o)
                    
                else:
                    if self.e:
                        self.T(15, t, 0, "93365376061606269313761363066383")
                    else:
                        self.T(15, t, 0, "533333161366433606b3267613265323")
            else:
                if t<32:
                    self.m =self.m + str(hex(self.M[t >> 3] >> (1 ^ t & 7) * 4 & 15)).replace('0x','').replace('L','')
                    t = t+1
                    self.T(r, t, a, o)
                    a = a-1
        elif r > 6 and r < 10:
            if a < len(o) >> 1:
                num = t>>2
                if len(self.A)>num:
                    self.A[num] |= (int(o[(a >> 2) * 8:(((a >> 2) * 8)+8)], 16) >> 8 * (a % 4) & 255 ^ a % 1) << ((t & 3) << 3)
                else:
                    for i in range(len(self.A),num+1):
                        self.A.append(0)
                    self.A[num]=(int(o[(a >> 2) * 8:(((a >> 2) * 8)+8)], 16) >> 8 * (a % 4) & 255 ^ a % 1) << ((t & 3) << 3)
                t = t+1
                self.T(9, t, a + 1, o)
            else:
                self.T(12, t, 0, self.n)
        elif r > 11 and r < 14:
            r= base64.decodestring(urllib.unquote(o))
            if a < len(r):
                num = t>>2
                if len(self.A)>num:
                    self.A[num] |= ord(r[a]) << 8 * (t % 4)
                else:
                    for i in range(len(self.A),num+1):
                        self.A.append(0)
                    self.A[num] = ord(r[a]) << 8 * (t % 4)
                a = a+1
                t = t+1
                self.T(12, t, a, self.n)
            else:
                self.A[t >> 2] |= 1 << (t % 4 <<3) +7
                self.m=(t + 8 >> 6 << 4) + 14
                if len(self.A)>self.m:
                    self.A[self.m] = t << 3
                else:
                    for i in range(len(self.A),self.m+1):
                        self.A.append(0)
                    self.A[self.m] = t<<3
                self.T(3, 0, 0, self.M)
        elif r > 14 and r < 17:
            if a < len(o) >> 1:
                num = t>>2
                data = (int(self.reverse(o[(a >> 2) * 8: ((a >> 2) * 8+8)]), 16) >> 8 * (a % 4) & 255 ^ a % 7) << ((t & 3) << 3)
                if len(self.A) >num:
                    self.A[num] = self.A[num]|data #(int(self.reverse(o[(a >> 2) * 8: ((a >> 2) * 8+8)]), 16) >> 8 * (a % 4) & 255 ^ a % 7) << ((t & 3) << 3)
                else:
                    for i in range(len(self.A),num+1):
                        self.A.append(0)
                    self.A[num] = data
                t =t+1
                self.T(16, t, a + 1, o)
            else:
                if self.e:
                    self.T(7, t, 0, "63663762376362366433633262663465")
                else:
                    self.T(7, t, 0, "64316539343233356235343631663866")
    def get_encode_url(self,local_time):
        self.url = self.url+";2;&tim="+str(local_time)
        self.url = urllib.quote(self.url)
        self.url = urllib.quote(self.url)
        self.url = self.url.replace('/','%252F')
 
    def get_url(self,url,mid,vid):
        self.initialize()
        self.url=url
        self.mid=mid
        self.vid=vid
        local_time = int(time.time()*1000)
        #local_time = 1452737197077
        tk=str(local_time-7)
        self.m=tk
        self.get_encode_url(local_time)
        self.n=urllib.quote(base64.encodestring(self.mid).replace('\n',''))
        self.m = urllib.quote(base64.encodestring(str(self.m)).replace('\n',''))
        self.T(1, 0, -1, base64.decodestring(urllib.unquote(self.m)))
        url = "http://cache.m.iqiyi.com/jp/tmts/"+self.mid+"/"+self.vid+"/?platForm=h5&rate=1&tvid="+self.mid+"&vid="+self.vid+"&cupid=qc_100001_100186&type=mp4&qyid=i86oc4g5j665sc7fr4r5asx3&nolimit=0&agenttype=13&src=d846d0c32d664d32b6b54ea48997a589&sc="+self.m+"&__refI="+self.url+"&qd_wsz=MF8w&t="+tk+"&__jsT=sgve"
        return url
if __name__ == '__main__':
    from time import sleep
    test_cal=get_url()
    while True:
        url = test_cal.get_url('http://www.iqiyi.com/dongman/20130503/053dccbe76571c2d.html',"135053900","c2e517cc018848bb86b044603b298ec7")
        req = urllib.urlopen(url)
        data = req.read()
        req.close
        regex_express ='"code":"(.*?)"'
        regex_pattern = re.compile(regex_express)
        match_result = regex_pattern.search(data)
        if match_result:
            match_result = match_result.groups()[0]
            print match_result
        sleep(1) 
        #break
