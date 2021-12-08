from typing import MutableSequence
from Employer import *

class DisplayModule:
  name: str
  actualStatus: int
  value: int
  def newUser(self, name: str):
    self.name = name
    self.actualStatus = 0
  def changeStatus(self, actualStatus: str):
    self.actualStatus += 1
    print(actualStatus + "\t done")
  def printStatus(self):
    print("\033[A"*self.actualStatus + "Current user is " + self.name +\
      "\n", end="")