from __future__ import annotations

import unittest
from datetime import UTC, datetime

from paper_digest.models import Paper
from paper_digest.ranking import rank_papers, score_paper


CONFIG = {
    "strong_terms": ["laser-driven ion acceleration", "tnsa"],
    "support_terms": ["proton beam", "target", "maximum energy"],
    "exclude_terms": ["ion trap"],
    "minimum_score": 4,
}


def make_paper(title: str, abstract: str) -> Paper:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    return Paper(
        paper_id="2601.00001",
        title=title,
        authors=["A. Researcher"],
        abstract=abstract,
        published=now,
        updated=now,
        url="https://arxiv.org/abs/2601.00001",
        categories=["physics.plasm-ph"],
    )


class RankingTests(unittest.TestCase):
    def test_score_paper_rewards_relevant_terms(self) -> None:
        paper = make_paper(
            "Laser-driven ion acceleration with high quality proton beam",
            "The target improves maximum energy in a TNSA-like regime.",
        )

        score, terms = score_paper(paper, CONFIG)

        self.assertGreaterEqual(score, 10)
        self.assertIn("laser-driven ion acceleration", terms)
        self.assertIn("tnsa", terms)

    def test_rank_papers_filters_excluded_topics(self) -> None:
        relevant = make_paper("Laser-driven ion acceleration", "A proton beam from a target.")
        excluded = make_paper("Ion trap with laser cooling", "This trapped ion work is unrelated.")

        ranked = rank_papers([excluded, relevant], CONFIG)

        self.assertEqual([paper.title for paper in ranked], ["Laser-driven ion acceleration"])
