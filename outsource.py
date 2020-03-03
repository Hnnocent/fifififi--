import jieba

test = "铁路运输不得不是一种运输方式。分类管理是通过对储存进行统计，综合、排列、分类，找出主要矛盾、抓住重点进行管理的一种科学有效的管理方法。"
test_jieba = list(jieba.cut(test))

with open('negative-words.txt', 'r', encoding='UTF-8') as f:
    list_negative = f.read().splitlines()

test_negative = [item for item in test_jieba if item in list_negative]

with open('stopwords-chinese.txt', 'r', encoding='UTF-8') as f:
    list_stopwords = f.read().splitlines()

test_delete = [item for item in test_jieba if item not in list_stopwords]


print(test_delete)
print(test_negative)
print(test_jieba)