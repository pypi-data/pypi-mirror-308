
class CostAnalyzer:
    def __init__(self, base_costs, cost_multipliers):
        """
        Initializes the CostAnalyzer with configurable costs and multipliers.
        
        :param base_costs: A dictionary with base costs for each category (e.g., vehicle types).
                           Example: {'car': 1000, 'motorbike': 500}
        :param cost_multipliers: A nested dictionary with multipliers for each type and level.
                                 Example: {
                                     'accident': {'moderate': 1.5, 'severe': 2.0},
                                     'fire': {'moderate': 2.0, 'severe': 3.0}
                                 }
        """
        self.base_costs = base_costs
        self.cost_multipliers = cost_multipliers

    def calculate_cost(self, category, incident_type, level):
        """
        Calculates the estimated cost based on category, incident type, and severity level.

        :param category: The primary category for cost calculation (e.g., vehicle type).
        :param incident_type: The type of incident or scenario affecting the cost.
        :param level: The level or severity of the incident.
        :return: Calculated estimated cost.
        :raises ValueError: If any input parameter is invalid.
        """
        if category not in self.base_costs:
            raise ValueError(f"Invalid category: {category}. Supported categories: {list(self.base_costs.keys())}")
        
        if incident_type not in self.cost_multipliers:
            raise ValueError(f"Invalid incident type: {incident_type}. Supported types: {list(self.cost_multipliers.keys())}")
        
        if level not in self.cost_multipliers[incident_type]:
            raise ValueError(f"Invalid level: {level}. Supported levels: {list(self.cost_multipliers[incident_type].keys())}")

        # Calculate cost based on the base cost and multiplier
        base_cost = self.base_costs[category]
        multiplier = self.cost_multipliers[incident_type][level]
        estimated_cost = base_cost * multiplier

        return estimated_cost
