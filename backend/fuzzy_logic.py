import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def calculate_quality(latency, jitter, packet_loss):

    # ------------------------------------------------
    # INPUT VARIABLES
    # ------------------------------------------------

    latency_var = ctrl.Antecedent(
        np.arange(0, 201, 1),
        "latency"
    )

    jitter_var = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "jitter"
    )

    packet_var = ctrl.Antecedent(
        np.arange(0, 11, 0.1),
        "packet_loss"
    )

    quality_var = ctrl.Consequent(
        np.arange(0, 101, 1),
        "quality"
    )

    # ------------------------------------------------
    # MEMBERSHIP FUNCTIONS
    # ------------------------------------------------

    latency_var["low"] = fuzz.trimf(
        latency_var.universe,
        [0, 0, 40]
    )

    latency_var["medium"] = fuzz.trimf(
        latency_var.universe,
        [20, 60, 100]
    )

    latency_var["high"] = fuzz.trimf(
        latency_var.universe,
        [70, 200, 200]
    )

    jitter_var["low"] = fuzz.trimf(
        jitter_var.universe,
        [0, 0, 10]
    )

    jitter_var["medium"] = fuzz.trimf(
        jitter_var.universe,
        [5, 20, 40]
    )

    jitter_var["high"] = fuzz.trimf(
        jitter_var.universe,
        [30, 100, 100]
    )

    packet_var["low"] = fuzz.trimf(
        packet_var.universe,
        [0, 0, 1]
    )

    packet_var["medium"] = fuzz.trimf(
        packet_var.universe,
        [0.5, 2, 4]
    )

    packet_var["high"] = fuzz.trimf(
        packet_var.universe,
        [3, 10, 10]
    )

    quality_var["poor"] = fuzz.trimf(
        quality_var.universe,
        [0, 0, 40]
    )

    quality_var["average"] = fuzz.trimf(
        quality_var.universe,
        [25, 50, 70]
    )

    quality_var["good"] = fuzz.trimf(
        quality_var.universe,
        [60, 80, 100]
    )

    # ------------------------------------------------
    # FUZZY RULES
    # ------------------------------------------------

    rule1 = ctrl.Rule(
        latency_var["low"] &
        jitter_var["low"] &
        packet_var["low"],
        quality_var["good"]
    )

    rule2 = ctrl.Rule(
        latency_var["medium"] &
        jitter_var["low"] &
        packet_var["low"],
        quality_var["good"]
    )

    rule3 = ctrl.Rule(
        latency_var["medium"] &
        jitter_var["medium"],
        quality_var["average"]
    )

    rule4 = ctrl.Rule(
        latency_var["high"] |
        jitter_var["high"],
        quality_var["poor"]
    )

    rule5 = ctrl.Rule(
        packet_var["high"],
        quality_var["poor"]
    )

    rule6 = ctrl.Rule(
        latency_var["low"] &
        packet_var["medium"],
        quality_var["average"]
    )

    rule7 = ctrl.Rule(
        jitter_var["medium"] &
        packet_var["medium"],
        quality_var["average"]
    )

    rule8 = ctrl.Rule(
        latency_var["high"] &
        packet_var["high"],
        quality_var["poor"]
    )

    system = ctrl.ControlSystem([
        rule1,
        rule2,
        rule3,
        rule4,
        rule5,
        rule6,
        rule7,
        rule8
    ])

    simulation = ctrl.ControlSystemSimulation(system)

    # ------------------------------------------------
    # INPUT
    # ------------------------------------------------

    latency_input = min(max(latency, 0), 200)
    jitter_input = min(max(jitter, 0), 100)
    packet_input = min(max(packet_loss, 0), 10)

    simulation.input["latency"] = latency_input
    simulation.input["jitter"] = jitter_input
    simulation.input["packet_loss"] = packet_input

    # ------------------------------------------------
    # CALCULATE
    # ------------------------------------------------

    simulation.compute()

    score = float(simulation.output["quality"])

    if score < 40:
        category = "Poor"
    elif score < 70:
        category = "Average"
    else:
        category = "Good"

    # ------------------------------------------------
    # MEMBERSHIP VALUES
    # ------------------------------------------------

    latency_membership = {
        "low": round(
            fuzz.interp_membership(
                latency_var.universe,
                latency_var["low"].mf,
                latency_input
            ), 2
        ),
        "medium": round(
            fuzz.interp_membership(
                latency_var.universe,
                latency_var["medium"].mf,
                latency_input
            ), 2
        ),
        "high": round(
            fuzz.interp_membership(
                latency_var.universe,
                latency_var["high"].mf,
                latency_input
            ), 2
        )
    }

    jitter_membership = {
        "low": round(
            fuzz.interp_membership(
                jitter_var.universe,
                jitter_var["low"].mf,
                jitter_input
            ), 2
        ),
        "medium": round(
            fuzz.interp_membership(
                jitter_var.universe,
                jitter_var["medium"].mf,
                jitter_input
            ), 2
        ),
        "high": round(
            fuzz.interp_membership(
                jitter_var.universe,
                jitter_var["high"].mf,
                jitter_input
            ), 2
        )
    }

    packet_membership = {
        "low": round(
            fuzz.interp_membership(
                packet_var.universe,
                packet_var["low"].mf,
                packet_input
            ), 2
        ),
        "medium": round(
            fuzz.interp_membership(
                packet_var.universe,
                packet_var["medium"].mf,
                packet_input
            ), 2
        ),
        "high": round(
            fuzz.interp_membership(
                packet_var.universe,
                packet_var["high"].mf,
                packet_input
            ), 2
        )
    }

    return {
        "score": round(score, 2),
        "category": category,
        "membership": {
            "latency": latency_membership,
            "jitter": jitter_membership,
            "packet_loss": packet_membership
        },
        "rules_count": 8
    }