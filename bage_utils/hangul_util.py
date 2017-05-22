"""
original: https://github.com/sublee/korean/blob/master/korean/hangul.py
modified: bage79@gmail.com
"""
import re
import traceback
import warnings

from lxml.html.clean import Cleaner


def to_sequence(*sequences):
    def to_tuple(sequence):
        if not sequence:
            return sequence,
        return tuple(sequence)

    return sum(map(to_tuple, sequences), ())


warnings.filterwarnings("ignore", category=FutureWarning, append=1)  # for warning in re
# han_eng_re = re.compile('[^ㄱ-ㅎ가-힣0-9a-zA-Z~!@#=\^\$%&_\+~:\";\',\.?/\(\)\{\}\[\]\\s]')
han_eng_re = re.compile('[^ㄱ-ㅎ가-힣0-9a-zA-Z~!@#=^$%&_+:\";\',.?/(){\}\[\]\\s]')
html_tag_cleaner = Cleaner(allow_tags=[''], remove_unknown_tags=False)


# noinspection PyGlobalUndefined
class HangulUtil(object):
    IS_NOT_HANGUL = -1
    global to_sequence
    CHO_LIST = to_sequence(u'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
    MO_LIST = JUNG_LIST = to_sequence(u'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
    JONG_LIST = to_sequence(u'', u'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')
    JA_LIST = to_sequence(u'ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')

    CHO_JUNG_JONG_LIST = (CHO_LIST, JUNG_LIST, JONG_LIST)
    # print(CHO_JUNG_JONG_LIST)
    JA_RANGE = [ord(c) for c in JA_LIST]
    MO_RANGE = [ord(c) for c in MO_LIST]
    JONG_RANGE = [ord(c) for c in JONG_LIST if len(c) > 0]
    HANGUL_RANGE = range(ord(u'가'), ord(u'힣') + 1)
    HANGUL_LIST = list(set(list(MO_LIST) + list(JA_LIST) + [chr(c) for c in HANGUL_RANGE]))
    HANGUL_LIST.sort()
    HANGUL_FIRST = HANGUL_RANGE[0]

    HANJA_RANGE = range(ord(u'一'), ord(u'龥') + 1)

    ENGLISH_LOWER_RANGE = range(ord(u'a'), ord(u'z') + 1)
    ENGLISH_UPPER_RANGE = range(ord(u'A'), ord(u'Z') + 1)

    del to_sequence

    KEY_ENG_LIST = 'qwertyuiopasdfghjklzxcvbnm' + 'QWERTOP'
    KEY_HAN_LIST = 'ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔㅁㄴㅇㄹㅎㅗㅓㅏㅣㅋㅌㅊㅍㅠㅜㅡ' + 'ㅃㅉㄸㄲㅆㅒㅖ'
    KEY_ENG_TO_HAN = dict(zip(KEY_ENG_LIST, KEY_HAN_LIST))

    @staticmethod
    def remain_han_eng(s):
        """
        한글, 영어, 숫자, 일부 기호만 남기고 제거
        :param s:
        :return:
        """
        return ' '.join(han_eng_re.sub(' ', s).split(' ')).strip()

    @classmethod
    def has_hangul(cls, word: object) -> object:
        """
        :param word: 단어
        :return: 한글 음절을 포함하는지 여부
        """
        try:
            for char in word:
                if ord(char) in cls.HANGUL_RANGE:
                    return True
            return False
        except:
            print(traceback.format_exc())

    @classmethod
    def has_english(cls, word):
        """
        :param word: 단어
        :return: 한글 음절을 포함하는지 여부
        """
        try:
            for char in word:
                if ord(char) in cls.ENGLISH_LOWER_RANGE or ord(char) in cls.ENGLISH_UPPER_RANGE:
                    return True
            return False
        except:
            print(traceback.format_exc())

    @classmethod
    def __char_offset(cls, char):
        """
        :param char: 음절
        :return: offset from u"가".
        """
        if isinstance(char, int):
            offset = char
        else:
            if len(char) != 1:
                return cls.IS_NOT_HANGUL
            if not cls.is_full_hangul(char):
                return cls.IS_NOT_HANGUL
            offset = ord(char) - cls.HANGUL_FIRST
        if offset >= len(cls.HANGUL_RANGE):
            return cls.IS_NOT_HANGUL
        return offset

    @classmethod
    def is_full_hangul(cls, word, exclude_chars='.,'):
        """
        :param exclude_chars: 예외로 둘 문자들 (공백은 기본 포함)
        :param word: 단어
        :return: 모든 음절이 한글인지 여부
        """
        # print('is_full_hangul(%s)' % word)
        # print('is_full_hangul;', id(log), log.level)
        try:
            for char in word:
                if char != ' ' and (char not in exclude_chars) and (ord(char) not in cls.HANGUL_RANGE):
                    return False
            return True
        except:
            print(traceback.format_exc())

    @classmethod
    def is_full_hangul_or_english(cls, word, exclude_chars=''):
        """
        :param exclude_chars: 예외로 둘 문자들 (공백은 기본 포함)
        :param word: 단어
        :return: 모든 음절이 한글인지 여부
        """
        # print('is_full_hangul(%s)' % word)
        # print('is_full_hangul;', id(log), log.level)
        try:
            for char in word:
                if char != ' ' and (char not in exclude_chars) and (ord(char) not in cls.HANGUL_RANGE) and (ord(char) not in cls.ENGLISH_UPPER_RANGE) and (
                            ord(char) not in cls.ENGLISH_LOWER_RANGE):
                    return False
            return True
        except:
            print(traceback.format_exc())

    @classmethod
    def has_hangul(cls, word):
        """
        :param word: 단어
        :return: 한글 음절을 포함하는지 여부
        """
        try:
            for char in word:
                if ord(char) in cls.HANGUL_RANGE:
                    return True
            return False
        except:
            print(traceback.format_exc())

    @classmethod
    def has_hanja(cls, word):
        """
        :param word: 단어
        :return: 한글 음절을 포함하는지 여부
        """
        try:
            for char in word:
                if ord(char) in cls.HANJA_RANGE:
                    return True
            return False
        except:
            print(traceback.format_exc())

    @classmethod
    def is_hangul_char(cls, char):
        """

        :param char: 음절
        :return: 한글 여부
        """
        if len(char) == 0:
            return False

        try:
            if ord(char) in cls.HANGUL_RANGE:
                return True
            return False
        except:
            print(traceback.format_exc())

    @classmethod
    def is_english_char(cls, char):
        """

        :param char: 음절
        :return: 한글 여부
        """
        if len(char) == 0:
            return False

        try:
            if ord(char) in cls.ENGLISH_LOWER_RANGE or ord(char) in cls.ENGLISH_UPPER_RANGE:
                return True
            return False
        except:
            print(traceback.format_exc())

    @classmethod
    def is_hanja_char(cls, char):
        """

        :param char: 음절
        :return: 한글 여부
        """
        if len(char) == 0:
            return False

        try:
            if ord(char) in cls.HANJA_RANGE:
                return True
            return False
        except:
            print(traceback.format_exc())

    @classmethod
    def is_moum(cls, char):
        """
        :param char: 음절
        :return: 모음 여부
        """
        return char in cls.MO_LIST

    @classmethod
    def is_jaum(cls, char):
        """
        :param char: 음절
        :return: 자음 여부
        """
        return char in cls.JA_LIST

    @classmethod
    def is_cho(cls, char):
        """
        :param char: 음절
        :return: 초성 여부
        """
        return char in cls.CHO_LIST

    @classmethod
    def is_jung(cls, char):
        """
        :param char: 음절
        :return: 종성 여부
        """
        return cls.is_moum(char)

    @classmethod
    def is_jong(cls, char):
        """
        :param char: 음절
        :return: 종성 여부
        """
        return char in cls.JONG_LIST

    @classmethod
    def get_cho(cls, char):
        """
        :param char: 음절
        :return: 초성
        """
        if cls.is_cho(char):
            return char
        # offset = int(__char_offset(char))
        # if offset == IS_NOT_HANGUL:
        #     return char
        elif cls.is_jung(char) or cls.is_jong(char):
            return ''
        return cls.CHO_LIST[int(cls.__char_offset(char) / int(len(cls.MO_LIST) * len(cls.JONG_LIST)))]

    @classmethod
    def get_jung(cls, char):
        """
        :param char: 음절
        :return: 중성
        """
        if cls.is_jung(char):
            return char
        elif cls.is_cho(char) or cls.is_jong(char):
            return ''
        return cls.MO_LIST[int(cls.__char_offset(char) / int(len(cls.JONG_LIST)) % len(cls.MO_LIST))]

    @classmethod
    def get_jong(cls, char):
        """
        :param char: 음절
        :return: 종성
        """
        if cls.has_jung(char) and cls.is_jong(char):
            return char
        elif cls.is_cho(char) or cls.is_jung(char):
            return ''
        return cls.JONG_LIST[cls.__char_offset(char) % len(cls.JONG_LIST)]

    @classmethod
    def has_cho(cls, char):
        """
        :param char: 음절
        :return: 초성을 포함하는지 (사용할 일이 있을까?)
        """
        if len(char) > 1:
            char = char[-1]
        return True if len(cls.get_cho(char)) else False

    @classmethod
    def has_jung(cls, char):
        """
        :param char: 음절
        :return: 중성을 포함하는지
        """
        if len(char) > 1:
            char = char[-1]
        return True if len(cls.get_jung(char)) else False

    @classmethod
    def has_jong(cls, char):
        """
        :param char: 음절
        :return: 종성을 포함하는지
        """
        if len(char) > 1:
            char = char[-1]
        return True if len(cls.get_jong(char)) else False

    @classmethod
    def split_char(cls, char):
        """
        :param char: 음절
        :returns: tuple(초성, 중성, 종성)
        """
        offset = cls.__char_offset(char)

        cho = cls.get_cho(offset)
        jung = cls.get_jung(offset)
        jong = cls.get_jong(offset)
        # chars = []
        # if i != '':
        #     chars.append(i)
        # if v != '':
        #     chars.append(v)
        # if f != '':
        #     chars.append(f)
        # return chars
        return cho, jung, jong

    @classmethod
    def join_char(cls, cho, jung, jong=''):
        """
        :param jong: 초성
        :param jung: 중성
        :param cho: 종성
        :return: 음절
        """
        if not (cho and jung):
            return cho or jung

        indexes = [tuple.index(*args) for args in zip(cls.CHO_JUNG_JONG_LIST, (cho, jung, jong))]
        offset = (indexes[0] * len(cls.MO_LIST) + indexes[1]) * len(cls.JONG_LIST) + indexes[2]
        return chr(cls.HANGUL_FIRST + offset)

    @classmethod
    def join_suffix(cls, char, jong_suffix):
        """
        :param jong_suffix: 음절
        :param char: 종성이면서 접미사 (ㄴ, ㄹ, ....)
        :return: 음절
        """
        cho, jung, jong = cls.split_char(char)
        if cho != '' and jung != '' and jong == '':
            return cls.join_char(cho, jung, jong_suffix)
        else:
            return ''.join([char, jong_suffix])

    @classmethod
    def split_string(cls, word):
        """
        :param word: 단어
        :return: list(음절)
        """
        li = []
        for char in word:
            if cls.is_full_hangul(char):
                li.extend(cls.split_char(char))
            else:
                li.append(char)
        return li

    @classmethod
    def join_string(cls, char_list):
        """
        :param char_list: list(음절)
        :return: 단어
        """
        letters = []
        i = len(char_list) - 1
        try:
            while i >= 0:
                if cls.is_jong(char_list[i]):
                    try:
                        letters.insert(0, cls.join_char(char_list[i - 2], char_list[i - 1], char_list[i]))
                        i -= 3
                    except:
                        try:
                            letters.insert(0, cls.join_char(char_list[i - 1], char_list[i]))
                            i -= 2
                        except:
                            letters.insert(0, char_list[i])
                            i -= 1
                elif cls.is_jung(char_list[i]):
                    try:
                        letters.insert(0, cls.join_char(char_list[i - 1], char_list[i]))
                        i -= 2
                    except:
                        letters.insert(0, char_list[i])
                        i -= 1
                else:
                    letters.insert(0, char_list[i])
                    i -= 1
            return u''.join(letters)
        except:
            return None

    # noinspection PyPep8Naming
    @classmethod
    def qwerty_to_hangul(cls, word):
        chars = []
        for char in word:
            if char in cls.KEY_ENG_TO_HAN:
                chars.append(cls.KEY_ENG_TO_HAN[char])
            else:
                chars.append(char)
        hangul = cls.join_string(chars)
        if hangul:
            return hangul
        else:
            return word  # convert failed

    @staticmethod
    def get_except_hangul(value):
        """한글을 제외한 문자열을 리턴함"""
        chars = ''
        for i in value:
            if not HangulUtil.is_hangul_char(i):
                chars += i
        return chars

    @staticmethod
    def get_except_english(value):
        """영어를 제외한 문자열을 리턴함"""
        chars = ''
        for i in value:
            if not HangulUtil.is_english_char(i):
                chars += i
        return chars


if __name__ == '__main__':
    # for ch in HangulUtil.HANGUL_RANGE:
    #     print(chr(ch), )
    print(HangulUtil.HANGUL_LIST)
    # print(HangulUtil.ENGLISH_LOWER_RANGE)
    # print(HangulUtil.ENGLISH_UPPER_RANGE)
    # print(HangulUtil.has_english('한f ㅎㅎㅎㅎㅎ'))
    # print('ㅌㅌㅌㅌ')
    # print('%s, %s, %s' % (HangulUtil.get_cho('ㄹ'), HangulUtil.get_jung('ㄹ'), HangulUtil.get_jong('ㄹ')))
    # print('%s, %s, %s' % (HangulUtil.get_cho('ㅏ'), HangulUtil.get_jung('ㅏ'), HangulUtil.get_jong('ㅏ')))
    # print('%s, %s, %s' % (HangulUtil.get_cho('라'), HangulUtil.get_jung('라'), HangulUtil.get_jong('라')))
    # print('%s, %s, %s' % (HangulUtil.get_cho('란'), HangulUtil.get_jung('란'), HangulUtil.get_jong('란')))
    # print(HangulUtil.has_jung('ㄹ'))
    # print(HangulUtil.is_full_hangul('하 바'))
    # print(HangulUtil.has_hanja('벌크선社'[-1]))
    # print(HangulUtil.has_hanja('수출입銀'[-1]))
    # print(HangulUtil.is_full_hangul('합병한다.'))
    # print(HangulUtil.is_full_hangul('차세대-폐렴구균백신'))
    # print(HangulUtil.is_full_hangul_or_english("""[헤럴드경제=박혜림 기자] '오늘의 날씨'만 철썩같이 믿고 어제보다 덜 추운 줄 알고 얇게 입고 나왔다가 낭패보신 경험 있으시죠?""", exclude_chars="""=[]\"'.?!"""))
    # print(HangulUtil.is_full_hangul_or_english("""[헤럴드경제=박혜림 기자] '오늘의 날씨'만 철썩같이 믿고 어제보다 덜 추운 줄 알고 얇게 입고 나왔다가 낭패보신 경험 있으시죠?""", exclude_chars="""\"'.?!"""))
