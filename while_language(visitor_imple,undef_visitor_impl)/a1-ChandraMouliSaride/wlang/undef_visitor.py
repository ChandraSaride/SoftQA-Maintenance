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
            
class UndefVisitor (wlang.ast.AstVisitor):
    """Computes all variables that are used before being defined"""
    def __init__ (self):
        super (UndefVisitor, self).__init__ ()
        #set for storing undefined variables
        self._undef_vars = set ()
        #set for storing defined variables
        self._def_vars=set()
        self._final_undef_vars=set()
        self._state=0
        pass

    def check (self, node):
        """Check for undefined variables starting from a given AST node"""
        # do the necessary setup/arguments and call self.visit (node, args)
        self.visit(node)
        pass

    def get_undefs (self):
        """Return the set of all variables that are used before being defined
           in the program.  Available only after a call to check()
        """
        return self._final_undef_vars
        
    def visit_StmtList (self, node, *args, **kwargs):
    	if node.stmts is None:
            return
        for s in node.stmts:
            self.visit (s)
  
        pass
    
    def visit_IntVar (self, node, *args, **kwargs):
        #To avoid repetition of variables
    	if(node not in self._def_vars and node not in self._undef_vars):
    		self._def_vars.add(node)
        pass
            
    def visit_Const (self, node, *args, **kwargs):
        pass
    
    def visit_Stmt (self, node, *args, **kwargs):
        pass
    
    def visit_AsgnStmt (self, node, *args, **kwargs):
    	#Based on code from interpreter
    	if(self._state is 1):
    		if(node.lhs not in self._def_vars):
    			self._undef_vars.add(node.lhs)
    	elif(self._state is 2):
    		if(node.lhs in self._undef_vars):
    			self._def_vars.add(node.lhs)
    			self._undef_vars.remove(node.lhs)
    	else:
    		self.visit_IntVar(node.lhs)
    	rhstype=type(node.rhs)
    	#to detect if rhs is using any variables, just for adding any variables which are used without declaration
    	flag=(rhstype is not wlang.ast.IntConst and rhstype is not wlang.ast.BoolConst )
    	if (flag):
    		
    		for con in node.rhs.args:
    		 #check to avoid contants in rhs like y:=z-1 , to avoid -1 
    		 vartype=type(con)
    		 if (vartype is not wlang.ast.IntConst and vartype is not wlang.ast.BoolConst ):	
    			if((con not in self._def_vars and con not in self._undef_vars) or con in self._undef_vars):
    		           self._final_undef_vars.add(con)
        pass

    def visit_Exp (self, node, *args, **kwargs):
        pass
    
    def visit_HavocStmt (self, node, *args, **kwargs):
    	#Based on code from interpreter
    	if(self._state is 1):
    		for x in node.vars:
    			if(x not in self._def_vars):
    				self._undef_vars.add(x)
				  
    	elif(self._state is 2):
    		for x in node.vars:
    			if(x  in self._undef_vars):
    				self._def_vars.add(x)
    				self._undef_vars.remove(x)

    	else:
    		 for x in node.vars:
    			if(x not in self._def_vars):
    		  		self._def_vars.add(x)		
    	  
        pass
    
    def visit_AssertStmt (self, node, *args, **kwargs):
        pass
    
    def visit_AssumeStmt (self, node, *args, **kwargs):
        pass

    def visit_IfStmt (self, node, *args, **kwargs):
    	self._state=1
        self.visit (node.then_stmt)
        if node.has_else ():
        	self._state=2
        	self.visit (node.else_stmt)
            
        self._state=0
        pass

    def visit_WhileStmt (self, node, *args, **kwargs):
        self.visit (node.body)
        pass
        
