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
import cStringIO
import sys
import operator
import z3

class SymState(object):
    def __init__(self, solver = None):
        # environment mapping variables to symbolic constants
        self.env = dict()
        # path condition
        self.path = list ()
        self._solver = solver
        if self._solver is None:
            self._solver = z3.Solver ()

        # true if this is an error state
        self._is_error = False

    def add_pc (self, *exp):
        """Add constraints to the path condition"""
        self.path.extend (exp)
        self._solver.append (exp)
        
    def is_error (self):
        return self._is_error
    def mk_error (self):
        self._is_error = True
        
    def is_empty (self):
        """Check whether the current symbolic state has any concrete states"""
        res = self._solver.check ()
        return res == z3.unsat


        
    def fork(self):
        """Fork the current state into two identical states that can evolve separately"""
        child = SymState ()
        child.env = dict(self.env)
        child.add_pc (*self.path)
        
        return (child)
    
    def __repr__ (self):
        return str(self)
        
    def to_smt2 (self):
        """Returns the current state as an SMT-LIB2 benchmark"""
        return self._solver.to_smt2 ()
    
        
    def __str__ (self):
        buf = cStringIO.StringIO ()
        buf.write ('\n')
        buf.write ('-----')
        buf.write ('\n')
        for k, v in self.env.iteritems():
            buf.write (str (k))
            buf.write (': ')
            buf.write (str (v))
            buf.write ('\n')
        buf.write ('pc: ')
        buf.write (str (self.path))
        buf.write ('\n')
        if(self._is_error):
            buf.write ('This path  is infeasible pc failed !')
            
        return buf.getvalue ()
                   
