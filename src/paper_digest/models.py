from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Paper:
    paper_id: str
    title: str
    authors: list[str]
    abstract: str
    published: datetime
    updated: datetime
    url: str
    pdf_url: str | None = None
    doi: str | None = None
    primary_category: str | None = None
    categories: list[str] = field(default_factory=list)
    comment: str | None = None
    score: int = 0
    matched_terms: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PaperSummary:
    one_sentence: str
    mechanism: str
    study_type: str
    laser_parameters: str
    target: str
    ion_species: str
    max_energy: str
    main_contribution: str
    limitations: str
    why_it_matters: str

    @classmethod
    def fallback(cls, paper: Paper) -> "PaperSummary":
        abstract = " ".join(paper.abstract.split())
        if len(abstract) > 280:
            abstract = abstract[:277].rstrip() + "..."
        mechanism = infer_mechanism(paper.title + " " + paper.abstract)
        return cls(
            one_sentence=abstract or "摘要为空，需阅读原文确认主要贡献。",
            mechanism=mechanism,
            study_type=infer_study_type(paper.title + " " + paper.abstract),
            laser_parameters="摘要中未明确说明",
            target="摘要中未明确说明",
            ion_species=infer_ion_species(paper.title + " " + paper.abstract),
            max_energy="摘要中未明确说明",
            main_contribution="基于标题和摘要，该论文与激光离子加速相关，建议阅读全文确认实验或模拟细节。",
            limitations="未进行全文解析，局限性需从正文判断。",
            why_it_matters="该条目被关键词和分类规则识别为相关，可作为每日跟踪候选。",
        )


def infer_mechanism(text: str) -> str:
    lowered = text.lower()
    if "target normal sheath" in lowered or "tnsa" in lowered:
        return "TNSA"
    if "radiation pressure" in lowered or " rpa" in lowered:
        return "RPA"
    if "hole boring" in lowered:
        return "hole-boring"
    if "shock acceleration" in lowered or "collisionless shock" in lowered:
        return "collisionless shock acceleration"
    if "breakout afterburner" in lowered or " boa" in lowered:
        return "BOA"
    if "magnetic vortex" in lowered or " mva" in lowered:
        return "MVA"
    if "relativistic transparency" in lowered or "break-out afterburner" in lowered:
        return "relativistic transparency/BOA"
    return "未明确归类"


def infer_study_type(text: str) -> str:
    lowered = text.lower()
    if "review" in lowered:
        return "review"
    if "experiment" in lowered or "measured" in lowered or "demonstrate" in lowered:
        return "experiment"
    if "simulation" in lowered or "particle-in-cell" in lowered or " pic " in f" {lowered} ":
        return "simulation"
    if "machine learning" in lowered or "bayesian optimization" in lowered or "bayesian optimisation" in lowered:
        return "machine learning/automation"
    if "closed-loop" in lowered or "automated optimization" in lowered or "automated optimisation" in lowered:
        return "machine learning/automation"
    if "theory" in lowered or "model" in lowered:
        return "theory/model"
    return "未明确说明"


def infer_ion_species(text: str) -> str:
    lowered = text.lower()
    species = []
    if "proton" in lowered:
        species.append("proton")
    if "carbon" in lowered or "c6+" in lowered:
        species.append("carbon")
    if "helium" in lowered or "alpha particle" in lowered:
        species.append("helium")
    if "deuteron" in lowered or "deuterium" in lowered:
        species.append("deuteron")
    if "heavy ion" in lowered:
        species.append("heavy ion")
    if "ion" in lowered and not species:
        species.append("ion")
    return ", ".join(species) if species else "摘要中未明确说明"
