import jieba

test = "物流系统不是信息系统"
test_jieba = list(jieba.cut(test))

with open('negative-words.txt', 'r', encoding='UTF-8') as f:
    list_negative = f.read().splitlines()

test_negative = [item for item in test_jieba if item in list_negative]
if len(test_negative)/2==0:
    with open('stopwords-chinese.txt', 'r', encoding='UTF-8') as f:
        list_stopwords = f.read().splitlines()

    test_delete = [item for item in test_jieba if item not in list_stopwords]

    print(test_delete)
    print(test_negative)
    print(test_jieba)
else:
    print("0")
