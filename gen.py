#!/usr/bin/python3

import random
import os
import sys
import itertools
import logging

# random.choice
# random.randint
# random.random

class SudokuGenerator():
  def __init__(self, side=9):
    """
    self.s (side): number of elements making one side (9X9, 3X3, etc)
    self.p (puzzle): nested list representing the grid
    """
    self.s = side
    self.numSet = set(range(1, self.s+1))
    logging.info(self.numSet)
    self.p = [[None for i in range(self.s)] for j in range(self.s)]

  def generate(self):
    self._fillRow(0)
    for i in range(1, self.s):
      logging.critical(f"INDEX: {i}")
      logging.info(self.print())
      self._fillRow(i)
      # >>> zip(*[[1,2], [3,4], [5,6]])
      # [(1, 3, 5), (2, 4, 6)]
      # See Unpacking Argument Lists: http://docs.python.org/tutorial/controlflow.html#tut-unpacking-arguments
      # The reverse situation occurs when the arguments are already in a list or tuple but need to be unpacked for a function call requiring separate positional arguments. For instance, the built-in range() function expects separate start and stop arguments. If they are not available separately, write the function call with the *-operator to unpack the arguments out of a list or tuple:
      hitCols = self._findHits()
      while len(hitCols) > 0:
        for index in hitCols:
          logging.debug(f"index: {index}")
          cols = list(zip(*self.p))
          col = [c for c in cols[index] if c is not None]
          num = self._getDuplicate(col)
          logging.debug(f"duplicate: {num}")
          E = self.numSet.difference(set(col))
          choice = random.choice(list(E))
          logging.debug(f"choice: {choice}")
          idx1 = self.p[i].index(choice)
          idx2 = self.p[i].index(num)
          self._swap(self.p[i], idx1, idx2)
          logging.debug(f"swapped row: {self.p[i]}")
          logging.debug(f"hitCols before: {hitCols}")

          # a swap can cause two hits to be resolved together
          # this is to check for that case
          for c in cols:
            if c[i] == choice:
              col2_index = cols.index(c)
              logging.info(f"col2_index {col2_index}")
          if not self._hasDuplicateItems(cols[col2_index]):
            if col2_index in hitCols:
              hitCols.pop(hitCols.index(col2_index))

          # just resolved this, so removing
          hitCols.pop(hitCols.index(index))
          logging.debug(f"hitCols after: {hitCols}")
          set1 = set(self._findHits())
          set2 = set(hitCols)
          differenceSet = set1.difference(set2)
          hitCols.extend(list(differenceSet))
          # hitCols = list(set(hitCols))

  def _swap(self, row, idx1, idx2):
    row[idx1], row[idx2] = row[idx2], row[idx1]
  
  def _getDuplicate(self, col):
    # TODO: Refactor this. Very Java-esque.
    out = None
    for i in range(len(col)):
      curr = col[i]
      for j in range(i+1, len(col)):
        if col[j] == curr: out = curr
    return curr

  def print(self):
    for row in self.p:
      for elem in row:
        print(elem, end=' ')
      print()

  def _findHits(self):
    cols = list(zip(*self.p))
    l = []
    for c in cols:
      if self._hasDuplicateItems(c):
        l.append(cols.index(c))
    return l

  def _hasDuplicateItems(self, row):
    filtered = [c for c in row if c is not None]
    return len(filtered) > len(set(filtered))

  def _fillRow(self, rowNum):
    row = list(
      random.choice(
        list(
          itertools.permutations(range(1, 10)))))
    logging.debug(f"row: {row}")
    self.p[rowNum] = row

def main():
  # TODO: config to write to log file
  logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%b %d, %Y %I:%M:%S %p',
    level=logging.DEBUG
  )
  s = SudokuGenerator()
  s.generate()
  s.print()


if __name__ == "__main__":
  main()