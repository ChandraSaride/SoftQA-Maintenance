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
from __future__ import print_function

import wlang.ast

class StatsVisitor (wlang.ast.AstVisitor):
    """Statistics gathering visitor"""
    def __init__ (self):
        super (StatsVisitor, self).__init__ ()
        # number of statements visited
        self._num_stmts = 0
        # the set of all visited variables
        self._vars = set ()
        
    def get_num_stmts (self):
        """Returns number of statements visited"""
        return self._num_stmts

    def get_num_vars (self):
        """Returns number of distinct variables visited"""
        print(self._vars)
        return len (self._vars)
    
    def visit_StmtList (self, node, *args, **kwargs):
        if node.stmts is None:
            return
        for s in node.stmts:
            self.visit (s)
        pass
            
    def visit_Stmt (self, node, *args, **kwargs):

    	self._num_stmts = self._num_stmts + 1
        pass
    
    def visit_IntVar (self, node, *args, **kwargs):
    	#To avoid repetition of variables
    	if(node not in self._vars):
    		self._vars.add(node)
        pass
    
    def visit_Const (self, node, *args, **kwargs):
        #We can save constants list using node.val, but in  question its asked only to count variables
        pass
    
    def visit_AsgnStmt (self, node, *args, **kwargs):
    	#Based on code from interpreter
    	self.visit_IntVar(node.lhs)
    	self.visit_Stmt(node)
    	rhstype=type(node.rhs)
    	#to detect if rhs is using any variables, just for adding any variables which are used without declaration
    	flag=(rhstype is not wlang.ast.IntConst and rhstype is not wlang.ast.BoolConst )
    	if (flag):
    		
    		for con in node.rhs.args:
    		 #check to avoid contants in rhs like y:=z-1 , to avoid -1 
    		 vartype=type(con)
    		 if (vartype is not wlang.ast.IntConst and vartype is not wlang.ast.BoolConst ):
                       if(con not in self._vars):
    		                         self._vars.add(con)

        pass
        
    def visit_IfStmt (self, node, *args, **kwargs):
    	self.visit_Stmt (node)
        self.visit (node.then_stmt)
        if node.has_else ():
            self.visit (node.else_stmt)
        pass

    def visit_WhileStmt (self, node, *args, **kwargs):
    	self.visit_Stmt (node)
        self.visit (node.body)
        pass
    
    def visit_AssertStmt (self, node, *args, **kwargs):
    	self.visit_Stmt(node)
        pass
    
    def visit_AssumeStmt (self, node, *args, **kwargs):
    	self.visit_Stmt(node)
        pass
        
    def visit_HavocStmt (self, node, *args, **kwargs):
    	#Based on code from interpreter
    	for x in node.vars:
    		if(x not in self._vars):
    		  self._vars.add(x)  
    	self.visit_Stmt(node)
        pass

    def visit_Exp (self, node, *args, **kwargs):
    	self.visit_Stmt(node)
        pass

    
        

