IPython = (__doc__ is not None) and ('IPython' in __doc__)
Main    = __name__ == '__main__'

import numpy as np
import random

logging = False

def log(message):
    if logging:
        print(message)

class World:
    def __init__(self,rows,columns):
        self._rows=rows
        self._columns=columns
        self._plane=np.array([None]*(rows*columns)).reshape(rows,columns)
        
    def __repr__(self):
        lines=[i for i in self]
        display=''
        for i in lines:
            display=display+str(i)+'\n'
        return display
    
    def rows(self):
        return self
    
    def columns(self):
        return self
    
    def plane(self):
        return self 
    
    def __getitem__(self, loc):
        return self._plane[loc]
    
    def __setitem__(self, loc, val):
        self._plane[loc] = val
    
    def add(self,item,loc):
        self[loc] = item
        pass
    
    def fetch(self,loc):
        return self._plane[loc]
    
    def remove(self,item,loc):
        self[loc]=None
        pass
    
    def biota(self):
        alive=[]
        [[alive.append(j) for j in i if j != None] for i in self]
        return alive
    pass
	
class Animal:
    def __init__(self,map_,location,breed_interval,icon,been_alive,alive=True,can_breed=False):
        self._icon=icon
        self._been_alive=been_alive
        self._alive=alive
        self._map_=map_
        self._location=location
        self._map_.add(self,location)
        self._breed_interval=breed_interval
        self._can_breed=can_breed
        pass
    
    def __repr__(self):
        return self._icon
         
    def alive(self):
        return self._alive
    
    def _been_alive(self):
        self._been_alive+=1
        return self._been_alive
    
    def map_(self):
        return self._map_
    
    def location(self):
        return self._location
    
    def breed_interval(self):
        return self._breed_interval
    
    def can_breed(self):
        return self._can_breed
    
    def icon(self):
        return self._icon
    
    def wrap(self,choice):
        mapx,mapy=self._map_._plane.shape
        x,y=choice
        if x<0:
            x=(mapx-1)
        if y<0:
            y=(mapy-1)
        if x>(mapx-1):
            x=0
        if y>(mapy-1):
            y=0
        return(x,y)
        
    def move(self):
        if self._alive:
            x,y=self._location
            _moves=[(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)]
            choice=self.wrap(random.choice(_moves))
            if self._map_.fetch(choice) == None:
                self._location=choice
                self._map_.remove(self._icon,(x,y))
                self._map_.add(self,choice)
        pass
    
    def breed(self):
        if (self._been_alive % self.__class__.breed_interval == 0 or self._can_breed):
            self._can_breed=True
            x,y=self._location
            _moves=[(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)]
            
            while self._can_breed and len(_moves) > 0:
                choice=random.choice(_moves)
                _moves.remove(choice)
                choice=self.wrap(choice)
                
                if self._map_.fetch(choice) == None:
                    if type(self) == Fish:
                        Fish(self._map_,choice)
                        self._can_breed=False
                    else:
                        Bear(self._map_,choice)
                        self._can_breed=False
        pass
    pass   
	
class Fish(Animal):
	#ideal icon: u'\U0001f41f'
    def __init__(self,map_,location,been_alive=0,breed_interval=12,icon="FISH"):
        Animal.__init__(self,map_,location,breed_interval,icon,been_alive)
        pass

    def live(self):
        if self._alive:
            self._been_alive+=1
            self.overpop()
            if self._alive:
                self.breed()
            else:
                self._map_.remove('\U0001f41f',self._location)
        else:
            self._map_.remove('\U0001f41f',self._location)
        pass
    
    def overpop(self):
        x,y=self._location
        places=[self.wrap(i) for i in [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)]]
        if len([i for i in places if type(self._map_.fetch(i))==Fish and self._map_.fetch(i)!=self]) >= 2:
            self._map_.remove('\U0001f41f',self._location)
            self._alive=False
        pass
    
class Bear(Animal):
	#ideal icon: u'\U0001f43b'
    survive_without_food=10
    def __init__(self,map_,location,breed_interval=8,icon="BEAR",been_alive=0):
        Animal.__init__(self,map_,location,breed_interval,icon,been_alive)
        self._starvation=0
    pass
    
    def starvation(self):
        return self._starvation
    
    def eat(self):
        x,y=self._location
        places=[self.wrap(i) for i in [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1)]]
        while len(places) > 0:
            choice = random.choice(places)
            if type(self._map_.fetch(choice))==Fish:
                self._map_.remove('\U0001f41f',choice)
                self._starvation=0
                break
            else:
                places.remove(choice)
        pass
    
    def live(self):
        if self._alive:
            self._been_alive+=1
            self._starvation+=1
            self.eat()
            if self._starvation >= Bear.survive_without_food:
                self._alive=False
                self._map_.remove(self._icon,self._location)
            if self._alive:
                self.breed()
        else:
            self._map_.remove(self._icon,self)
        pass
    pass
	
def wbf(nrows, ncols, nbears, nfish):
    new_world=World(nrows,ncols)
    while nbears > 0:
        x=random.randint(0,nrows-1)
        y=random.randint(0,ncols-1)
        if new_world.fetch((x,y))==None:
            Bear(new_world,(x,y))
            nbears-=1
    while nfish > 0:
        x=random.randint(0,nrows-1)
        y=random.randint(0,ncols-1)
        if new_world.fetch((x,y))==None:
            Fish(new_world,(x,y))
            nfish-=1
    return new_world
	
def step_system(world):
    for x in world.biota():
        x.live()
    for x in world.biota():
        x.move()

#wbf(row,col,bears,fish)
w = wbf(10,10,6,25)
n=0
Bear.breed_interval=13
Fish.breed_interval=7
for i in range(40):
    n+=1
    
    print('step:',n,'animals:',len([i._been_alive for i in w.biota()]))
    print(w)
    step_system(w)
    if len(w.biota())==0:
        print('step',n,'all dead.')
        break