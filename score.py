import jieba

## 计算单句得分
## sim是所有关键词的最大相似度的list   simHigh simLow 相似度上下限
## n为关键词数量  s为该句总分
def sentenceScore(sim, s, n, simHigh, simLow):
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


##根据答案类型调用各自的算分函数  senNum为句子数量    
def decideType(senNum,teaAnswer, stuAnswer):
    
    if senNum == 1:
        s=DanJu(teaAnswer, stuAnswer)
    else:
        t = Type(teaAnswer, stuAnswer)
        ##总分式
        if t == 1:  
            s=ZongFen(teaAnswer, stuAnswer)
        ##并列式
        else:
            s=BingLie(teaAnswer, stuAnswer)
    return s
    
            


## 判断并列or总分
def Type(teaAnswer, stuAnswer):
    list_tea = teaAnswer.split('。',-1)
    list_stu = stuAnswer.split('。',-1)
    
    ##去掉list里面的句号
    for item in list_tea:
        if item=='。':
            list_tea=list_tea.remove('。')
    for item in list_stu:
        if item=='。':
            list_stu=list_stu.remove('。')       
    
    sen1 = list_stu[0]  # 学生答案首句
    
    del(list_tea[0])  # 剩下的标答分句
    
    for item in list_tea:
        cut1 = list(jieba.cut(item))   
        a = cut1[0]
        key.append(a)                 # key是标答首个关键词的list

    cut2 = list(jieba.cut(sen1) ) # 学生答案关键词

    n=0
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

#单句式答案判分
def DanJu(teaAnswer, stuAnswer):
    list_tea=list(jieba.cut(teaAnswer))
    list_stu=list(jieba.cut(stuAnswer))
    s = 10
    n = len(list_tea)          #关键词数量  实际上应该是直接取提供的标答关键词的数量
    sim=cosine(teaAnswer, stuAnswer)
    Score=sentenceScore(sim, s, n, simHigh, simLow)
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
    
    
##并列式答案得分
def BingLie(teaAnswer, stuAnswer):
    tea = teaAnswer.split('。',-1)
    stu = stuAnswer.split('。',-1)

    for item in ea:
        if item=='。':
            tea=tea.remove('。')
    for item in stu:
        if item=='。':
            stu=stu.remove('。')  
            
            
 ##构建学生答案分句关键词的二维数组     
    subkey_stu=[]
    for i in range(len(stu)):
        subkey_stu.append([])
        key=list(jieba.cut(stu[i]))
        subkey_stu[i].append(key)
        
     #老师答案关键词数组
    subkey_tea=[]
    for i in range(len(sub_tea)):
        subkey_tea.append([])
        key=list(jieba.cut(item))
        subkey_tea[i].append(key)
        
            
##各个句子计算得分   
    maxS=0    
    for i in subkey_stu:
        list_stu=subkey_stu[i]  #学生答案的一个分句的关键词list
        for j in subkey_tea:
            list_tea=subkey_tea[j]
            S=cosine(list_stu,list_tea)   
            
        #学生答案里的一个句子和标答的所有句子去比相似度 找到最大的一组对应
            if maxS<S:   
                maxS=S 
                index=j #记录是标答的哪一个句子 并删除这个句子 之后不再比较这一句
                k=len(subkey_tea)    #句子数量
                s=10/k               #该句总分
                n=len(list_tea)      #该分句的关键词个数
                s1=sentenceScore(maxS, s, n, simHigh, simLow)        
            del(subkey_tea[j])                 
        Score+=s1 
    return Score

