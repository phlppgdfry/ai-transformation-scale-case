import unittest

from aitx import governance, inventory, load, pilot, portfolio, production, readiness, roadmap, value


class ReadinessTest(unittest.TestCase):
    def test_scores_are_on_the_scale_and_units_weigh_equally(self):
        r = readiness.scores()
        for bu in r["by_bu"].values():
            for v in bu.values():
                self.assertTrue(1 <= v <= 5)
        d = "governance"
        expected = sum(r["by_bu"][bu][d] for bu in r["by_bu"]) / len(r["by_bu"])
        self.assertAlmostEqual(r["group"][d], round(expected, 2), places=2)

    def test_governance_is_the_largest_gap(self):
        self.assertEqual(readiness.scores()["priority_gaps"][0], "governance")


class InventoryTest(unittest.TestCase):
    def setUp(self):
        self.rows = {x["id"]: x for x in inventory.triage()}

    def test_every_initiative_gets_one_decision_and_a_reason(self):
        self.assertEqual(len(self.rows), len(load("initiatives.json")))
        for x in self.rows.values():
            self.assertIn(x["decision"], {"scale", "fix", "merge", "pause", "stop"})
            self.assertTrue(x["reason"])

    def test_shadow_tools_stop(self):
        for x in self.rows.values():
            if x["kind"] == "shadow-tool" and x["decision"] != "pause":
                self.assertEqual(x["decision"], "stop", x["id"])

    def test_ai_act_review_pauses_before_anything_else(self):
        self.assertEqual(self.rows["I-09"]["decision"], "pause")  # CV screening switched on by the vendor
        self.assertEqual(self.rows["I-18"]["decision"], "pause")  # video analytics on customers

    def test_live_but_unmeasured_is_fixed_not_scaled(self):
        self.assertEqual(self.rows["I-15"]["decision"], "fix")


class GovernanceTest(unittest.TestCase):
    def test_recruitment_is_high_risk(self):
        tiers = {x["id"]: x["tier"] for x in governance.register()}
        self.assertEqual(tiers["UC-22"], "High-risk (Annex III)")
        self.assertEqual(tiers["UC-03"], "Transparency")


class PortfolioTest(unittest.TestCase):
    def test_high_risk_is_parked(self):
        cls = {u["id"]: u["class"] for u in portfolio.scored()}
        self.assertEqual(cls["UC-22"], "park")

    def test_first_choice_is_robust(self):
        rb = portfolio.robustness(samples=500)
        self.assertGreater(rb["UC-01"]["top5"], 0.8)

    def test_log_value_score_is_bounded(self):
        for u in portfolio.scored():
            self.assertTrue(1 <= u["value_score"] <= 5)


class RoadmapTest(unittest.TestCase):
    def test_dependencies_and_capacity_hold(self):
        self.assertEqual(roadmap.check(), [])

    def test_parked_use_cases_are_not_scheduled(self):
        scheduled = {u["id"] for u in roadmap.plan()["use_cases"]}
        self.assertNotIn("UC-22", scheduled)

    def test_check_catches_a_violation(self):
        p = roadmap.plan()
        p["use_cases"][0] = {**p["use_cases"][0], "start": 1}
        self.assertTrue(roadmap.check(p))


class ValueTest(unittest.TestCase):
    def test_npv(self):
        self.assertAlmostEqual(value.npv([108, 116.64], 0.08), 200.0, places=6)

    def test_foundations_are_a_cost_to_the_portfolio(self):
        v = value.portfolio_case()
        self.assertLess(v["foundations_npv"], 0)
        self.assertEqual(v["portfolio_npv"], v["use_case_npv"] + v["foundations_npv"])


class PilotTest(unittest.TestCase):
    def test_decision_follows_the_pre_registered_rules(self):
        e = pilot.evaluate()
        self.assertEqual(e["decision"], "GO" if all(e["checks"].values()) else "NO-GO")

    def test_control_group_matters(self):
        e = pilot.evaluate()
        self.assertNotAlmostEqual(e["naive_before_after_pp"], e["results"]["waste_pct"]["effect_pp"], places=1)

    def test_bootstrap_interval_contains_the_estimate(self):
        r = pilot.evaluate()["results"]["waste_pct"]
        self.assertLessEqual(r["ci90"][0], r["effect_pp"])
        self.assertGreaterEqual(r["ci90"][1], r["effect_pp"])


class ProductionTest(unittest.TestCase):
    def test_open_blocking_gates_block(self):
        s = production.status()
        self.assertTrue(s["blockers"])
        self.assertTrue(s["verdict"].startswith("Not ready"))


if __name__ == "__main__":
    unittest.main()
