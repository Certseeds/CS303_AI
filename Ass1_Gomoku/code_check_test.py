#!/usr/bin/env python3
import sys
import time
from Ass1_Gomoku.code_check import CodeCheck
def main():
    times = time.time()
   # code_checker = CodeCheck("Gomoku_first.py", 15)
   # code_checker = CodeCheck("Gomoku_onehalf.py", 15)
   # code_checker = CodeCheck("Gomoku_three.py", 15)
   # code_checker = CodeCheck("Gomoku_one_two.py", 15)
   # code_checker = CodeCheck("Gomoku_fourth.py", 15)
    code_checker = CodeCheck("Gomoku_fifth.py", 15)

    if not code_checker.check_code():
        print(code_checker.errormsg)
    else:
        print('pass')
    print(time.time() - times)
if __name__ == '__main__':
    main()


