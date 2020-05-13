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
import wlang.int

class TestInt (unittest.TestCase):

	#Node Coverage




    def test_one (self):
    	#Here we covered block statements, statements list, assignment, boolean Expression, if statement, print,bfactor,batom,relational operators
        prg1 = "{x := 10;y:=5};{if(x>y or x=10) then res:=1 else skip ;print_state}"
        # test parser
        ast1 = ast.parse_string (prg1)
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x,y,res is defined
        self.assertIn ('x', st.env)
        self.assertIn ('y', st.env)
        self.assertIn ('res', st.env)
        # x is 10 , y is 5 , res is 1
        self.assertEquals (st.env['x'], 10)
        self.assertEquals (st.env['y'], 5)
        self.assertEquals (st.env['res'], 1)
        # no other variables in the state
        self.assertEquals (len (st.env), 3)

    def test_two (self):
    	#Here we covered while statement,subtraction,multilication,addition,skip,block statements, statements list, assignment,print
        prg1 = "x:=1;y:=((x*100)/x)+1;if(x=1) then skip;while(x=1) do {res:=1;x:=x-1}; print_state"
        # test parser
        ast1 = ast.parse_string (prg1)
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x,y,res is defined
        self.assertIn ('x', st.env)
        self.assertIn ('res', st.env)
        self.assertIn('y',st.env)
        # x is 0 , res is 1,y is 101
        self.assertEquals (st.env['x'], 0)
        self.assertEquals (st.env['y'], 101)
        self.assertEquals (st.env['res'], 1)
        # no other variables in the state
        self.assertEquals (len (st.env), 3)

    def test_three (self):
    	#Here we covered while statement,all relational operations,subtraction,multilication,addition,skip,block statements, statements list, assignment,print
        prg1 = """ x:=10;
        		   havoc y;
        		   havoc z;
        		   y:=x+1;
        		   assert(y>x);
        		   assume(z<y);
        		   havoc a,b;
        		   assume(a<=z);
        		   assume(b>=z);
        		   print_state


        """
        # test parser
        ast1 = ast.parse_string (prg1)
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x,y,z,a,b is defined
        self.assertIn ('x', st.env)
        self.assertIn ('y', st.env)
        self.assertIn ('z', st.env)
        self.assertIn ('a', st.env)
        self.assertIn ('b', st.env)
        # x is 10 ,y is 11
        self.assertEquals (st.env['x'], 10)
        self.assertEquals (st.env['y'], 11)
        # no other variables in the state
        self.assertEquals (len (st.env), 5)

    def test_four (self):
    	#Here we covered parsing from file,block statements, statements list, assignment, boolean Expression, if statement, print,bfactor,batom
        
        # test parser
        ast1 = ast.parse_file ("./wlang/parse_file_test.txt")
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x,y,res is defined
        self.assertIn ('x', st.env)
        self.assertIn ('y', st.env)
        self.assertIn ('res', st.env)
        # x is 10 , y is 5 , res is 1
        self.assertEquals (st.env['x'], 10)
        self.assertEquals (st.env['y'], 5)
        self.assertEquals (st.env['res'], 1)
        # no other variables in the state
        self.assertEquals (len (st.env), 3)



    #Branch Coverage

    def test_five (self):
    	#Here we covered both branches of if statement ,along with various elements
        prg1 = "{x := 10;y:=5};{if(x>y or x=10) then res:=1 else skip ;if(x<10) then skip else res:=1;print_state}"
        # test parser
        ast1 = ast.parse_string (prg1)
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x,y,res is defined
        self.assertIn ('x', st.env)
        self.assertIn ('y', st.env)
        self.assertIn ('res', st.env)
        # x is 10 , y is 5 , res is 1
        self.assertEquals (st.env['x'], 10)
        self.assertEquals (st.env['y'], 5)
        self.assertEquals (st.env['res'], 1)
        # no other variables in the state
        self.assertEquals (len (st.env), 3)


    def test_six (self):
    	#Here we covered while statement,subtraction,multilication,addition,skip,block statements, statements list, assignment,print
        prg1 = "x:=2;y:=((x*100)/x)+1;if(x=1) then skip;while(x>0) do {res:=1;x:=x-1}; print_state"
        # test parser
        ast1 = ast.parse_string (prg1)
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x,y,res is defined
        self.assertIn ('x', st.env)
        self.assertIn ('res', st.env)
        self.assertIn('y',st.env)
        # x is 0 , res is 1,y is 101
        self.assertEquals (st.env['x'], 0)
        self.assertEquals (st.env['y'], 101)
        self.assertEquals (st.env['res'], 1)
        # no other variables in the state
        self.assertEquals (len (st.env), 3)


    def test_seven (self):
    	#Here we covered while statement,all relational operations,subtraction,multilication,addition,skip,block statements, statements list, assignment,print
        prg1 = """ x:=10;
        		   havoc y;
        		   havoc z;
        		   y:=x+1;
        		   assert(y>x);
        		   assume(z<y);
        		   havoc a,b;
        		   assume(a<=z);
        		   assume(b>=z);
        		   print_state


        """
        # test parser
        ast1 = ast.parse_string (prg1)
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x,y,z,a,b is defined
        self.assertIn ('x', st.env)
        self.assertIn ('y', st.env)
        self.assertIn ('z', st.env)
        self.assertIn ('a', st.env)
        self.assertIn ('b', st.env)
        # x is 10 ,y is 11
        self.assertEquals (st.env['x'], 10)
        self.assertEquals (st.env['y'], 11)
        # no other variables in the state
        self.assertEquals (len (st.env), 5)


    def test_eight (self):
    	#Here we covered parsing from file,block statements, statements list, assignment, boolean Expression, if statement, print,bfactor,batom
        
        # test parser
        ast1 = ast.parse_file ("./wlang/parse_file_test.txt")
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x,y,res is defined
        self.assertIn ('x', st.env)
        self.assertIn ('y', st.env)
        self.assertIn ('res', st.env)
        # x is 10 , y is 5 , res is 1
        self.assertEquals (st.env['x'], 10)
        self.assertEquals (st.env['y'], 5)
        self.assertEquals (st.env['res'], 1)
        # no other variables in the state
        self.assertEquals (len (st.env), 3)






        
        
