'''
Created on Mar 3, 2022

@author: nigel
'''

class Course(object):
    '''
    classdocs
    '''


    def __init__(self, id: str, n: str, cr: str):
        '''
        Constructor
        '''
        self.cid = id
        self.name = n
        self.credits = cr
        
    def __str__(self):
        return 'Course: {}\nName: {}\nCredits: {}'.format(self.cid,self.name, self.credits)