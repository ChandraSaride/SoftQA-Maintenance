import unittest
import wlang.ast as ast
import wlang.undef_visitor as undef_visitor

class TestStatsVisitor (unittest.TestCase):
    def test_one (self):
        prg1 = "x := 10; y := x + z;havoc a;a:=b+c"
        ast1 = ast.parse_string (prg1)

        uv = undef_visitor.UndefVisitor ()
        uv.check (ast1)
        self.assertEquals (set ([ast.IntVar('z'),ast.IntVar('b'),ast.IntVar('c')]), uv.get_undefs ())

    def test_two (self):
        prg1 = """havoc x;
					if x > 10 then
						y:=x+1

					else
						z := 10 ;
					x := z + 1"""
        ast1 = ast.parse_string (prg1)

        uv = undef_visitor.UndefVisitor ()
        uv.check (ast1)
        self.assertEquals (set ([ast.IntVar('z')]), uv.get_undefs ())

    def test_three (self):
        prg1 = """havoc x;
					if x > 10 then
						z:=11

					else
						z := 10 ;
					x := z + 1"""
        ast1 = ast.parse_string (prg1)

        uv = undef_visitor.UndefVisitor ()
        uv.check (ast1)
        self.assertEquals (set (), uv.get_undefs ())
