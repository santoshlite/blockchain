#!/usr/bin/python
# -*- coding: utf-8 -*-

#to use sha256 hash for the blockchain
from hashlib import sha256

#Takes in any number of arguments and produces a sha256 hash as a result
def updatehash(*args):
    hashing_text = ""; h = sha256()

    #loop through each argument and hash
    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

#The "node" of the blockchain. Points to the previous block by its unique hash in previous_hash.
class Block():
    data = None
    hash = None
    nonce = 0
    previous_hash = "0"*64
    #default data for block defined in constructor. Minimum specified should be number and data.
    def __init__(self, data, number=0):
        self.data = data
        self.number = number


    #returns a sha256 hash for the block's data. Function instead of variable in constructor
    #to avoid corruption of the variable.
    def hash(self):
        return updatehash(
            self.number,
            self.previous_hash,
            self.data,
            self.nonce
        )

    #returns a string of the block's data. Useful for diagnostic print statements.
    def __str__(self):
        return str("Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce
            )
        )


#The "LinkedList" of the blocks-- a chain of blocks.
class Blockchain():
    #the number of zeros in front of each hash
    difficulty = 4

    #restarts a new blockchain or the existing one upon initialization
    def __init__(self, chain=[]):
        self.chain = chain

    #add a new block to the chain
    def add(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.append(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass
        while True:
            if block.hash()[:self.difficulty] == "0"*self.difficulty:
                self.add(block);break
            else:
                block.nonce +=1

    def isValid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            if _previous != _current or _current[:self.difficulty] != "0"*self.difficulty:
                return False
            return True


#for testing purposes
def main():
    blockchain = Blockchain()
    database = ["hey", "it's me", "cool", "vbucks"]

    num = 0
    for data in database:
        num +=1
        blockchain.mine(Block(data,num))

    for block in blockchain.chain:
        print(block)

    print(blockchain.isValid())

if __name__ == '__main__':
    main()
