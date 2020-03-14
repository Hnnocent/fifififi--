import jieba
import numpy as np
from gensim.models import word2vec

sentences = word2vec.Text8Corpus('dict.txt')
model = word2vec.Word2Vec(sentences,min_count = 1)
simHigh=input("请输入相似度最大阈值")
simLow=input("请输入相似度最小阈值")

#文本预处理,输入初始文本得到list
def text_clean(test):
    test_jieba = list(jieba.cut(test))

    with open('negative-words.txt', 'r', encoding='UTF-8') as f:
        list_negative = f.read().splitlines()

    test_negative = [item for item in test_jieba if item in list_negative]
    if len(test_negative) / 2 == 0:
        with open('stopwords-chinese.txt', 'r', encoding='UTF-8') as f:
            list_stopwords = f.read().splitlines()

        test_delete = [item for item in test_jieba if item not in list_stopwords]
        return test_delete
    else:
        print("你得零分")

#词向量获取,输入需要相似度对比的词语得到他们的向量
def get_word2vec(word):
    vector = np.array(model[word])
    return vector

#相似度计算，输入两次的词语，计算余弦值
def get_score(w1,w2):
    v1=get_word2vec(w1)
    v2=get_word2vec(w2)
    return float(np.sum(v1 * v2)) / (np.linalg.norm(v1) * np.linalg.norm(v2))


#关键词提取，输入学生答案分词列表，从中获取关键词
def get_keywords(ans):
    d = {}
    for a in ans:
        d[a] = d.get(a,0) + 1
    count = list(d.items())  # 得到list中每个词的出现次数列表

    # 计算学生答案关键词的TF-IDF值
    f = open('IDF.txt', 'r', encoding='utf-8')  # 引用IDF值表
    TI = {}  # 储存有IDF值的关键词
    high = []  # 储存没有IDF值的关键词
    for i in range(len(count)):
        TF = count[i][1] / len(ans) * len(count[i][0])
        flag = 0
        f.seek(0)
        # 对于每个关键词 寻找IDF值
        IDF = 0
        for l in f.readlines():
            l = l.replace('\n', '')
            s = l.split(' ')
            if count[i][0] == s[0]:
                IDF = eval(s[1])
                flag = 1  # 记为找到
                break
        if flag == 1:
            TI[count[i][0]] = TF * IDF
        if flag == 0:
            high.append(count[i][0])
    f.close()
    TI = list(TI.items())
    TI.sort(key=lambda x: x[-1], reverse=True)  # 由高到低排序
    n = int(input('答案关键词数：'))
    x = int(input('多备个数：'))

    print('答案关键词为：', end='')
    keywords = []  # 最终的关键词列表
    for i in range(len(TI)):
        high.append(TI[i][0])  # 将有IDF值的关键词按序添加在优先输出的关键词中
    for i in range(n + x):
        keywords.append(high[i])
    return keywords



## 计算单句得分
## sim是所有关键词的最大相似度的list   simHigh simLow 相似度上下限
## n为关键词数量  s为该句总分
def sentenceScore(sim, s, n):
    s0 = s / n    # s0每个关键词的满分
    senTotal = 0  # 学生答案总分
    s1 = 0        # 该学生关键词得分
    for item in sim:
        if item >= simHigh:
            s1 = s0
        elif item < simLow:
            s1 = 0
        elif simLow <= sim < simHigh:
            s1 = item * s0
        senTotal += s1
    return senTotal

#单句式答案判分,输入标准答案关键词的list和学生答案关键词的list
def DanJu(teaAnswers, stuAnswers):
    sim=[]
    max=0
    for teaAnswer in teaAnswers:
        for stuAnswer in stuAnswers:
            if get_score(stuAnswer,teaAnswer)>max:
                max=get_score(stuAnswer,teaAnswer)
        sim.append(max)

    s = 10
    n = len(teaAnswers)          #关键词数量  实际上应该是直接取提供的标答关键词的数量

    Score=sentenceScore(sim, s, n)
    return Score


tea_Answers=input("请输入标准答案关键词")#输入标准答案关键词list
stu_Answers=input("请输入学生答案")#输入学生答案
#处理学生答案，得到学生答案关键词list
stu_Answers=get_keywords(text_clean(stu_Answers))
score=DanJu(tea_Answers, stu_Answers)
print(score)


