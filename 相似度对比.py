
import jieba
import numpy as np

'''

def get_word_vector():
    str1 = input("sentance：")
    str2 = input("answer：")
    cut1 = jieba.cut(str1)#切分答案，取得切分词块
    cut2 = jieba.cut(str2)
    word1 = (','.join(cut1)).split(',')
    word2 = (','.join(cut2)).split(',')
    key_word = list(set(word1 + word2))
    word_vector1 = np.zeros(len(key_word))#建立矩阵（空）
    word_vector2 = np.zeros(len(key_word))
    for i in range(len(key_word)):#求所有向量的值
        for j in range(len(word1)):#求关键词出现的次数
            if key_word[i] == word1[j]:
                word_vector1[i] += 1
        for k in range(len(word2)):#求关键词出现的次数
            if key_word[i] == word2[k]:
                word_vector2[i] += 1
    return word_vector1, word_vector2#返回词向量

def cosine():
    v1, v2 = get_word_vector()
    return float(np.sum(v1 * v2)) / (np.linalg.norm(v1) * np.linalg.norm(v2))#计算余弦值
                                                                            # np.linalg.norm求范式，默认参数是矩阵整体平方开根号
                                                                            # 输出是数字，不会保留矩阵维度特性

print(cosine())
'''
v1=np.array([1,2])
v2=np.array([1,3])
print(float(np.sum(v1 * v2)) / (np.linalg.norm(v1) * np.linalg.norm(v2)))