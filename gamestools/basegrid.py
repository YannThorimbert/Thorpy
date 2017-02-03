"""Module providing several classes for handling grid objects"""

class __GridIterator__(object):

    def __init__(self, nx, ny, x, y):
        self.x = x-1
        self.y = y
        self.nx = nx
        self.ny = ny

    def __next__(self):
        if self.x == self.nx-1:
            self.x = 0
            self.y += 1
            if self.y > self.ny-1:
                raise StopIteration()
            else:
                return (self.x, self.y)
        else:
            self.x += 1
            return (self.x, self.y)

    def next(self): #for python2 compatibility
        return self.__next__()

class BaseGrid(object):

    def __init__(self, nx, ny, value=None, periodicity=(False,False)):
        self.nx = nx
        self.ny = ny
        self.cells = [[value for y in range(ny)] for x in range(nx)]
        self.default_value = value
        self.periodicity = periodicity
        self.min_nxy = min(self.nx, self.ny)
        self.set_all = self.fill #alias

    def copy(self):
        grid = BaseGrid(self.nx, self.ny, self.periodicity)
        for x,y in self:
            grid[x,y] = self[x,y]
        return grid

    def __len__(self):
        """Returns the number of cells contained on the grid."""
        return self.nx * self.ny

    def __getitem__(self, key):
        x,y = key
        if self.periodicity[0]:
            x %= self.nx
        if self.periodicity[1]:
            y %= self.ny
        return self.cells[x][y]

    def __setitem__(self, key, value):
        self.cells[key[0]][key[1]] = value

    def __iter__(self, x=0, y=0):
        """Iterate over coordinates."""
        return __GridIterator__(self.nx, self.ny, x, y)

    def __repr__(self):
        return str(self.cells)

    def itercells(self):
        """Iterate over cell values"""
        for x,y in self:
            yield self[x,y]

    def iterline(self, y):
        for x in range(self.nx):
            yield self[x,y]

    def itercolumn(self, x):
        for y in range(self.ny):
            yield self[x,y]


    def iterdiag_up(self, x, y):
        n = min(self.nx-x, self.ny-y) #opti sans min?
##        print("up", x, y, n)
        for i in range(n):
##            print(self[x+i,y+i], x+i, y+i)
            yield self[x+i,y+i]

    def iterdiag_down(self, x, y):
        n = min(self.nx-x, y+1) #opti sans min?
##        print("down", x, y, n)
        for i in range(n):
##            print(self[x+i,y-i], x+i, y-i)
            yield self[x+i,y-i]

    def fill(self, value):
        for x,y in self:
            self[x,y] = value

    def is_inside(self, coord):
        """returns True if <coord> is contained into the domain (not pixels!)"""
        return (0 <= coord[0] < self.nx) and  (0 <= coord[1] < self.ny)

    def shift_values_x(self, amount): #todo: fill new cells (works only for |amount| = 1!!!
        if amount > 0: #shift to the right, new column on the left
            for x in range(self.nx-1,amount-1,-1):
                for y in range(self.ny):
                    self[x,y] = self[x-1,y]
            for y in range(self.ny): #boucler!
                self[0,y] = self.default_value
        else:
            for x in range(self.nx+amount): #amount is negative!
                for y in range(self.ny):
                    self[x,y] = self[x+1,y]
            for y in range(self.ny): #boucler!
                self[self.nx-1,y] = self.default_value

    def shift_values_y(self, amount): #todo: fill new cells (works only for |amount| = 1!!!
        if amount > 0: #shift to the right, new column on the left
            for y in range(self.ny-1,amount-1,-1):
                for x in range(self.nx):
                    self[x,y] = self[x,y-1]
            for x in range(self.nx): #boucler!
                self[x,0] = self.default_value
        else:
            for y in range(self.ny+amount): #amount is negative!
                for x in range(self.nx):
                    self[x,y] = self[x,y+1]
            for x in range(self.nx): #boucler!
                self[x,self.ny-1] = self.default_value



class DiagonalHelper(object):

    def __init__(self, grid):
        self.grid = grid
        self.diags_up = [[None for y in range(grid.ny)] for x in range(grid.nx)]
        self.diags_down = [[None for y in range(grid.ny)] for x in range(grid.nx)]
        self._build_diags()

    def _build_diags(self):
        nx, ny = self.grid.nx, self.grid.ny
        for x in range(nx): #coming from up and down lines
            n = min(nx-x, ny)
            for i in range(n):
                self.diags_down[x+i][ny-1-i] = (x, ny-1, n)
                self.diags_up[x+i][0+i] = (x, 0, n)
        for y in range(ny-1): #down coming from left column
            n = min(y+1, nx)
            for i in range(n):
                self.diags_down[0+i][y-i] = (0, y, n)
        for y in range(1, ny): #up coming from left column
            n = min(ny-y, nx)
            for i in range(n):
                self.diags_up[0+i][y+i] = (0, y, n)

    def iterdiag_up(self, x, y):
        x, y, n = self.diags_up[x][y]
        for i in range(n):
            yield self.grid[x+i,y+i]

    def iterdiag_down(self, x, y):
        x, y, n = self.diags_down[x][y]
        for i in range(n):
            yield self.grid[x+i,y-i]

