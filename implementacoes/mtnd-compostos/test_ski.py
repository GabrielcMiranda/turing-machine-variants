# implementacoes/lambda-ski/test_ski.py
import unittest
from ski import parse_ski, reduce_ski, Comb, Var, App
from abstracao import bracket_abstraction

class TestSistemaSKI(unittest.TestCase):

    def test_regras_basicas(self):
        # I x -> x
        f, hist = reduce_ski(parse_ski("I x"))
        self.assertEqual(str(f), "x")

        # K x y -> x
        f, hist = reduce_ski(parse_ski("K x y"))
        self.assertEqual(str(f), "x")

        # S x y z -> x z (y z)
        f, hist = reduce_ski(parse_ski("S x y z"))
        self.assertEqual(str(f), "x z (y z)")

    def test_identidade_skk(self):
        f, _ = reduce_ski(parse_ski("S K K x"))
        self.assertEqual(str(f), "x")

    def test_bracket_abstraction_simples(self):
        # T[λx. x] -> I
        term_x = Var('x')
        result = bracket_abstraction('x', term_x)
        self.assertEqual(result, Comb('I'))

        # T[λx. y] -> K y
        term_y = Var('y')
        result = bracket_abstraction('x', term_y)
        self.assertEqual(result, App(Comb('K'), term_y))

    def test_termo_nao_normalizante(self):
        # S I I (S I I) deve rodar até estourar o limite de passos configurado
        f, hist = reduce_ski(parse_ski("S I I (S I I)"), max_steps=10)
        self.assertEqual(len(hist), 10)

if __name__ == '__main__':
    unittest.main()