class SymExec (wlang.ast.AstVisitor):
    def __init__(self):
        self._state_list = list ()
        self._num_paths=0
        self._ifchkflg=0
        self._fromblock=0
        self._whilecnt=0
        self._inloop=0
        self._stateforwhile=0
        pass

    def run (self, ast, state):
        ## set things up and 
        self.visit (ast, state=state)
        
        return self._state_list
        pass

    def visit_IntVar (self, node, *args, **kwargs):
        st=self._state_list[self._num_paths]
        return st.env[node.name]
    
    def visit_BoolConst(self, node, *args, **kwargs):
        return z3.BoolVal (node.val)

    def visit_IntConst (self, node, *args, **kwargs):
        return z3.IntVal(node.val)
    
    def visit_RelExp (self, node, *args, **kwargs):
        lhs = self.visit (node.arg (0), *args, **kwargs)
        rhs = self.visit (node.arg (1), *args, **kwargs)
        if node.op == '<=': return z3.simplify(lhs<=rhs)
        if node.op == '<': return z3.simplify(lhs<rhs)
        if node.op == '=': return z3.simplify(lhs==rhs)
        if node.op == '>=': return z3.simplify(lhs>=rhs)
        if node.op == '>': return z3.simplify(lhs>rhs)


    def visit_BExp (self, node, *args, **kwargs):
        kids = [self.visit (a, *args, **kwargs) for a in node.args]
        
        
        if node.op == 'not':
            assert node.is_unary ()
            assert len (kids) == 1
            return z3.Not(kids[0])
        x=kids[0]
        y=kids[1]
        fn = None
        base = None
        if node.op == 'and':
            return z3.And(x,y)
        elif node.op == 'or':
            return z3.Or(x,y)

        
    def visit_AExp (self, node, *args, **kwargs):
        kids = [self.visit (a, *args, **kwargs) for a in node.args]
        x=kids[0]
        y=kids[1]
        fn = None
        base = None
        if node.op == '+':
            return z3.simplify(x + y)
            
        elif node.op == '-':
            return z3.simplify(x - y)

        elif node.op == '*':
            return z3.simplify(x * y)

        elif node.op == '/':
            return z3.simplify(x / y)
     
        
        
    def visit_SkipStmt (self, node, *args, **kwargs):
        st=self._state_list[self._num_paths]
        return st
        
    
    def visit_PrintStateStmt (self, node, *args, **kwargs):
        st=self._state_list[self._num_paths]
        if(not st.is_error() and not st.is_empty()):
            print('state is ',st)
        pass

    def visit_AsgnStmt (self, node, *args, **kwargs):
        if(len(self._state_list)==0):
            st = kwargs['state']
        else:
            st=self._state_list[self._num_paths]
        
        st.env [node.lhs.name] = self.visit (node.rhs, *args, **kwargs)
        if(len(self._state_list)==0):
            self._state_list.append(st)
        else:
            if(self._fromblock):
                self._state_list[self._num_paths]=st
            else:
                for s in self._state_list:
                    self._num_paths=self._state_list.index(s)
                    s.env[node.lhs.name]=self.visit (node.rhs, *args, **kwargs)

            
            return st
            pass

    def visit_IfStmt (self, node, *args, **kwargs):
        cond = self.visit (node.cond, *args, **kwargs)
        st=self._state_list[:]
        for s in st:
            st1=s.fork()
            self._state_list.append(st1)
        self._num_paths=0
        size=len(self._state_list)
        for s in self._state_list:
            if(self._num_paths<size/2):
                s.add_pc(z3.simplify(cond))
                if str(s._solver.check())=='unsat':
                    s.mk_error();
                self._fromblock=1
                self.visit (node.then_stmt, *args, **kwargs)
                self._fromblock=0
                self._num_paths=self._num_paths+1
            else:
                s.add_pc(z3.simplify(z3.Not(cond)))
                if str(s._solver.check())=='unsat':
                    s.mk_error();
                self._fromblock=1
                if node.has_else():
                    self.visit (node.else_stmt, *args, **kwargs)
                self._fromblock=0
                self._num_paths=self._num_paths+1

        self._num_paths=0
        pass
            
    def visit_WhileStmt (self, node, *args, **kwargs):
        cond = self.visit (node.cond, *args, **kwargs)
        st=self._state_list[:]
        for s in st:
            st1=s.fork()
            self._state_list.append(st1)
        self._num_paths=0
        size=len(self._state_list)
        for s in self._state_list:
            if(self._num_paths<size/2):
                s.add_pc(z3.simplify(cond))
                if str(s._solver.check())=='unsat':
                    s.mk_error();
                self._fromblock=1
                for i in range(0,10):
                    self.visit (node.body, *args, **kwargs)
                self._fromblock=0
                self._num_paths=self._num_paths+1
            else:
                s.add_pc(z3.simplify(z3.Not(cond)))
                if str(s._solver.check())=='unsat':
                    s.mk_error();
                self._num_paths=self._num_paths+1

        self._num_paths=0
        pass

    def visit_AssertStmt (self, node, *args, **kwargs):
        ## Don't forget to print an error message if an assertion might be violated
        cond = self.visit (node.cond, *args, **kwargs)
        st=self._state_list[self._num_paths]
        st.add_pc(cond)
        if str(st._solver.check())=='unsat':
            st.mk_error()
            print('Assertion failed',st.to_smt2())

        return kwargs['state']
    
    def visit_AssumeStmt (self, node, *args, **kwargs):
        st=self._state_list[self._num_paths]
        kwargs['state']=st
        return self.visit_AssertStmt (node, *args, **kwargs)
        pass

    def visit_HavocStmt (self, node, *args, **kwargs):
        if(len(self._state_list)==0):
            st = kwargs['state']
        else:
            st=self._state_list[self._num_paths]
        st1=st.fork()
        if(len(self._state_list)==0):
            for v in node.vars:
                st1.env [v.name] = z3.Int(v.name)
            self._state_list.append(st1)
        else:
            if(self._fromblock):
                for v in node.vars:
                    st1.env [v.name] = z3.Int(v.name)
                self._state_list[self._num_paths]=st1
            else:
                for s in self._state_list:
                    for v in node.vars:
                        s.env [v.name] = z3.Int(v.name)
        return st1
        pass

    def visit_StmtList (self, node, *args, **kwargs):
        if(len(self._state_list)==0):
            st = kwargs['state']
        else:
            st=self._state_list[self._num_paths]
        st1=st.fork()
        nkwargs = dict (kwargs)
        for stmt in node.stmts:
            nkwargs ['state'] = st1
            self.visit (stmt, *args, **nkwargs)
            st=self._state_list[self._num_paths]
        return st

        

    

                    
