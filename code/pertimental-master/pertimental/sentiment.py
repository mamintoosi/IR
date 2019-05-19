import os

import sys
from hazm import Normalizer, sent_tokenize, word_tokenize, Stemmer
from nltk.classify import NaiveBayesClassifier
from sklearn.externals import joblib

# TODO: Dataset should be place in different file(s).
positive_vocab = ['عالی', 'ممتاز', 'شگفت‌انگیز', 'خیلی خوب', 'خوب', 'زیبا', 'عالی', ':)']

negative_vocab = ['بد', 'وحشتناک', 'به‌درد‌نخور', 'تنفر', 'خیلی بد', 'ناراضی', ':(']

neutral_vocab = ['عادی', 'اون', 'این', 'بود', 'هست', 'به', 'است', 'معمولی', 'نیست']


class PersianSentiment:

    def __word_feats(self, words):
        return dict([(word, True) for word in words])
    
    def __train(self):
        positive_features = [(self.__word_feats(pos), 'pos') for pos in positive_vocab]
        negative_features = [(self.__word_feats(neg), 'neg') for neg in negative_vocab]
        neutral_features = [(self.__word_feats(neu), 'neu') for neu in neutral_vocab]
    
        train_set = negative_features + positive_features + neutral_features
    
        model = NaiveBayesClassifier.train(train_set)
        # TODO: Model.pkl should be place in different directories related to package.
        joblib.dump(model, 'Model.pkl')
    
    def __get_model(self):
        # TODO: Model.pkl should be place in different directories related to package.
        if not os.path.exists('Model.pkl'):
            self.__train()
        # TODO: Model.pkl should be place in different directories related to package.
        return joblib.load('Model.pkl')

    def score(self, sentences):
        # Predict
        pos, neg, neu = 0, 0, 0
        stemmer = Stemmer()
        classifier = self.__get_model()
        normalizer = Normalizer()
    
        sentences = sent_tokenize(sentences)
    
        for sentence in sentences:
            sentence = normalizer.normalize(sentence)
            words = word_tokenize(sentence)
    
            for word in words:
                stemmer.stem(word)
                class_result = classifier.classify(self.__word_feats(word))
                if class_result == 'neg':
                    neg = neg + 1
                if class_result == 'pos':
                    pos = pos + 1
    
        positive_sentiment = str(float(pos) / len(words))
        # print('Positive: ' + positive_sentiment)
        neutral_sentiment = str(float(neu) / len(words))
        # print('Neutral: ' + neutral_sentiment)
        negative_sentiment = str(-float(neg) / len(words))
        # print('Negative: ' + negative_sentiment)
    
        total_sentiment = (float(positive_sentiment) +
                           float(negative_sentiment)) / 2
        # print('Total (Avg): ' + str(total_sentiment))
    
        return total_sentiment


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Use python3 predict.py <Your Text>")
        exit(0)
    else:
        print(PersianSentiment().score(sys.argv[1]))
