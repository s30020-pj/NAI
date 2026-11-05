"""
Simplified threat assessment using the Sugeno fuzzy inference method with three input parameters
"""

def calc_threat_score(distance_km, speed_mps, angle_degrees):

    """
    Calculate threat score using Sugeno fuzzy logic.

    Parameters:
        distance_km (float): Distance from radar center in km
        speed_mps (float): Object speed in m/s
        angle_degrees (float): Movement angle in degrees

    Returns:
        float: Threat score between 0 and 100
    """

    far     = max(0, min(1, distance_km / 100))
    fast    = max(0, min(1, speed_mps / 6000))
    away    = max(0, min(1, angle_degrees / 180))

    near    = 1 - far
    slow    = 1 - fast
    toward  = 1 - away

    rules = [
        (far    * slow  * away,     0),
        (far    * fast  * away,     0),
        (near   * slow  * away,     0),
        (near   * fast  * away,     35),
        (far    * slow  * toward,   35),
        (far    * fast  * toward,   65),
        (near   * slow  * toward,   65),
        (near   * fast  * toward,   100),
    ]

    weighted_sum    = 0
    weight_sum      = 0

    for strength, rule_score in rules:
        weighted_sum += strength * rule_score
        weight_sum += strength

    return weighted_sum / weight_sum

def get_threat_status(score):

    """
    Convert threat score into a threat category

    Parameters:
    score (float): Calculated threat score, or None

    Returns:
    str: low, mid, high, critical or unknown
    """

    if score is None:
        return "unknown"
    if score < 25:
        return "low"
    if score < 50:
        return "mid"
    if score < 75:
        return "high"
    return "critical"