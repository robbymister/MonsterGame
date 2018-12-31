import pygame

class Actor:
    '''
    Represents an Actor in the game. Can be the Player, a Monster, boxes, wall.
    Any object in the game's grid that appears on the stage, and has an
    x- and y-coordinate.
    '''
    
    def __init__(self, icon_file, stage, x, y, delay=5):
        '''
        (Actor, str, Stage, int, int, int) -> None
        Given the name of an icon file (with the image for this Actor),
        the stage on which this Actor should appear, the x- and y-coordinates
        that it should appear on, and the speed with which it should
        update, construct an Actor object.
        '''
        
        self._icon = pygame.image.load(icon_file) # the image image to display of self
        self.set_position(x, y) # self's location on the stage
        self._stage = stage # the stage that self is on

        # the following can be used to change this Actors 'speed' relative to other
        # actors speed. See the delay method.
        self._delay = delay
        self._delay_count = 0
    
    def set_position(self, x, y):
        '''
        (Actor, int, int) -> None
        Set the position of this Actor to the given x- and y-coordinates.
        '''
        
        (self._x, self._y) = (x, y)

    def get_position(self):
        '''
        (Actor) -> tuple of two ints
        Return this Actor's x and y coordinates as a tuple.
        '''
        
        return (self._x, self._y)

    def get_icon(self):
        '''
        (Actor) -> pygame.Surface
        Return the image associated with this Actor.
        '''
        
        return self._icon

    def is_dead(self):
        '''
        (Actor) -> bool
        Return True iff this Actor is not alive.
        '''
        
        return False

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool

        Other is an Actor telling us to move in direction (dx, dy). In this case, we just move.
        (dx,dy) is in {(1,1), (1,0), (1,-1), (0,1), (0,0), (0,-1), (-1,1), (-1,0), (-1,-1)}
    
        In the more general case, in subclasses, self will determine 
        if they will listen to other, and if so, will try to move in
        the specified direction. If the target space is occupied, then we 
        may have to ask the occupier to move.
        '''

        self.set_position(self._x + dx, self._y + dy)
        return True

    def delay(self):
        '''
        (Actor) -> bool
        Manage self's speed relative to other Actors. 
        Each time we get a chance to take a step, we delay. If our count wraps around to 0
        then we actually do something. Otherwise, we simply return from the step method.
        '''

        self._delay_count = (self._delay_count+1) % self._delay
        return self._delay_count == 0

    def step(self):
        '''
        (Actor) -> None
        Make the Actor take a single step in the animation of the game.
        self can ask the stage to help as well as ask other Actors
        to help us get our job done.
        '''

        pass

class Player(Actor):
    '''
    A Player is an Actor that can handle events. These typically come
    from the user, for example, key presses etc.
    '''

    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Player, str, Stage, int, int) -> None
        Construct a Player with given image, on the given stage, at
        x- and y- position.
        '''
        
        super().__init__(icon_file, stage, x, y)
    
    def handle_event(self, event):
        '''
        Used to register the occurrence of an event with self.
        '''
        
        pass

