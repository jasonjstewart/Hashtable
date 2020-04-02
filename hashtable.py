#!/usr/bin/env python3
import os, os.path, binascii
from collections import namedtuple
from io import StringIO
from PIL import Image


# a named tuple to hold an individual key and value
# this Node "object" is never seen outside this class
# (e.g. get() returns the value, not the full Node)
Node = namedtuple("Node", ( 'key', 'value' ))

# This is super small because we want to test the loading and print for debugging easier
NUM_BUCKETS = 10


class Hashtable(object):
    '''
    An abstract hashtable superclass.
    '''
    def __init__(self):
        self.buckets = []
        #TODO: initialize the buckets to empty lists
        for item in range(NUM_BUCKETS):
            self.buckets.append([])


    def set(self, key, value):
        '''
        Adds the given key=value pair to the hashtable.
        creates the hash
        '''
        #TODO: store the value by the hash of the key
        self.buckets[self.get_bucket_index(key)].append(Node(key,value))


    def get(self, key):
        '''
        Retrieves the value under the given key.
        Returns None if the key does not exist.
        '''
        #TODO: get the value by the hash of the key
        returnedlist = self.buckets[self.get_bucket_index(key)]
        #returnedlist.index(key)
        for item in returnedlist:
            if item.key == key:
                 return item.value
        
        return ''


    def remove(self, key):
        '''
        Removes the given key from the hashtable.
        Returns silently if the key does not exist.
        '''
        #TODO: remove the value by the hash of the key
        returnedlist = self.buckets[self.get_bucket_index(key)]
        #returnedlist.index(key)
        for item in range(len(returnedlist)):
            if returnedlist[item-1].key == key:
                returnedlist.remove(returnedlist[item-1])
                return ''


    def get_bucket_index(self, key):
        '''
        Returns the bucket index number for the given key.
        The number will be in the range of the number of buckets.
        '''
        # leave this method as is - write your code in the subclasses
        raise NotImplementedError('This method is abstract!  The subclass must define it.')



    ##################################################
    ###   Helper methods

    def __repr__(self):
        '''Returns a representation of the hash table'''
        buf = StringIO()
        for i, bkt in enumerate(self.buckets):
            for j, node in enumerate(bkt):
                buf.write('{:>5}  {}\n'.format(
                    '[{}]'.format(i) if j == 0 else '',
                    node.key,
                ))
        return buf.getvalue()



######################################################
###   String hash table

class StringHashtable(Hashtable):
    '''A hashtable that takes string keys'''


    def get_bucket_index(self, key):
        '''
        Returns the bucket index number for the given key.
        The number will be in the range of the number of buckets.
        This is where the hashing will go
        '''

        #TODO: hash the string and return the bucket index that should be used

        total = 0
        for ch in key:
            total+=ord(ch)
        
        return total % NUM_BUCKETS




######################################################
###   Guid hash table

COUNTER_CHARS = ( 16, 24 )

class GuidHashtable(Hashtable):
    '''A hashtable that takes GUID keys'''

    def get_bucket_index(self, key):
        '''
        Returns the bucket index number for the given key.
        The number will be in the range of the number of buckets.
        '''
        #16, 16
        #TODO: hash the string and return the bucket index that should be used
        total = 0
        for ch in key[COUNTER_CHARS[0]:COUNTER_CHARS[1]]:
            total+=ord(ch)

        return total % NUM_BUCKETS
        # return ord(key[16:16]) % NUM_BUCKETS



######################################################
###   Image hash table

NUM_CHUNKS = 8

class ImageHashtable(Hashtable):
    '''A hashtable that takes image name keys and creates the hash from (some of) the bytes of the file.'''

    def get_bucket_index(self, key):
        '''
        Returns the bucket index number for the given key.
        The number will be in the range of the number of buckets.
        Read Image in, look at png format, a few numbers in the first few bytes that change every file, but png will be the key, take some
        of the bytes
        '''

        #TODO: hash the string and return the bucket index that should be used
        with open(os.getcwd()+'/images/'+key, "rb") as image:
            f = image.read()
            b = bytearray(f)
            total = 0
            for item in range(len(b)):
                total+= b[item] % NUM_BUCKETS


        return total % NUM_BUCKETS
