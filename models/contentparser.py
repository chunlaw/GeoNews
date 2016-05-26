# encoding=utf-8
import jieba
import jieba.posseg
import os

class ContentParser:

    def __init__(self, diction=None, content=None):
        self.diction = diction or "assets/location.dict"
        self.content = content or ""
        jieba.load_userdict(self.diction)

    def getLocations(self):
        seg_list = jieba.posseg.cut( self.content )
        ns = []
        lastNs = False
        for i in seg_list:
            if i.flag == 'nnl':
                print (i.word)
                if lastNs:
                    ns[-1] += i.word
                else:
                    ns.append( i.word )
                lastNs = True
            else:
                lastNs = False
        return ns

    def setContent(self, content):
        self.content = content

    def test(self):
        self.setContent ( "馬屎埔村收地行動停工兩日後，日本 東京 天水圍天瑞" )
        print ( self.getLocations () )
        self.setContent ( "日本 天津 東京大阪")
        print ( self.getLocations () )
        self.setContent ( "清晨5時許，跑馬地司徒拔道47A一個單位，一名21歲姓許青年，被外籍女傭發現不適，隨即昏迷，連忙報警。救護員到場將事主送院搶救，但終於不治。")
        print ( self.getLocations () )
        return "hi"
