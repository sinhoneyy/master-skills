#!/usr/bin/env python3
"""Exercise a vendored Product Design Harness without executing host instructions."""
import copy
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RESOURCE = ROOT / "skills/product-design-harness/resources"
sys.path.insert(0, str(RESOURCE / "scripts"))
from check_review import check, check_handoff
from check_override import check as check_override


def load(relative):
    return json.loads((RESOURCE / relative).read_text(encoding="utf-8"))


def require(ok, label):
    if not ok:
        raise AssertionError(label)
    print("PASS", label)


def main():
    reviews = [
        "quick-gate-review.json", "standard-gate-review.json",
        "ux3-council-review.json", "stop-reframe-review.json",
        "live-coding-review.json",
    ]
    for filename in reviews:
        document = load("examples/" + filename)
        require(not check(document), "valid " + filename)
    for name in ("quick", "live-coding"):
        review = load("examples/" + ("quick-gate-review.json" if name == "quick" else "live-coding-review.json"))
        pack = load("examples/" + name + "-context-pack.json")
        require(not check_handoff(review, pack), "valid " + name + " handoff")
        bad = copy.deepcopy(pack)
        bad["scope"] = ["Unapproved expansion"]
        require(bool(check_handoff(review, bad)), "reject expanded " + name + " scope")
    review = load("examples/quick-gate-review.json")
    bad = copy.deepcopy(review)
    bad["combined_verdict"] = "verify"
    require(bool(check(bad)), "reject inconsistent combined verdict")
    bad = copy.deepcopy(review)
    bad["weakest_flow"] = "business"
    require(bool(check(bad)), "reject inconsistent weakest flow")
    bad = copy.deepcopy(review)
    bad["evidence_tier"] = "t4"
    require(bool(check(bad)), "reject inconsistent headline evidence tier")
    stop = load("examples/stop-reframe-review.json")
    override = load("examples/verdict-override.json")
    require(not check_override(override, stop), "valid override")
    bad = copy.deepcopy(override)
    bad["expires_at"] = "2000-01-01T00:00:00Z"
    require(bool(check_override(bad, stop)), "reject expired override")
    bad = copy.deepcopy(override)
    bad["authorized_scope"]["may_do"].append(stop["execution_boundary"]["must_not_do"][0])
    require(bool(check_override(bad, stop)), "reject exactly prohibited override action")
    # Known upstream limitation: whitespace-padded overrides are not rejected.
    # Do not advertise this validator as a security authorization boundary.
    print("KNOWN GAP: whitespace-padded prohibited override (upstream PR #23)")
    for filename in ("ux3-model.svg", "intersections.svg", "product-vs-coding-harness.svg"):
        if not (RESOURCE / "assets" / filename).exists():
            print("KNOWN GAP: missing upstream SVG:", filename)
    print("Validation complete (known upstream limitations remain disclosed).")


if __name__ == "__main__":
    main()
