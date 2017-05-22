class ListUtil(object):
    @staticmethod
    def remove_emtpy(li):
        return [line for line in li if len(line) > 0]

    @staticmethod
    def chunks(li, chunk_size):
        if len(li) < 1 or chunk_size < 1:
            return li
        chunk_size = int(chunk_size)
        for i in range(0, len(li), chunk_size):
            yield li[i: i + chunk_size]

    @staticmethod
    def chunks_by_split(li, max_split):
        """주어진 List를 max_split 수대로 자른다
        :param li: Split 대상 List
        :param max_split: Split 수
        :return Lists in list
        """
        # if max_split < 2:
        #     return li
        min_chunk_size = len(li) // max_split
        max_chunk_size = min_chunk_size + 1

        if min_chunk_size == 0:
            return [li]
        max_chunk_split = len(li) % max_split
        min_chunk_split = max_split - max_chunk_split

        # print('%s * %s + %s * %s = %s ' % (min_chunk_size, min_chunk_split, max_chunk_size, max_chunk_split, len(li)))
        li2 = []
        li2.extend(list(ListUtil.chunks(li[:min_chunk_size * min_chunk_split], min_chunk_size)))
        li2.extend(list(ListUtil.chunks(li[min_chunk_size * min_chunk_split:], max_chunk_size)))
        return li2


if __name__ == '__main__':
    li = list(range(49))
    # li = list(range(49))
    print('li: %s' % li)
    # chunks = ListUtil.chunks(li, 4)

    max_split = 1
    chunks = ListUtil.chunks_by_split(li, max_split)
    print('chunks', chunks, type(chunks))
    for i, chunk in enumerate(chunks, 1):
        print(i, chunk)
