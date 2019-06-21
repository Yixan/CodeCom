# keras module for building LSTM
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.utils as ku
from keras.callbacks import ModelCheckpoint
from tensorflow import set_random_seed
from numpy.random import seed
import numpy as np
import string, os
import warnings
import json

warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)
# filePath="data1\\"
savePath = "model\\CheckpointModel_2.h5"
fileName='data2.txt'
tokenizer=None
total_words=None
max_sequence_len=None

def main():
    set_random_seed(100)
    seed(1)
    global tokenizer
    tokenizer = Tokenizer()
    corpus = []
    # for filename in os.listdir(filePath):
    #     with open(filePath + filename, 'r', encoding="utf-8") as file:
    #         for line in file.readlines():
    #             if not line == None and len(line) <= 50:
    #                 corpus.append(line)
    with open(fileName, 'r', encoding="utf-8") as file:
        for line in file.readlines():
            if not line == None and len(line) <= 60:
                corpus.append(line)

    inp_sequences, total_words = get_sequence_of_tokens(corpus)
    predictors, label, max_sequence_len = generate_padded_sequences(inp_sequences, total_words)
    # print(max_sequence_len)
    model = create_model(max_sequence_len)
    model.summary()
    checkpoint = ModelCheckpoint(savePath,
                                 monitor='val_loss', save_weights_only=False, verbose=1,
                                 save_best_only=False, period=1)
    if os.path.exists(savePath):
        model.load_weights(savePath)
        # 若成功加载前面保存的参数，输出下列信息
        print("checkpoint_loaded")
    else:
        pass
        # os.mkdir('model')
    model.fit(predictors, label, epochs=11, verbose=5,callbacks=[checkpoint])
    f = open('para_dict.json', 'w')
    para_dict={'total_words':total_words,'max_sequence_len': max_sequence_len}
    json.dump(para_dict, f)
    f.close()


def get_sequence_of_tokens(corpus):
    global tokenizer
    tokenizer.fit_on_texts(corpus)
    fp = open('word_dict.json', 'w')
    json.dump(tokenizer.word_index, fp)
    fp.close()
    global total_words
    total_words = len(tokenizer.word_index) + 1

    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        # print(token_list)
        for i in range(1, len(token_list)-2):
            n_gram_sequence = token_list[:i + 3]
            # yield n_gram_sequence
            input_sequences.append(n_gram_sequence)

    return input_sequences, total_words

def generate_padded_sequences(input_sequences,total_words):
    global max_sequence_len
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
    predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
    print(predictors)
    label = ku.to_categorical(label, num_classes=total_words)
    return predictors, label, max_sequence_len

def create_model(max_sequence_len):
    input_len = max_sequence_len - 1
    model = Sequential()
    # Add Input Embedding Layer
    model.add(Embedding(total_words, 10, input_length=input_len))
    # Add Hidden Layer 1 - LSTM Layer
    model.add(LSTM(100))
    model.add(Dropout(0.1))
    # Add Output Layer
    model.add(Dense(total_words, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

def generate_text(seed_text, next_words, model, max_sequence_len):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        print(token_list)
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted = model.predict_classes(token_list, verbose=0)

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text

if __name__ == '__main__':
    main()







