"""Validate the entire model-produced plan before any dispatcher sees it."""

import json
import math


class InvalidPlan(ValueError):
    pass


def parse_plan(text, capabilities):
    text = text.strip()
    if not text or len(text) > 262144:
        raise InvalidPlan("Empty or oversized model output")
    if "{" not in text:
        if text.startswith(("[", "```")) or "}" in text:
            raise InvalidPlan("Malformed action output")
        return {"response": text, "face": "speaking", "sound": "speaking"}
    try:
        plan = json.loads(text[text.index("{") : text.rindex("}") + 1])
    except ValueError:
        raise InvalidPlan("Malformed action JSON") from None
    if not isinstance(plan, dict):
        raise InvalidPlan("Expected an action object")
    allowed = {
        "response",
        "movement",
        "action",
        "face",
        "sound",
        "chain",
        "action_chain",
        "face_chain",
        "sound_chain",
    }
    if set(plan) - allowed or not isinstance(plan.get("response", ""), str):
        raise InvalidPlan("Unknown action fields or invalid response")
    for field, names in (
        ("movement", "movements"),
        ("action", "actions"),
        ("face", "faces"),
        ("sound", "sounds"),
    ):
        value = plan.get(field)
        if value is not None and (
            not isinstance(value, str) or value not in capabilities[names]
        ):
            raise InvalidPlan("Unavailable action identifier")
    for field, names in (
        ("chain", "movements"),
        ("action_chain", "actions"),
        ("face_chain", "faces"),
        ("sound_chain", "sounds"),
    ):
        chain = plan.get(field, [])
        if not isinstance(chain, list) or len(chain) > 32:
            raise InvalidPlan("Invalid action chain")
        for item in chain:
            if field == "sound_chain":
                if not isinstance(item, str) or item not in capabilities[names]:
                    raise InvalidPlan("Unavailable sound")
                continue
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("name"), str)
                or item["name"] not in capabilities[names]
            ):
                raise InvalidPlan("Unavailable chain identifier")
            allowed_item = (
                {"name", "duration"}
                if field == "face_chain"
                else {"name", "repetitions"}
            )
            if set(item) - allowed_item:
                raise InvalidPlan("Unknown chain fields")
            if field == "face_chain":
                duration = item.get("duration")
                if duration is not None and (
                    type(duration) not in (int, float)
                    or not math.isfinite(duration)
                    or not 0 < duration <= 60
                ):
                    raise InvalidPlan("Invalid face duration")
            else:
                repetitions = item.get("repetitions", 1)
                if type(repetitions) is not int or not 1 <= repetitions <= 20:
                    raise InvalidPlan("Invalid action repetitions")
    return plan
