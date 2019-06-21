"""仍然使用尝试1中的数据处理方式，但此次将搜集到的前100个python文件导入到模型中"""

#分隔符切分实验
#此代码可以作为one-hot编码前的一次数据预处理

import re
def pre_process(filename):
    file = open(filename,'r',encoding='utf-8')
    strings = file.read()
    strings = re.split('([ ,.\n()=])',strings)


    while ' ' in strings:
        strings.remove(' ')
    while '' in strings:
        strings.remove('')
    strings = ' '.join(strings)
    return strings

text = ''
filename = ''
for i in range(100):
    filename = 'data\\' + str(i) + '.txt'
    text += pre_process(filename)
# print(text[:1000])

# 将字符串序列向量化
import numpy as np

maxlen = 60
step = 5
sentences = []
next_chars = []

for i in range(0, len(text[:1000]) - maxlen, step):
    sentences.append(text[i:i + maxlen])
    next_chars.append(text[i + maxlen])

print('Number of sequences:', len(sentences))

chars = sorted(list(set(text)))
print('Unique characters:', len(chars))
char_indices = dict((char, chars.index(char)) for char in chars)

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)))
y = np.zeros((len(sentences), len(chars)))
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1
# print(x.shape)

#用于预测下一个代码词的单层LSTM模型
import keras
from keras import layers

model = keras.models.Sequential()
#model.add(layers.Embedding(len(chars),128,input_length=maxlen))
model.add(layers.LSTM(128,input_shape=(maxlen,len(chars))))
model.add(layers.Dense(len(chars),activation='softmax'))

optimizer = keras.optimizers.RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy',optimizer=optimizer)
model.summary()

from keras.callbacks import ModelCheckpoint
filepath = "model/Checkpoint_model.hdf5"
checkpoint = ModelCheckpoint(filepath, save_weights_only=False,verbose=1,save_best_only=False, period=1)

#给定模型预测，采样下一个代码词的函数
def sample(preds,temperature=0.1):
    print(preds)
    preds = np.asarray(preds).astype('float')
    preds = np.log(preds) /temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1,preds,1)
    print('---------------------------采样----------------------------------')
    print(probas)
    return np.argmax(probas)


import random
import sys
import os

for epoch in range(1, 50):
    # print('\n' + '---------------------------------------------------------epoch=' + str(
    #     epoch) + '---------------------------------------------------------')

    if os.path.exists(filepath):
        model.load_weights(filepath)
        # print("=================================正在从断点开始续训模型=================================")
        model.fit(x, y, batch_size=128, epochs=1, callbacks=[checkpoint])

    else:
        model.fit(x, y, batch_size=128, epochs=1, callbacks=[checkpoint])

    # 定义随时数，随机数越高，文本生成的创造性越强，规则表示越弱
    for temperature in [0.1, 0.3, 0.5, 0.8]:
        # print('\n' + '------ temperature:' + '\n', temperature)

        for j in range(20):
            if j == 0:
                start_index = random.randint(0, len(text) - maxlen - 1)
                generated_text = text[start_index:start_index + maxlen]

            for i in range(100):
                sampled = np.zeros((1, maxlen, len(chars)))
                for t, char in enumerate(generated_text):
                    sampled[0, t, char_indices[char]] = 1.

                preds = model.predict(sampled, verbose=0)[0]
                next_index = sample(preds, temperature=0.3)
                next_char = chars[next_index]

                generated_text += next_char
                generated_text = generated_text[1:]

                sys.stdout.write(next_char)
                if next_char == '\n':
                    break
