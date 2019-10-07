# 构建数据集

import torch
from torch.utils.data import Dataset

import re
import random
import string
import unicodedata

SOS_token = 0
EOS_token = 1
MAX_LENGTH = 10


class Lang(object):
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0:"SOS", 1:"EOS"}
        self.n_words = 2
        
    def addSentendce(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)
            
    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


# 定义字符串编码格式转换函数，将unicode编码（一个字符占两个字节）转换为ASCII编码（一个字符占1个字节）
def unicodeToAscii(s):
    # unicodedata.normalize('NFD',s):将unicode字符串s按照‘NFD’转化成标准形式ASCII形式，去除ASCii没有的字符
    # unicodedata.category(c): 返回字符c在UNICODE里分类的类型,'Mn'是一种类型
    return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c) != 'Mn')


def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    # 将s中的([.!?])符号替换为” \l"
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s

def readLangs(lang1, lang2, reverse=False):
    """
    函数主要是处理得到pairs，
    未对lang1和lang2做任何处理，而是直接用Lang类封装成对象
    """
    print("Reading lines...")
    
    # 读入数据
    print(lang1, lang2)
    lines = open('./data/{}-{}.txt'.format(lang1, lang2), encoding='utf8').read().strip().split('\n')
    
    # 将文本分成eng-fra语言对，应该是列表的列表
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]
    
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)
        
    return input_lang, output_lang, pairs


# 简化数据集，选择特定前缀求长度小于MAX_LENGTH的数据集
eng_prefixes = ("i am ", "i m ", "he is", "he s ", "she is", "she s",
                "you are", "you re ", "we are", "we re ", "they are",
                "they re ")

def filterPair(p):
    return len(p[0].split(' ')) < MAX_LENGTH and len(p[1].split(' '))< MAX_LENGTH and p[1].startswith(eng_prefixes)

def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

def prepareData(lang1, lang2, reverse=False):
    input_lang, output_lang, pairs = readLangs(lang1, lang2, reverse)
    print("Read {} sentence pairs".format(len(pairs)))
    pairs = filterPairs(pairs)
    print("Trimmed to {} sentence pairs".format(len(pairs)))
    print("counting words...")
    for pair in pairs:
        input_lang.addSentendce(pair[0])
        output_lang.addSentendce(pair[1])
    print("Counted words:")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    print(random.choice(pairs))
    return input_lang, output_lang, pairs

def indexesFromSentence(lang, sentence):
    # 返回句子中单词的编号列表
    return [lang.word2index[word] for word in sentence.split(' ')]

def tensorFromSentence(lang, sentence):
    '''将indexes加一个EOS，然后转换成LongTensor类型返回'''
    # indexes类型是什么，长什么样：列表类型，sentence中词的编号
    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    result = torch.LongTensor(indexes)
    return result

def tensorFromPair(input_lang, output_lang, pair):
    input_tensor = tensorFromSentence(input_lang, pair[0])
    target_tensor = tensorFromSentence(output_lang, pair[1])
    return input_tensor, target_tensor

class TextDataset(Dataset):
    def __init__(self, dataload=prepareData, lang=['eng', 'fra']):
        self.input_lang, self.output_lang, self.pairs = dataload(lang[0], lang[1], reverse=True)
        self.input_lang_words = self.input_lang.n_words
        self.output_lang_words = self.output_lang.n_words
        
    def __getitem__(self, index):
        return tensorFromPair(self.input_lang, self.output_lang, self.pairs[index])

    
    def __len__(self):
        return len(self.pairs)


# 调试
if __name__ == '__main__':
    input_lang = Lang('fra')
    output_lang = Lang('eng')
    dataset = TextDataset()