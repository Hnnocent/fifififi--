#TF-IDF算法
ans=eval(input())#设学生答案分词列表为ans

#统计每个词出现次数
d={}
for a in ans:
    d[a]=d.get(a,0)+1
count=list(d.items())#得到list中每个词的出现次数列表

#计算学生答案关键词的TF-IDF值
f=open('IDF.txt','r',encoding='utf-8')#引用IDF值表
TI={}#储存有IDF值的关键词
high=[]#储存没有IDF值的关键词
for i in range(len(count)):
    TF=count[i][1]/len(ans)*len(count[i][0])
    flag=0
    f.seek(0)
    #对于每个关键词 寻找IDF值
    IDF=0
    for l in f.readlines():
        l=l.replace('\n','')
        s=l.split(' ')
        if count[i][0]==s[0]:
            IDF=eval(s[1])
            flag=1#记为找到
            break
    if flag==1:
        TI[count[i][0]]=TF*IDF
    if flag==0:
        high.append(count[i][0])
f.close()
TI=list(TI.items())
TI.sort(key=lambda x:x[-1],reverse=True)#由高到低排序
n=int(input('答案关键词数：'))
x=int(input('多备个数：'))

print('答案关键词为：',end='')
gjc=[]#最终的关键词列表
for i in range(len(TI)):
    high.append(TI[i][0])#将有IDF值的关键词按序添加在优先输出的关键词中
for i in range(n+x):
    gjc.append(high[i])
print(gjc)#输出要求个数的关键词列表




