class KeyboardPlayer(Player):
    '''
    A KeyboardPlayer is a Player that can handle keypress events.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        Construct a KeyboardPlayer. Other than the given Player information,
        a KeyboardPlayer also keeps track of the last key event that took place.
        '''
        
        super().__init__(icon_file, stage, x, y)
        self._last_event = None # we are only interested in the last event
    
    def handle_event(self, event):
        '''
        (KeyboardPlayer, int) -> None
        Record the last event directed at this KeyboardPlayer.
        All previous events are ignored.
        '''

        self._last_event = event

    def step(self):
        '''
        (KeyboardPlayer) -> None
        Take a single step in the animation. 
        For example: if the user asked us to move right, then we do that.
        '''
        if self.GameOver() == True: #JUST PRINTS OUT GAME OVER REPEATEDLY
            self._stage._screen.fill((0,255,255))
            print("Game Over.")
        if self._last_event is not None:
            dx, dy = None, None
            if self._last_event == pygame.K_DOWN:
                dx, dy = 0,1
            if self._last_event == pygame.K_LEFT:
                dx, dy = -1,0
            if self._last_event == pygame.K_RIGHT:
                dx, dy = 1,0
            if self._last_event == pygame.K_UP:
                dx, dy = 0,-1
            if self._last_event == pygame.K_c: #bot right
                dx, dy = 1,1
            if self._last_event == pygame.K_z: #bot left
                dx, dy = -1,1
            if self._last_event == pygame.K_e: #top right
                dx, dy = 1, -1
            if self._last_event == pygame.K_q: #top left
                dx, dy = -1,-1
            if dx is not None and dy is not None:
                self.move(self, dx, dy) # we are asking ourself to move

            self._last_event = None

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        ''' 
        new_x = self._x + dx
        new_y = self._y + dy
        
        if self._stage.is_in_bounds(new_x, new_y):
            if self._stage.get_actor(new_x, new_y): #checks if space is occupied
                a = self._stage.get_actor(new_x, new_y)
                if isinstance(a, Monster): #checks if moving to a monster
                    self._stage.remove_player() #removes player
                if a.move(self, dx, dy) == False: #calls the move function for a
                    return False
                else:
                    super().move(other, dx, dy)
                    return True
            else: #confirms if space is free, so can move
                super().move(other, dx, dy)
                return True
        else:
            return False
        
    def GameOver(self): #attempt at game over screen
        lst = self._stage.get_actors()
        if "Player" not in str(lst[0]):
            print("KKKKKKKKKK")
            return True
        else:
            return False

        
class Box(Actor):
    '''
    A Box Actor.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a Box on the given stage, at given position.
        '''
        
        super().__init__(icon_file, stage, x, y)

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        new_x = self._x + dx
        new_y = self._y + dy #other in this case is the player
        
        if self._stage.is_in_bounds(new_x, new_y):  #is it on stage
            if self._stage.get_actor(new_x, new_y): #checks if someone is there
                a = self._stage.get_actor(new_x, new_y)
                if a.move(self, dx, dy) == True:
                    super().move(self, (dx), (dy)) 
                    return True 
                else:
                    return False
            else:   #indicating the space is free
                super().move(self, (dx), (dy))  #should move self
                return True
        else:
            return False
        
class StickyBox(Box):

    def __init__(self, icon_file, stage, x, y):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a StickyBox on the given stage, at given position.
        '''

        super().__init__(icon_file, stage, x, y)


