from collections import deque

class FancyDES():

    def __init__(self, message, key):
        self.message = [
            ['0xFF','0xF5', '0xF4', '0xF2'],
            ['0x5F','0x35', '0x24', '0x12'],
            ['0xFF','0xF5', '0xF4', '0x42'],
            ['0x6F','0x55', '0x24', '0x32'],
        ]

    def shift(self,key = None):
        key_internal = [
            ['0xFF','0xF5', '0xF9', '0xF2'],
            ['0x5F','0x35', '0x25', '0x12'],
            ['0xFF','0xF5', '0x64', '0x42'],
            ['0x6F','0x55', '0x53', '0x32'],
        ]
        print(self.message)
        output = []
        for i in range(4):
            sum = 0
            item = deque(self.message[i])
            for num in key_internal[i]:
                sum += int(num,16)
            print(sum%4)
            if (i % 2 == 0):
                item.rotate((sum % 4) * -1)
            else:
                item.rotate(sum%4)
            output.append(list(item))
        print('\n')
        print(output)        

if __name__ == '__main__':
    fancyDES = FancyDES('HELLO','HELLO')
    fancyDES.shift() 