###以下是分句的计算模式
'''

##根据答案类型调用各自的算分函数  senNum为句子数量
def decideType(senNum, teaAnswer, stuAnswer):
    if senNum == 1:
        s = DanJu(teaAnswer, stuAnswer)
    else:
        t = Type(teaAnswer, stuAnswer)
        ##总分式
        if t == 1:
            s = ZongFen(teaAnswer, stuAnswer)
        ##并列式
        else:
            s = BingLie(teaAnswer, stuAnswer)
    return s


## 判断并列or总分,输入标准答案和学生答案
def Type(teaAnswer, stuAnswer):
    list_tea = teaAnswer.split('。', -1)
    list_stu = stuAnswer.split('。', -1)

    ##去掉list里面的句号
    for item in list_tea:
        if item == '。':
            list_tea = list_tea.remove('。')
    for item in list_stu:
        if item == '。':
            list_stu = list_stu.remove('。')

    sen1 = list_stu[0]  # 学生答案首句

    del (list_tea[0])  # 剩下的标答分句
    key=[]
    for item in list_tea:
        cut1 = get_keywords(list(jieba.cut(item)))
        a = cut1[0]
        key.append(a)  # key是标答首个关键词的list

    cut2 = get_keywords(list(jieba.cut(sen1)))  # 学生答案关键词

    n = 0
    for item in cut2:
        for j in key:
            if j == item:
                n += 1

    # 总分式
    if n == len(key):
        Type = 1
    # 并列式
    else:
        Type = 0
    return Type


##并列式答案得分
def BingLie(teaAnswer, stuAnswer):
    tea = teaAnswer.split('。', -1)
    stu = stuAnswer.split('。', -1)

    for item in tea:
        if item == '。':
            tea = tea.remove('。')
    for item in stu:
        if item == '。':
            stu = stu.remove('。')

            ##构建学生答案分句关键词的二维数组
    subkey_stu = []
    for i in range(len(stu)):
        subkey_stu.append([])
        key = list(jieba.cut(stu[i]))
        subkey_stu[i].append(key)

    # 老师答案关键词数组
    subkey_tea = []
    for i in range(len(sub_tea)):
        subkey_tea.append([])
        key = list(jieba.cut(item))
        subkey_tea[i].append(key)

    ##各个句子计算得分
    maxS = 0
    Score=0
    for i in subkey_stu:
        list_stu = subkey_stu[i]  # 学生答案的一个分句的关键词list
        for j in subkey_tea:
            list_tea = subkey_tea[j]
            S = cosine(list_stu, list_tea)

            # 学生答案里的一个句子和标答的所有句子去比相似度 找到最大的一组对应
            if maxS < S:
                maxS = S
                index = j  # 记录是标答的哪一个句子 并删除这个句子 之后不再比较这一句
                k = len(subkey_tea)  # 句子数量
                s = 10 / k  # 该句总分
                n = len(list_tea)  # 该分句的关键词个数
                s1 = sentenceScore(maxS, s, n)
            del (subkey_tea[j])
        Score += s1
    return Score

#总分式答案判分过程   暂且假设用句号分割句子
def ZongFen(teaAnswer, stuAnswer):
    list_tea = teaAnswer.split('。',-1)
    list_stu = stuAnswer.split('。',-1)

##去掉list里面的句号
    for item in list_tea:
       if item=='。':
            list_tea=list_tea.remove('。')
    for item in list_stu:
        if item=='。':
            list_stu=list_stu.remove('。')   
            
  
  ##学生答案和标答的总句 关键词
    main_tea= list(jieba.cut(list_tea[0]))
    main_stu= list(jieba.cut(list_stu[0]))
    

  ## 分句list
    sub_tea=list_tea[1:]
    sub_stu=list_stu[1:]

   ##学生答案分句关键词的二维数组      
    subkey_stu=[]
    for i in range(len(sub_stu)):
        subkey_stu.append([])
        key=list(jieba.cut(item))
        subkey_stu[i].append(key)
    
    ##老师答案关键词二维数组 ??
    subkey_tea=[]
    for i in range(len(sub_tea)):
        subkey_tea.append([])
        key=list(jieba.cut(item))
        subkey_tea[i].append(key)
        
        
        
    ##计算主句得分
    mainScore=cosine(main_tea,main_stu)  
    
    ##计算分句得分
    s1=0
    for i in subkey_stu:
        key1=subkey_stu[i][0] #学生答案首个关键词
        key1_list=subkey_stu[i][1:]   #其他关键词的list
        for j in subkey_tea:
            key2=subkey_tea[j][0]
            if key1==key2:
               key2_list=subkey_tea[j][1:]
               sim=cosine(key2_list,key1_list)  #返回一个list 得到相似度最大的lsit
               s0=4      #老师提供
               k=len(sub_tea)    #分句数量
               s=(10-s0)/k       #该句总分
               n= len(key2_list)+1   #该分句的关键词个数
               s1=sentenceScore(sim, s, n, simHigh, simLow)
               subScore+=s1                
    Score=mainScore+subScore
    return Score    
'''

