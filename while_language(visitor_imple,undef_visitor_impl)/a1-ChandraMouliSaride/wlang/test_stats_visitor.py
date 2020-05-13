import unittest
import wlang.ast as ast
import wlang.stats_visitor as stats_visitor

class TestStatsVisitor (unittest.TestCase):
    def test_one (self):
        prg1 = """{x:=1;y:=2};
        			havoc z,a,b;
        			if(x=1)then z:=x+y
        			else z:=x*y;
        			while(y=2)do y:=y-1;
        			assert(z>x);
        			assume(z<100);
        			b:=9;
        			y:=e+f;
        			print_state"""
        ast1 = ast.parse_string (prg1)

        sv = stats_visitor.StatsVisitor ()
        sv.visit (ast1)
        self.assertEquals (sv.get_num_stmts (), 13)
        self.assertEquals (sv.get_num_vars (), 7)
