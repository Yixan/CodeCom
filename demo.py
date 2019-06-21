from keras.preprocessing.text import Tokenizer
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import json
import numpy as np

# total_words = 2058
total_words = 0
# max_sequence_len = 9
max_sequence_len = 0
word_index=dict()
model=None
def init():
    savePath = "model\\CheckpointModel_6-3.h5"
    global  word_index
    word_index = json.load(open('word_dict.json', 'r'))
    para=json.load(open('para_dict.json', 'r'))
    global total_words,max_sequence_len
    total_words=para['total_words']
    max_sequence_len=para['max_sequence_len']
    global model
    model = load_model(savePath)

def find_index(seed_text):
    index_list=[]
    seed_text=seed_text.split()
    for word in seed_text:
        if not word in  word_index:
            index=None
            return

        index_list.append(word_index[word])
    return index_list

def generate_text(seed_text, model, max_sequence_len):
    seed_text=seed_text.replace("("," pareleft",).replace(")"," pareright").replace("."," dot")\
    .replace(","," comma").replace(" \'\'"," quotMark").replace("="," equal").replace(":"," colon")
    # for _ in range(next_words):
    i=0
    while i<=10:
        token_list = find_index(seed_text)
        if token_list==None:
            return "无法预测"
        # print(token_list)
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted= model.predict_classes(token_list, verbose=0)[0]
        # print(type(predicted_list))
        # predicted_list.sort()
        # predicted=predicted_list[-1]
        output_word = ""
        for word, index in word_index.items():
            if index == predicted:
                output_word = word
                break
        if output_word=='eom':
            break
        seed_text += " " + output_word
        i+=1
    return seed_text

def rep(str):
    return str.replace(" pareleft","(",).replace(" pareright",")").replace(" dot",".")\
    .replace(" comma",",").replace(" quotMark ","\'\'").replace(" equal","=").replace(" colon",":")\
    .replace(" quotmark","\'\'")
if __name__ == '__main__':
    init()
    print("输入“exit()”退出")
    while True:
        seed = input("请输入起始单词:\n")
        if seed=='exit()':
            break
        # len = input("请输入句子长度:")
        print(rep(generate_text(seed, model, max_sequence_len)))

