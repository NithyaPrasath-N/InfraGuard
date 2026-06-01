class RiskEngine:

    RISK_POINTS = {
        "LOW": 10,
        "MEDIUM": 25,
        "HIGH": 50,
        "CRITICAL": 100
    }

    def calculate_score(self, findings):

        score = 0

        for finding in findings:

            if finding["drift"]:

                score += self.RISK_POINTS.get(
                    finding["risk"],
                    0
                )

        return score

    def get_status(self, score):

        if score >= 100:
            return "CRITICAL"

        if score >= 50:
            return "WARNING"

        return "HEALTHY"