class Wall(Actor): 

    def __init__(self, icon_file, stage, x, y):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a Wall on the given stage, at given position.
        '''

        super().__init__(icon_file, stage, x, y)

    def move(self, other, dx, dy):
        '''(Actor, Actor, int, int) -> bool
        Checks if the actor can move, but set to automatically default at False.'''
        return False #makes sure Wall never gets moved
    
class Stage:
    '''
    A Stage that holds all the game's Actors (Player, monsters, boxes, etc.).
    '''
    
    def __init__(self, width, height, icon_dimension):
        '''Construct a Stage with the given dimensions.'''
        
        self._actors = [] # all actors on this stage (monsters, player, boxes, ...)
        self._player = None # a special actor, the player

        # the logical width and height of the stage
        self._width, self._height = width, height

        self._icon_dimension=icon_dimension # the pixel dimension of all actors
        # the pixel dimensions of the whole stage
        self._pixel_width = self._icon_dimension * self._width
        self._pixel_height = self._icon_dimension * self._height
        self._pixel_size = self._pixel_width, self._pixel_height

        # get a screen of the appropriate dimension to draw on
        self._screen = pygame.display.set_mode(self._pixel_size)

    def is_in_bounds(self, x, y):
        '''
        (Stage, int, int) -> bool
        Return True iff the position (x, y) falls within the dimensions of this Stage.'''
        
        return self.is_in_bounds_x(x) and self.is_in_bounds_y(y)

    def is_in_bounds_x(self, x):
        '''
        (Stage, int) -> bool
        Return True iff the x-coordinate given falls within the width of this Stage.
        '''
        
        return 0 <= x and x < self._width

    def is_in_bounds_y(self, y):
        '''
        (Stage, int) -> bool
        Return True iff the y-coordinate given falls within the height of this Stage.
        '''

        return 0 <= y and y < self._height

    def get_width(self):
        '''
        (Stage) -> int
        Return width of Stage.
        '''

        return self._width

    def get_height(self):
        '''
        (Stage) -> int
        Return height of Stage.
        '''
        
        return self._height

    def set_player(self, player):
        '''
        (Stage, Player) -> None
        A Player is a special actor, store a reference to this Player in the attribute
        self._player, and add the Player to the list of Actors.
        '''
        
        self._player=player
        self.add_actor(self._player)

    def remove_player(self):
        '''
        (Stage) -> None
        Remove the Player from the Stage.
        '''
        
        self.remove_actor(self._player)
        self._player=None

    def player_event(self, event):
        '''
        (Stage, int) -> None
        Send a user event to the player (this is a special Actor).
        '''
        
        self._player.handle_event(event)

    def add_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Add the given actor to the Stage.
        '''

        self._actors.append(actor)

    def remove_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Remove the given actor from the Stage.
        '''
        
        self._actors.remove(actor)

    def step(self):
        '''
        (Stage) -> None
        Take one step in the animation of the game. 
        Do this by asking each of the actors on this Stage to take a single step.
        '''

        for a in self._actors:
            a.step()

    def get_actors(self):
        '''
        (Stage) -> None
        Return the list of Actors on this Stage.
        '''
        
        return self._actors

    def get_actor(self, x, y):
        '''
        (Stage, int, int) -> Actor or None
        Return the first actor at coordinates (x,y).
        Or, return None if there is no Actor in that position.
        '''
        
        for a in self._actors:
            if a.get_position() == (x,y):
                return a
        return None

    def draw(self):
        '''
        (Stage) -> None
        Draw all Actors that are part of this Stage to the screen.
        '''
        
        self._screen.fill((0,0,0)) # (0,0,0)=(r,g,b)=black
        for a in self._actors:
            icon = a.get_icon()
            (x,y) = a.get_position()
            d = self._icon_dimension
            rect = pygame.Rect(x*d, y*d, d, d)
            self._screen.blit(icon, rect)
        pygame.display.flip()

class Monster(Actor):
    '''A Monster class.'''
    
    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a Monster.'''
        
        super().__init__(icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1

    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''
        
        if self.is_dead() == True:
            self._stage.remove_actor(self)
            return False

        if not self.delay(): return 
        self.move(self, self._dx, self._dy)
        return True


    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''
        
        if other != self: # Noone pushes me around
            return False

        bounce_off_edge = False

        new_x = self._x + self._dx
        new_y = self._y + self._dy

        if not self._stage.is_in_bounds_x(new_x): 
            self._dx=-self._dx
            bounce_off_edge=True
            
        if not self._stage.is_in_bounds_y(new_y):
            self._dy =- self._dy
            bounce_off_edge = True

        if bounce_off_edge: 
            return False

        actor = self._stage.get_actor(new_x, new_y)
        actor1 = self._stage.get_actor(self._x -1, self._y)
        actor2 = self._stage.get_actor(self._x, self._y -1)
        actor3 = self._stage.get_actor(self._x +1, self._y)
        actor4 = self._stage.get_actor(self._x, self._y +1)
        if isinstance(actor1, StickyBox):
            dx = 0  #checks all sides of monster and if box is there, doesnt move
            dy = 0
            return False
        elif isinstance(actor2, StickyBox):
            dx = 0  
            dy = 0
            return False
        elif isinstance(actor3, StickyBox):
            dx = 0  
            dy = 0
            return False
        elif isinstance(actor4, StickyBox):
            dx = 0  
            dy = 0
            return False
        elif isinstance(actor, StickyBox): #checks if monster moves into stickybox
            dx = 0
            dy = 0
            return False
        
        if actor != None:
                self._dx =- self._dx
                self._dy =- self._dy

        if isinstance(actor, KeyboardPlayer):
            actor._stage.remove_actor(actor) #kills actor
        if isinstance(actor, Box) or isinstance(actor, Wall):
            return False #above checks if box, wall or stickybox
                
        return super().move(other, dx, dy)

    def is_dead(self):
        '''
        Return whether this Monster has died.
        That is, if self is surrounded on all sides, by either Boxes or
        other Monsters.'''
        actor1 = self._stage.get_actor(self._x -1, self._y)
        actor2 = self._stage.get_actor(self._x, self._y -1)
        actor3 = self._stage.get_actor(self._x +1, self._y)
        actor4 = self._stage.get_actor(self._x, self._y +1)
        actor5 = self._stage.get_actor(self._x +1, self._y -1)
        actor6 = self._stage.get_actor(self._x +1, self._y +1)
        actor7 = self._stage.get_actor(self._x -1, self._y +1)
        actor8 = self._stage.get_actor(self._x -1, self._y -1) #checks all surrounding places
        lst = [[actor1, self._x -1, self._y], [actor2, self._x, self._y -1], [actor3, self._x +1, self._y], [actor4, self._x, self._y +1], [actor5, self._x +1, self._y -1], [actor6, self._x +1, self._y +1], [actor7, self._x -1, self._y +1], [actor8, self._x -1, self._y -1]]
        counter = 0
        for i in lst:
            if (i[0] != None) or (self._stage.is_in_bounds(i[1],i[2]) == False):
                counter += 1
            if counter == 8:
                return True
        return False
        


