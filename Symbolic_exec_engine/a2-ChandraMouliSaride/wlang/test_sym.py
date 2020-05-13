# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest
import wlang.ast as ast
import wlang.sym

class TestSym (unittest.TestCase):

    def test_one (self):
    	#Simple Symbolic execution of straight line of code
        print('test_one')
        prg1 = "havoc x,y;assume x>10;assert x=5"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
       	print(out)
        print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 1)

    def test_two (self):
    	#Simple Symbolic execution of straight line of code
        print('test_two')
        prg1 = "z:=10;havoc x,y;x:=x+y+1;y:=x/y;z:=10*y"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
       	print(out)
        print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 1)
        
    def test_three (self):
    	#Simple Symbolic execution of straight line of code
        print('test_three')
        prg1 = "havoc x;assume x<=10; assert x = 4"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
       	print(out)
        print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 1)


    def test_four (self):
    	#Symbolic execution of IF-Statement
        print('test_four')
        prg1 = "havoc x,y,z,a,b;if(not(x=1)) then x:=y+z else x:=y*z;if(a=1) then z:=20 else z:=10; if(not(a=1)) then z:=30 else z:=50"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
       	print(out)
        print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 8)

    def test_five (self):
    	#Symbolic execution of IF-Statement
        print('test_five')
        prg1 = "havoc x,y,z;if(x>=1) then x:=y+z else x:=y*z; if(x<50) then x:=x+1 else x:=x-1;skip"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
       	print(out)
        print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 4)

    def test_six (self):
    	#Symbolic execution of IF-Statement
        print('test_six')
        prg1 = "havoc x,y,z;if(x>1 or x=10) then {x:=y+1;havoc l} else x:=y-1;havoc a;a:=30;print_state; if(true) then x:=x/y else x:=x-1"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        print(out)
        print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 4)

    def test_seven (self):
    	#Symbolic execution of while-Statement
        print('test_seven')
        prg1 = "havoc x,y,res;while(x>0) do {res:=res+1;y:=20};havoc z;z:=res;havoc m;m:=30"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
       	print(out)
        print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 2)

    def test_eight (self):
    	#Symbolic execution of IF and while-Statement
        print('test_eight')
        prg1 = "havoc x,y,res,z;if(x>1 and x<50) then x:=z else skip;while(z>0) do {res:=res+1;y:=20}"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
       	print(out)
        print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 4)


    def test_nine (self):
        #Symbolic execution of while-Statement
        print('test_nine')
        prg1 = "havoc x,y,res;while(not(x=1)) do y:=20;while(x=1) do y:=30"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        print(out)
        print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 4)

    def test_ten (self):
        #Symbolic execution of diverging huge program
        print('test_ten- Diverging')
        print('Printing only feasbile paths as number of paths are huge')
        prg1 = "havoc x,y,res,z,a;if(x>1 and x<50) then x:=z else skip;while(z>0) do {res:=res+1;y:=20};while(not(x=1)) do y:=20;while(x=1) do y:=30;while(z<0) do {res:=res+1;y:=20};if(not(x=1)) then x:=y+z else x:=y*z;if(a=1) then z:=20 else z:=10; if(not(a=1)) then z:=30 else z:=50;if(x>=1) then x:=y+z else x:=y*z"
        ast1 = ast.parse_string (prg1)
        sym = wlang.sym.SymExec ()
        st = wlang.sym.SymState ()
        out = [s for s in sym.run (ast1, st)]
        for x in out:
            if(not x.is_error()):
                print(x)
                print('-----------------------------------------------------------------')
        self.assertEquals (len(out), 512)




        
