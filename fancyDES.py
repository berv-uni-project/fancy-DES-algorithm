from collections import deque
import random

class FancyDES():

    def __init__(self, path=None, message = None, key = None, fromFile = False):
        if (fromFile):
            files = open(path, 'r')
            self.message = files.read()   
        else:
            self.message = message
        
        self.key = key

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
        sum = 0
        for i in self.key:
            sum += ord(i)
        random.seed(sum)
        round = random.randint(1,25)
        if round < 7:
            round = 7
        self.position = 0
        blocks = self.getBlocks()
        number_of_blocks = len(blocks)
        
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
                block_left = block_right
                block_right = temp
            out_blocks.append(block_left)
            out_blocks.append(block_right)
        chiper = self.blocksToMessage(out_blocks)
        return chiper

if __name__ == '__main__':
    key_internal = [
            ['0xFF','0xF5', '0xF9', '0xF2'],
            ['0x5F','0x35', '0x25', '0x12'],
            ['0xFF','0xF5', '0x64', '0x42'],
            ['0x6F','0x55', '0x53', '0x32'],
        ]
    block_right = [
        ['0xFF','0xF5', '0xF4', '0xF2'],
        ['0x5F','0x35', '0x24', '0x12'],
        ['0xFF','0xF5', '0xF4', '0x42'],
        ['0x6F','0x55', '0x24', '0x32'],
    ]
    fancyDES = FancyDES(path='samples/text.txt',key = 'HELLO WORLD! HAHAHHA', fromFile=True)
    #print(fancyDES.shift(message=block_right,key=key_internal)) 
    #print(fancyDES.transpose(block_right))
    #print(fancyDES.xor(block_right, key_internal))
    print(fancyDES.generate_chiper())