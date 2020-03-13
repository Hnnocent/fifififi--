import jieba
import numpy as np
from gensim.models import word2vec

sentences = word2vec.Text8Corpus('dict.txt')
model = word2vec.Word2Vec(sentences,min_count = 1)


#文本预处理,输入初始文本得到list
def text_clean(test):
    test_jieba = list(jieba.cut(test))

    with open('negative-words.txt', 'r', encoding='UTF-8') as f:
        list_negative = f.read().splitlines()

    test_negative = [item for item in test_jieba if item in list_negative]

    with open('stopwords-chinese.txt', 'r', encoding='UTF-8') as f:
        list_stopwords = f.read().splitlines()

    test_delete = [item for item in test_jieba if item not in list_stopwords]
    return test_delete

#词向量获取,输入需要相似度对比的词语得到他们的向量
def get_word2vec(word):
    vector = np.array(model[word])
    return vector

#相似度计算，输入两次的向量，计算余弦值
def get_score(v1,v2):
    return float(np.sum(v1 * v2)) / (np.linalg.norm(v1) * np.linalg.norm(v2))


#关键词提取，输入学生答案分词列表，从中获取关键词
def get_keywords(ans):
    d = {}
    for a in ans:
        d[a] = d.get(a, 0) + 1
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






