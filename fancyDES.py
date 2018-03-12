#!/usr/bin/python3
from collections import deque
from pprint import pprint
import sbox
import hashlib
import random
import numpy as np

class FancyDES():
    internal_keys = []

    def __init__(self, path=None, message = None, key = None, fromFile = False):
        if (fromFile):
            files = open(path, 'rb')
            self.message = files.read()
        else:
            self.message = message

        self.key = key

    def sub_sbox(self, block, box):
        new_block = np.copy(block)
        for i in range(4):
            for j in range(4):
                # cell = int(block[i][j], 16)
                cell = block[i][j]
                new_block[i][j] = sbox.sub(cell, box)
        return new_block

    def gen_internal_key(self, n_round):
        h = hashlib.sha256()
        h.update(self.key.encode('utf-8'))
        key_hashed = list(h.digest())
        # print (key_hashed, type(key_hashed), len(key_hashed))

        # bagi ganjil-genap, XOR
        odd = np.array(key_hashed[::2])
        even = np.array(key_hashed[1::2])
        # print(type(odd))
        tmp = odd ^ even

        # ubah ke block, tambahin ke internal_keys
        block = np.array([tmp[x:x+4] for x in range(0, len(tmp), 4)])
        self.internal_keys.append(block)
        # print (block)

        # generate other key
        for i in range(n_round - 1):
            new_block = self.sub_sbox(block, sbox.sbox)
            new_block = block ^ new_block
            self.internal_keys.append(new_block)
            block = new_block

        pprint(self.internal_keys)


    def message_to_block(self, message = ''):
        self.block_left = [
            ['0xFF','0xF5', '0xF4', '0xF2'],
            ['0x5F','0x35', '0x24', '0x12'],
            ['0xFF','0xF5', '0xF4', '0x42'],
            ['0x6F','0x55', '0x24', '0x32'],
            ]
        self.block_right = [
            ['0xFF','0xF5', '0xF4', '0xF2'],
            ['0x5F','0x35', '0x24', '0x12'],
            ['0xFF','0xF5', '0xF4', '0x42'],
            ['0x6F','0x55', '0x24', '0x32'],
        ]

    def transpose(self, message = None):
        output = [[message[3-i][j] for i in range(4)] for j in range(4)]
        return output

    def transpose_back(self, message = None):
        output = [[message[i][3-j] for i in range(4)] for j in range(4)]
        return output

    def xor(self, message = None, key = None):
        output = []
        for i in range(4):
            new = []
            for j in range(4):
                temp = int(message[i][j], 16) ^ int(key[i][j], 16)
                new.append('0x{:02X}'.format(temp))
            output.append(new)
        return output

    def shift(self, message = None, key = None):
        output = []
        for i in range(4):
            sum = 0
            item = deque(message[i])
            for num in key[i]:
                sum += int(num,16)
            if (i % 2 == 0):
                item.rotate((sum % 4) * -1)
            else:
                item.rotate(sum%4)
            output.append(list(item))
        return output

    def messageToBlock(self, message = None):
        pos = 0
        out = []
        for i in range(4):
            temp = []
            for j in range(4):
                temp.append('0x{:02X}'.format(ord(message[pos])))
                pos += 1
            out.append(temp)
        # pprint(out)
        return out

    def messageToBlocks(self, n = 0, message = None):
        position = 0
        blocks = []
        for i in range(n):
            block = message[position:position+16]
            blocks.append(self.messageToBlock(block))
            position += 16
        return blocks

    def getBlocks(self):
        # expand to 16 byte each
        temp = self.message
        while len(temp) % 16 != 0:
            temp += '.'
        # if sum of block odd, add one block
        sum_blocks = len(temp) // 16
        if sum_blocks % 2 == 1:
            sum_blocks += 1
            temp += '................'

        print (temp, len(temp))
        blocks = self.messageToBlocks(sum_blocks, temp)
        return blocks

    def blocksToMessage(self, blocks = None):
        message = ''
        for block in blocks:
            for row in block:
                for item in row:
                    convert = chr(int(item,16))
                    message += convert
        return message

    def f_function(self, block = None, key= None):
        xor_result = self.xor(block, key)
        shift_result = self.shift(xor_result, key)
        # subsitusi s-box
        return shift_result

    def generate_chiper(self):
        # tentuin jumlah round via random
        sum = 0
        for i in self.key:
            sum += ord(i)
        random.seed(sum)
        round = random.randint(7,25)

        # ubah message ke block
        self.position = 0
        blocks = self.getBlocks()
        number_of_blocks = len(blocks)

        # TODO: Generate key internal
        key_internal = [
            ['0xFF','0xF5', '0xF9', '0xF2'],
            ['0x5F','0x35', '0x25', '0x12'],
            ['0xFF','0xF5', '0x64', '0x42'],
            ['0x6F','0x55', '0x53', '0x32'],
        ]

        out_blocks = []
        for iter_num in range(number_of_blocks // 2):
            block_left = blocks[iter_num]
            block_right = blocks[iter_num+1]
            #initiate with transpose
            block_left = self.transpose(block_left)
            block_right = self.transpose(block_right)
            # process block
            for i in range(round):
                # Fungsi f terhadap blok kanan
                f_result = self.f_function(block_right, key_internal)
                # xor
                temp = self.xor(block_left, f_result)
                # tukar
                if (i < round - 1):
                    block_left = block_right
                    block_right = temp
                else:
                    block_left = temp
                    block_right = block_right
            block_left = self.transpose_back(block_left)
            block_right = self.transpose_back(block_right)
            out_blocks.append(block_left)
            out_blocks.append(block_right)
        chiper = self.blocksToMessage(out_blocks)
        return chiper

if __name__ == '__main__':
    fancyDES = FancyDES(path='samples/text.txt',key = 'HELLO WORLD! HAHAHHA', fromFile=True)
    # chiper = fancyDES.generate_chiper()
    # print('Encrypted:')
    # print(chiper)
    # fancyDES1 = FancyDES(message=chiper, key = 'HELLO WORLD! HAHAHHA', fromFile=False)
    # plainteks = fancyDES1.generate_chiper()
    # print('Decrypted:')
    # print(plainteks)

    fancyDES.gen_internal_key(7)
    # block = [
    #     ['0xFF','0xF5', '0xF9', '0xF2'],
    #     ['0x5F','0x35', '0x25', '0x12'],
    #     ['0xFF','0xF5', '0x64', '0x42'],
    #     ['0x6F','0x55', '0x53', '0x32'],
    # ]
    # block = fancyDES.sub_sbox(block)
    # for row in block:
    #     for el in row:
    #         print('0x{:02X}'.format(el))
