#! /usr/bin/env python
#-*-coding:utf-8-*-
"""
用贝叶斯实现机器学习算法的实现
"""
import os
import time
import jieba
import jieba.posseg as pseg
import re
from math import log10

class data_handle(object):
    
    trainFilePath = "D:\\code\\MachineLearn\\file"  #训练文件路径
    testfilepath = "D:\\code\\MachineLearn\\test"  #测试文件路径
    cutFilePath = "D:\\code\\MachineLearn\\cut"   #分词后文件路径
    stop_word_filePath = "D:\\code\\MachineLearn\\stop.txt"  #停顿词文件完整路径
    time_div = 0 #分词所用时间
    time_make_wordbooks = 0 #构造词典所用时间
    time_train = 0 #训练模型所用时间
    wordbooks = set([])  #所有类别的所有文件词的总和
    wordbooks_list = []  #词典的list集合
    train_vector = []  #模型向量
    train_category_num_list = []
    train_category_vector = []
    
    def div(self, category, filename):
        """对给定类别的一个文件进行分词，并写到对应文件下，这个过程顺便去停顿词"""
        content = open(os.path.join(self.trainFilePath, category, filename),'rb').read().replace(' ','')
        cut_category_path = os.path.join(self.cutFilePath, category)
        if not os.path.exists(cut_category_path):
            os.mkdir(cut_category_path)
        fp_cut_word_w = open(os.path.join(cut_category_path, filename),'wb')
        stop_word = open(self.stop_word_filePath,'rb').read().split('\n')
        print content
        for i in pseg.cut(content):
            print "-------------------"
            print str(i)
            if re.match(r'.*/n$', str(i)) and str(i).split('/')[0] not in stop_word:
                fp_cut_word_w.write(str(i).split('/')[0])    #??
                fp_cut_word_w.write('_')
        fp_cut_word_w.close()
        
    def train_file_div(self):
        """对所有文件进行分词"""
        start = time.time()
        all_category_path = os.listdir(self.trainFilePath)
        for category in all_category_path:
            category_path = os.path.join(self.trainFilePath, category)
            for filename in os.listdir(category_path):
                self.div(category, filename)
        end = time.time()
        self.time_div = start - end
    
    def make_wordbooks(self):
        """根据已切好的所有类别文件，构造词典集合"""
        start = time.time()
        all_category_path = os.listdir(self.cutFilePath)
        for category in all_category_path:
            category_path = os.path.join(self.cutFilePath, category)
            for filename in os.listdir(category_path):
                file_words = open(os.path.join(category_path, filename), "rb").read()
                self.wordbooks = self.wordbooks | set(file_words.split("_")) - set([''])
        end = time.time()
        self.time_make_wordbooks = start - end
    
    def booksSet2list(self):
        self.wordbooks_list = list(self.wordbooks)
    
    def category2vector(self):
        """根据构造好的词典，把每类文件对对应词加和， 转换成向量"""
        start = time.time()
        all_category_path = os.listdir(self.cutFilePath)  #虽然每一次结果一样，但是如果新加入训练集，那么这个顺序就不一定正确了
        for category in all_category_path:
            category_path = os.path.join(self.cutFilePath, category)
            category_vector = [1]*len(self.wordbooks)
            category_words_num = len(all_category_path)
            for filename in os.listdir(category_path):
                print filename
                file_words_list = open(os.path.join(category_path, filename)).read().split("_")
                #接下来对每个文件中的所有词进行遍历
                for word in file_words_list:
                    if word in self.wordbooks:
                        category_vector[self.wordbooks_list.index(word)] += 1
                        category_words_num += 1
            print category_vector
            #每一类别文件遍历完之后，操作其构造训练结果
            for index, value in enumerate(category_vector):
                category_vector[index] = log10( float(value)/category_words_num )
            print "category_vector-----", category_vector
            print "category_words_num-----", category_words_num
            self.train_vector.append(category_vector)  #是按照文件夹下文件list进行添加的
            self.train_category_num_list.append(category_words_num)
        #遍历完所有的文件后，需要导出各个类别出现的概率
        totalNum = sum(self.train_category_num_list)
        for index, value in enumerate(self.train_category_num_list):
            self.train_category_vector.append(log10( float(self.train_category_num_list[index])/totalNum ))
        print self.train_category_vector
        end = time.time()
        self.time_train = end - start
    
    def cutAnd2vec(self, filename):
        """ 对单独的一个文件进行分词、转换成向量，并不保存在文件中 """
        list = [] #测试文本集中所有词语list表
        vector = [0]*len(self.wordbooks)
        #jieba.enable_parallel(4)   #并行处理
        stop_word = open(self.stop_word_filePath,'rb').read()
        content = open(filename, "rb").read().replace(' ','')
        for i in pseg.cut(content):
            if re.match(r'.*/n$', str(i)) and str(i).split('/')[0] not in stop_word:
                list.append(str(i).split('/')[0])
        for word in list:
            if word in self.wordbooks:
                vector[self.wordbooks_list.index(word)] += 1
        return vector
    
    def allTestHandle(self):
        """ 统一处理给出的测试文件夹中所有文件 """
        totalTestNum = len( os.listdir(self.testfilepath) )
        errorNum = 0
        for testfile in os.listdir(self.testfilepath):
            print "testfile-----", testfile
            rightresult = re.split(r"\d+", testfile)[0]
            vector = self.cutAnd2vec(os.path.join(self.testfilepath, testfile))
            result = []
            for n in range(len(self.train_vector)):
                #是按照文件夹中文件的顺序排列的
                #针对这个向量，分别与所有类训练结果相乘，看哪个最大即属于哪个类
                sum = 0
                for index, value in enumerate(vector):
                    sum += value * self.train_vector[n][index]
                sum += self.train_category_vector[n]
                result.append(sum)
            result_category = os.listdir(self.cutFilePath)[result.index( max(result) )]
            if rightresult != result_category:
                errorNum += 1
        print "the error rate is ------", float(errorNum)/totalTestNum
            
    def main(self):
        """ 最终测试函数 """
        self.train_file_div()
        self.make_wordbooks()
        self.booksSet2list()
        self.category2vector()
        self.allTestHandle()
        