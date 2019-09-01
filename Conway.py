from time import sleep
from random import randint, random
import os


class Game: 
  def __init__(self, size = (20, 80), total_gen_num = -1, rand_intensity = 0.7, sleep_interval = 0.2):
    self.board = Grid_(*size)
    self.total_gen_num = total_gen_num
    self.rand_intensity = rand_intensity
    self.sleep_interval = sleep_interval
    
    self.gen_num = 0
    self.running = False
    
    if os.name == 'nt':
      self.clear = 'cls'
    else:
      self.clear = 'clear'
    

  def fill_random(self):
    self.board.place_random(self.rand_intensity)
  
  def start(self):
    user = input('Do you want a Glider Gun or Random field? R/G\n') 
    if user.lower() == 'r':
      self.fill_random()
    elif user.lower() == 'g':
      self.board.place_glider()
    self.run()
  
  def does_survive(self, i, j, count):
    if self.board.field[i][j].is_alive and (count == 3 or count == 2):
      return True
    elif not self.board.field[i][j].is_alive and count == 3:
      return True
  
  def next_gen(self):
    next_grid = self.board.clean_board()

    for i in range(1, self.board.height - 1):
      for j in range(1, self.board.width - 1):
        neighbors_count = self.board.get_num_live_neighbors(i, j)
        next_grid[i][j].is_alive = self.does_survive(i, j, neighbors_count)
    
    if next_grid == self.board.field:
      self.running = False
    self.board.field = next_grid
    self.gen_num += 1
    return self.board.field


  def run(self):
    self.running = True
    while self.running and self.total_gen_num < 0 or self.gen_num < self.total_gen_num:
      sleep(self.sleep_interval)
      self.next_gen()
      os.system(self.clear)
      print(f"{self.board} \nCurrent generation: {self.gen_num} ({'running' if self.running else 'stopped because was static'})")
    self.play_again()
  
  def play_again(self):
    user = input('Play again? (Y/N)\n')
    if user.lower() == 'y':
      self.start('r')
    else:
      quit()



class Cell:
    def __init__(self, is_alive = False):
      self.is_alive = is_alive 

    def __int__(self):
      return 1 if self.is_alive else 0

    def __repr__(self):
      return 'O' if self.is_alive else '.'
    
    def __eq__(self, other):
        return self.is_alive == other.is_alive



class Grid_:
    def __init__(self, height, width):      
      self.width = width
      self.height = height
      self.field = self.clean_board()

    def __repr__(self):
      repr = ''
      for row in self.field:
        for cell in row:
          repr += f'{cell}'
        repr += '\n'
      return repr

    def clean_board(self):
      return [[Cell() for i in range(self.width)] for j in range(self.height)]
      
    def place_random(self, intensity):
      for i in range(self.width):
        for j in range(self.height):
          if random() >= intensity:
            self.field[j][i].is_alive = True

    def place_glider(self):
      for i, j in [(5, 1), (5, 2), (6, 1), (6, 2), (3, 13), (3, 14), (4,12), (4, 16), (5, 11), (5, 17), (6, 11), (6, 15),
      (6, 17), (6, 18), (7, 11), (7, 17), (8, 12), (8, 16), (9, 13), (9, 14), (1, 25), (2, 23), (2, 25), (3, 21), (3, 22),
      (4, 21), (4, 22), (5, 21), (5, 22), (6, 23), (6, 25), (7, 25), (3, 35), (3, 36), (4, 35), (4, 36)]:
        self.field[i][j].is_alive = True

    
    def get_num_live_neighbors(self, i, j):
      frame = [self.field[i + id][j + jd] for id, jd in [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1),(0, 1), (-1, 1), (-1, 0)]]
      return sum(map(int, frame))




if __name__ == "__main__":
  life = Game()
  life.start()
  
    
