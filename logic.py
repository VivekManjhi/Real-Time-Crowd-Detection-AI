def analyze_problems(data):

    result = {}

    for gate, count in data.items():

        if count > 30:
            result[gate] = "🔴 OVERCROWDED"
        elif count > 15:
            result[gate] = "🟡 MODERATE"
        else:
            result[gate] = "🟢 SAFE"

    best_gate = min(data, key=data.get)
    result["best_gate"] = "BEST ENTRY → " + best_gate.upper()

    return result