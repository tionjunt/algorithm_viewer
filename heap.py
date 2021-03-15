from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ListProperty

import math


class HeapWidget(Widget):
    def __init__(self, value=0, **kwargs):
        super().__init__(**kwargs)
        self.tree = []
        self.upper = 0
        self.current = 0
        self.currentMemory = 0

    @property
    def treeHeight(self):
        return int(math.log2(len(self.tree))+1)
    

    def makeHeapNode(self):
        entry = self.ids['entry']
        value = entry.text
        entry.text = ''
        try:
            value = int(value)
            self.addHeapNode(value)
        except:
            pass


    def addHeapNode(self, value):
        newNode = HeapNode(value=value)
        canv = self.ids['heapcanvas']
        self.tree.append(newNode)
        canv.add_widget(newNode)
        self.redraw()
    

    def redraw(self):
        for i, node in enumerate(self.tree):
            posx, posy = self.getPosFor(i)
            node.pos = (posx, posy)
            node.destinationPos = (posx, posy)


    def getPosFor(self, i):
        m = 2 ** (self.treeHeight)
        
        # nodes are assumed to start from 1, not 0
        nodeHeight = int(math.log2(i+1)) + 1
        positionFromLeft = i + 1 - 2**(nodeHeight-1)
        
        gridy = self.treeHeight-nodeHeight-1, 
        gridx = 2**(self.treeHeight-nodeHeight) + positionFromLeft * 2**(self.treeHeight-nodeHeight-1)

        canv = self.ids['heapcanvas']
        gridsizex, gridsizey = canv.size[0]/m, canv.size[1]/(self.treeHeight+1)

        return gridsizex*gridx, gridsizey*gridy

    
    def heapify(self):
        if len(self.tree) <= 1:
            pass
        else:
            self.upper = 0
            self.current = 1
            self.currentMemory = 1
        
            self.animationFlow()


    # animationFlow -> swap -> animationFlow2 -> animationFlow or
    # animationFlow -> animationFlow3 -> animationFlow
    # animationFlow first highlights two nodes by calling reverseColor.
    # If the two nodes are already sorted, animationFlow calls
    # animationFlow3, which will reverseColor and move the index forward
    # because the two nodes are already sorted.
    # If the nodes are not sorted, animationFlow calls swap.
    def animationFlow(self, *args):
        upperNode = self.tree[self.upper]
        currentNode = self.tree[self.current]

        self.reverseColor()

        if upperNode.value <= currentNode.value:
            Clock.schedule_once(self.animationFlow3, 1)
        else:
            Clock.schedule_once(self.swap, 1)
            

    def swap(self, *args):
        upperNode = self.tree[self.upper]
        currentNode = self.tree[self.current]

        # If node.pos is used to designate pos for Animation instead of 
        # destinationPos, two nodes will stop as the middle of them.
        animation1 = Animation(pos=currentNode.destinationPos, t='out_bounce')
        animation2 = Animation(pos=upperNode.destinationPos, t='out_bounce')

        animation2.start(currentNode)
        animation1.start(upperNode)

        self.tree[self.current], self.tree[self.upper] = self.tree[self.upper], self.tree[self.current]
        self.tree[self.current].destinationPos, self.tree[self.upper].destinationPos = self.tree[self.upper].destinationPos, self.tree[self.current].destinationPos

        Clock.schedule_once(self.animationFlow2, 1)
    

    def animationFlow2(self, *args):
        self.reverseColor()
        
        self.indexManager()
    
        if self.current >= len(self.tree):
            return
        
        Clock.schedule_once(self.animationFlow, 1)
    
    
    def animationFlow3(self, *args):
        self.reverseColor()

        self.upper = 0
        
        # Because upper is 0, calling indexManager is enough to
        # move to next node.
        self.indexManager()

        if self.current >= len(self.tree):
            return

        Clock.schedule_once(self.animationFlow, 1)


    def reverseColor(self, *args):
        upperNode = self.tree[self.upper]
        currentNode = self.tree[self.current]
        color = tuple(currentNode.color)

        if color == (0, 0, 0, 1):
            currentNode.color = 1, 1, 1, 1
            currentNode.backgroundColor = 0, 0, 0, 1
            upperNode.color = 1, 1, 1, 1
            upperNode.backgroundColor = 0, 0, 0, 1
        else:
            currentNode.color = 0, 0, 0, 1
            currentNode.backgroundColor = 1, 1, 1, 1
            upperNode.color = 0, 0, 0, 1
            upperNode.backgroundColor = 1, 1, 1, 1


    def indexManager(self):

        # Current node is raised up.
        self.current = self.upper

        # This means the current node is top of the heap, which means 
        # it is in the right position.
        if self.current == 0:
            self.current = self.currentMemory + 1
            self.currentMemory = self.currentMemory + 1
        
        if self.current%2 == 1:
            self.upper = self.current // 2
        else:
            self.upper = self.current // 2 - 1


    def clear(self):
        canv = self.ids['heapcanvas']
        canv.clear_widgets()
        self.tree = []
    

    def on_size(self, *args):
        self.redraw()


class HeapNode(Label):
    backgroundColor = ListProperty([1, 1, 1, 1])
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.text = str(value)
        self.value = value