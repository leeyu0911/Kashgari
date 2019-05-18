# encoding: utf-8

import os
import pandas as pd
import kashgari.macros as k
from typing import Tuple, List
from tensorflow.python.keras.utils import get_file
from kashgari import utils

CORPUS_PATH = os.path.join(k.DATA_PATH, 'corpus')


class ChineseDailyNerCorpus(object):
    """
    Chinese Daily New New Corpus
    https://github.com/zjy-ucas/ChineseNER/
    """
    __corpus_name__ = 'china-people-daily-ner-corpus'
    __zip_file__name = 'http://storage.eliyar.biz/corpus/china-people-daily-ner-corpus.tar.gz'

    @classmethod
    def load_data(cls,
                  subset_name: str = 'train',
                  shuffle: bool = True) -> Tuple[List[List[str]], List[List[str]]]:
        """
        Load dataset as sequence labeling format, char level tokenized

        features: ``[['海', '钓', '比', '赛', '地', '点', '在', '厦', '门', ...], ...]``

        labels: ``[['O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-LOC', 'I-LOC', ...], ...]``

        Sample::

            train_x, train_y = ChineseDailyNerCorpus.load_data('train')
            test_x, test_y = ChineseDailyNerCorpus.load_data('test')

        Args:
            subset_name: {train, test, valid}
            shuffle: should shuffle or not, default True.

        Returns:
            dataset_features and dataset labels
        """
        corpus_path = get_file(cls.__corpus_name__,
                               cls.__zip_file__name,
                               cache_dir=k.DATA_PATH,
                               untar=True)

        if subset_name == 'train':
            file_path = os.path.join(corpus_path, 'example.train')
        elif subset_name == 'test':
            file_path = os.path.join(corpus_path, 'example.test')
        else:
            file_path = os.path.join(corpus_path, 'example.dev')

        x_data, y_data = [], []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            x, y = [], []
            for line in lines:
                rows = line.split(' ')
                if len(rows) == 1:
                    x_data.append(x)
                    y_data.append(y)
                    x = []
                    y = []
                else:
                    x.append(rows[0])
                    y.append(rows[1])
        if shuffle:
            x_data, y_data = utils.unison_shuffled_copies(x_data, y_data)
        return x_data, y_data


class SMP2018ECDTCorpus(object):
    """
    https://worksheets.codalab.org/worksheets/0x27203f932f8341b79841d50ce0fd684f/

    This dataset is released by the Evaluation of Chinese Human-Computer Dialogue Technology (SMP2018-ECDT)
    task 1 and is provided by the iFLYTEK Corporation, which is a Chinese human-computer dialogue dataset.
    sample::

              label           query
        0   weather        今天东莞天气如何
        1       map  从观音桥到重庆市图书馆怎么走
        2  cookbook          鸭蛋怎么腌？
        3    health         怎么治疗牛皮癣
        4      chat             唠什么
    """

    __corpus_name__ = 'SMP2018ECDTCorpus'
    __zip_file__name = 'http://storage.eliyar.biz/corpus/SMP2018ECDTCorpus.tar.gz'

    @classmethod
    def load_data(cls,
                  subset_name: str = 'train',
                  shuffle: bool = True,
                  cutter: str = 'char') -> Tuple[List[List[str]], List[List[str]]]:
        """
        Load dataset as sequence classification format, char level tokenized

        features: ``[['听', '新', '闻', '。'], ['电', '视', '台', '在', '播', '什', '么'], ...]``

        labels: ``['news', 'epg', ...]``

        Samples::
            train_x, train_y = SMP2018ECDTCorpus.load_data('train')
            test_x, test_y = SMP2018ECDTCorpus.load_data('test')

        Args:
            subset_name: {train, test, valid}
            shuffle: should shuffle or not, default True.
            cutter: sentence cutter, {char, jieba}

        Returns:
            dataset_features and dataset labels
        """

        corpus_path = get_file(cls.__corpus_name__,
                               cls.__zip_file__name,
                               cache_dir=k.DATA_PATH,
                               untar=True)

        if cutter not in ['char', 'jieba', 'none']:
            raise ValueError('cutter error, please use one onf the {char, jeiba}')

        df_path = os.path.join(corpus_path, f'{subset_name}.csv')
        df = pd.read_csv(df_path)
        if cutter == 'jieba':
            try:
                import jieba
            except ModuleNotFoundError:
                raise ModuleNotFoundError("please install jieba, `$ pip install jieba`")
            x_data = [list(jieba.cut(item)) for item in df['query'].to_list()]
        elif 'char':
            x_data = [list(item) for item in df['query'].to_list()]
        y_data = df['label'].to_list()

        if shuffle:
            x_data, y_data = utils.unison_shuffled_copies(x_data, y_data)
        return x_data, y_data


if __name__ == "__main__":
    x, y = ChineseDailyNerCorpus.load_data('train')
    import json
    print(x[:3])
    print(y[:3])
    print("Hello world")