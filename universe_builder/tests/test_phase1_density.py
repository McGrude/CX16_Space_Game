"""Checks for the experimental total-body budget, not Phase 1 acceptance."""
import unittest
from universe_builder.analysis.phase1_density import generate, validate


class DensityTrialTests(unittest.TestCase):
    def test_forced_budgets_include_moons_and_parents(self):
        for budget in range(6):
            weights=[(i,100 if i==budget else 0) for i in range(6)]
            for sid in range(1,31):
                star={'id':str(sid),'proper':'Fixture','spect':'G2V'}
                objects=generate(star,42,weights)
                self.assertEqual(len(objects),budget)
                validate(star,objects)

    def test_repeatability(self):
        star={'id':'71456','proper':'Alpha Centauri','spect':'G2V'}
        weights=[(0,10),(1,35),(2,35),(3,15),(4,4),(5,1)]
        self.assertEqual(generate(star,42,weights),generate(star,42,weights))

    def test_sol_keeps_explicit_four_body_exception(self):
        star={'id':'0','proper':'Sol','spect':'G2V'}
        objects=generate(star,42,[(i,100 if i==0 else 0) for i in range(6)])
        self.assertEqual([o['name'] for o in objects],['Earth','Luna','Mars','Ceres'])
        validate(star,objects)


if __name__=='__main__':unittest.main()
