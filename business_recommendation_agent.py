class BusinessRecommendationAgent:

    def __init__(self):
        pass

    def generate_recommendations(self, demand_results):
        """
        demand_results:
        [
          {
            'zone': 'Z01',
            'demand': 700,
            'drivers': 460,
            'shortage': 240,
            'status': 'SHORTAGE'
          }
        ]
        """

        recommendations = []

        for row in demand_results:

            zone = row["zone"]
            demand = row["demand"]
            drivers = row["drivers"]
            shortage = row["shortage"]
            status = row["status"]

            # ---------------------------
            # BUSINESS RULE ENGINE
            # ---------------------------

            if status == "SHORTAGE" and shortage > 150:
                recommendations.append({
                    "zone": zone,
                    "action": "HIGH_SURGE",
                    "message": (
                        f"🔥 Enable 2.0x–2.5x surge pricing in {zone}. "
                        f"Offer instant driver bonuses."
                    )
                })

            elif status == "SHORTAGE":
                recommendations.append({
                    "zone": zone,
                    "action": "MODERATE_SURGE",
                    "message": (
                        f"⚠️ Enable 1.2x–1.5x surge pricing in {zone}. "
                        f"Push driver incentive alerts."
                    )
                })

            elif status == "SURPLUS" and abs(shortage) > 100:
                recommendations.append({
                    "zone": zone,
                    "action": "MARKETING_PUSH",
                    "message": (
                        f"📣 Excess drivers in {zone}. "
                        f"Run passenger discounts and promotions."
                    )
                })

            elif status == "SURPLUS":
                recommendations.append({
                    "zone": zone,
                    "action": "REDUCE_SUPPLY",
                    "message": (
                        f"🧊 Reduce driver login incentives in {zone}. "
                        f"Suggest repositioning."
                    )
                })

            else:
                recommendations.append({
                    "zone": zone,
                    "action": "STABLE",
                    "message": (
                        f"✅ Zone {zone} operating normally."
                    )
                })

        return recommendations
