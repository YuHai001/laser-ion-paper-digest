from __future__ import annotations

import unittest

from paper_digest.models import infer_ion_species, infer_mechanism, infer_study_type


class ModelInferenceTests(unittest.TestCase):
    def test_infers_new_mechanism_and_cross_direction_terms(self) -> None:
        self.assertEqual(infer_mechanism("Magnetic Vortex Acceleration of ions"), "MVA")
        self.assertEqual(
            infer_mechanism("ion acceleration in the relativistic transparency regime"),
            "relativistic transparency/BOA",
        )
        self.assertEqual(
            infer_study_type("closed-loop Bayesian optimization for laser-driven proton beams"),
            "machine learning/automation",
        )
        self.assertEqual(infer_ion_species("deuteron and carbon ion acceleration"), "carbon, deuteron")
