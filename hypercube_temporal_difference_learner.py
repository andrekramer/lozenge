# code by Claud Sonnet 4.0 (on its release day too) as prompted byt Andre

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

class HypercubeTDLearner:
    """
    Temporal Difference Learning in the Hypercube of Opposites
    
    This implements the TD learning extension proposed in the paper,
    where oppositional tensions are tracked and predicted over time.
    """
    
    def __init__(self, 
                 alpha: float = 0.1,      # Learning rate
                 gamma: float = 0.9,      # Discount factor
                 initial_tension: float = 0.5):  # Initial tension values
        
        self.alpha = alpha
        self.gamma = gamma
        
        # Track oppositional pairs and their tensions
        self.opposites: Dict[str, str] = {}  # concept -> opposite
        self.tensions: Dict[str, float] = {}  # concept -> current tension
        self.value_estimates: Dict[str, float] = {}  # V(A) - estimated future tension
        
        # History tracking for analysis
        self.tension_history: Dict[str, List[float]] = {}
        self.prediction_errors: Dict[str, List[float]] = {}
        self.time_step = 0
        
        self.initial_tension = initial_tension
    
    def add_oppositional_pair(self, concept_a: str, concept_b: str):
        """Add a new oppositional pair to the hypercube"""
        self.opposites[concept_a] = concept_b
        self.opposites[concept_b] = concept_a
        
        # Initialize tensions and value estimates
        self.tensions[concept_a] = self.initial_tension
        self.tensions[concept_b] = 1.0 - self.initial_tension  # Opposites sum to 1
        
        self.value_estimates[concept_a] = self.initial_tension
        self.value_estimates[concept_b] = 1.0 - self.initial_tension
        
        # Initialize history tracking
        self.tension_history[concept_a] = [self.tensions[concept_a]]
        self.tension_history[concept_b] = [self.tensions[concept_b]]
        self.prediction_errors[concept_a] = []
        self.prediction_errors[concept_b] = []
    
    def calculate_tension(self, concept: str) -> float:
        """
        Calculate current tension for a concept
        Tension = |P(A) - P(¬A)| where opposites sum to 1.0
        """
        if concept not in self.tensions:
            return 0.0
        
        opposite = self.opposites.get(concept)
        if opposite and opposite in self.tensions:
            return abs(self.tensions[concept] - self.tensions[opposite])
        return abs(self.tensions[concept] - 0.5)  # Default to neutral opposition
    
    def update_activation(self, concept: str, activation: float):
        """
        Update activation level for a concept (0.0 to 1.0)
        Automatically adjusts opposite to maintain sum = 1.0
        """
        if concept not in self.tensions:
            return
        
        # Clamp activation to valid range
        activation = max(0.0, min(1.0, activation))
        
        # Update concept and its opposite
        self.tensions[concept] = activation
        opposite = self.opposites.get(concept)
        if opposite:
            self.tensions[opposite] = 1.0 - activation
    
    def td_update(self, concept: str, observed_tension: Optional[float] = None):
        """
        Perform TD learning update for oppositional tension prediction
        
        TD Error: δ = r + γV(s') - V(s)
        Where r is the observed tension (reward signal)
        """
        if concept not in self.value_estimates:
            return
        
        # If no observed tension provided, use current calculated tension
        if observed_tension is None:
            observed_tension = self.calculate_tension(concept)
        
        # Current value estimate
        current_value = self.value_estimates[concept]
        
        # TD Error: observed_tension + γ * next_value - current_value
        # For simplicity, we estimate next_value as current_value (can be improved)
        next_value_estimate = current_value  # Could use more sophisticated prediction
        
        td_error = observed_tension + self.gamma * next_value_estimate - current_value
        
        # Update value estimate
        self.value_estimates[concept] = current_value + self.alpha * td_error
        
        # Record for analysis
        self.prediction_errors[concept].append(abs(td_error))
        
        return td_error
    
    def step(self, activations: Dict[str, float] = None):
        """
        Perform one time step of learning
        """
        self.time_step += 1
        
        # Update activations if provided
        if activations:
            for concept, activation in activations.items():
                self.update_activation(concept, activation)
        
        # Perform TD updates for all concepts
        td_errors = {}
        for concept in self.tensions.keys():
            td_error = self.td_update(concept)
            td_errors[concept] = td_error
            
            # Record tension history
            current_tension = self.calculate_tension(concept)
            self.tension_history[concept].append(current_tension)
        
        return td_errors
    
    def predict_future_tension(self, concept: str, steps_ahead: int = 1) -> float:
        """
        Predict future tension using current value estimates
        """
        if concept not in self.value_estimates:
            return 0.0
        
        # Simple prediction based on current value estimate
        # In practice, this could be much more sophisticated
        return self.value_estimates[concept] * (self.gamma ** steps_ahead)
    
    def get_system_state(self) -> Dict:
        """Get current state of the learning system"""
        return {
            'time_step': self.time_step,
            'tensions': dict(self.tensions),
            'value_estimates': dict(self.value_estimates),
            'opposites': dict(self.opposites)
        }
    
    def visualize_learning(self, concept: str = None):
        """
        Visualize the learning progress
        """
        if not self.tension_history:
            print("No learning history to visualize")
            return
        
        concepts_to_plot = [concept] if concept else list(self.tension_history.keys())
        
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot tension evolution
        for concept in concepts_to_plot:
            if concept in self.tension_history:
                axes[0].plot(self.tension_history[concept], label=f'Tension: {concept}')
        
        axes[0].set_title('Tension Evolution Over Time')
        axes[0].set_xlabel('Time Steps')
        axes[0].set_ylabel('Tension Level')
        axes[0].legend()
        axes[0].grid(True)
        
        # Plot prediction errors
        for concept in concepts_to_plot:
            if concept in self.prediction_errors and self.prediction_errors[concept]:
                axes[1].plot(self.prediction_errors[concept], label=f'Pred Error: {concept}')
        
        axes[1].set_title('TD Prediction Errors Over Time')
        axes[1].set_xlabel('Time Steps')
        axes[1].set_ylabel('Absolute TD Error')
        axes[1].legend()
        axes[1].grid(True)
        
        plt.tight_layout()
        plt.show()


# Demonstration and Testing
def demonstrate_hypercube_td_learning():
    """
    Demonstrate the TD learning system with a practical example
    """
    print("=== Hypercube Temporal Difference Learning Demo ===\n")
    
    # Create learner
    learner = HypercubeTDLearner(alpha=0.15, gamma=0.9)
    
    # Add some oppositional pairs
    learner.add_oppositional_pair("safety", "danger")
    learner.add_oppositional_pair("certainty", "uncertainty")
    learner.add_oppositional_pair("approach", "avoidance")
    
    print("Initial state:")
    state = learner.get_system_state()
    for concept, tension in state['tensions'].items():
        print(f"  {concept}: tension={tension:.3f}, value_est={state['value_estimates'][concept]:.3f}")
    print()
    
    # Simulate learning over time with varying activations
    print("Learning simulation:")
    
    scenarios = [
        # Scenario 1: Safety increases, danger decreases
        {"safety": 0.8, "danger": 0.2, "certainty": 0.6, "uncertainty": 0.4},
        {"safety": 0.9, "danger": 0.1, "certainty": 0.7, "uncertainty": 0.3},
        {"safety": 0.85, "danger": 0.15, "certainty": 0.8, "uncertainty": 0.2},
        
        # Scenario 2: Sudden danger spike
        {"safety": 0.2, "danger": 0.8, "certainty": 0.3, "uncertainty": 0.7},
        {"safety": 0.1, "danger": 0.9, "certainty": 0.2, "uncertainty": 0.8},
        
        # Scenario 3: Approach-avoidance conflict
        {"approach": 0.6, "avoidance": 0.4, "safety": 0.5, "danger": 0.5},
        {"approach": 0.7, "avoidance": 0.3, "safety": 0.6, "danger": 0.4},
        {"approach": 0.4, "avoidance": 0.6, "safety": 0.4, "danger": 0.6},
        
        # Scenario 4: Return to equilibrium
        {"safety": 0.5, "danger": 0.5, "certainty": 0.5, "uncertainty": 0.5},
        {"approach": 0.5, "avoidance": 0.5}
    ]
    
    for i, scenario in enumerate(scenarios):
        print(f"Step {i+1}: Activations = {scenario}")
        td_errors = learner.step(scenario)
        
        # Show key metrics
        state = learner.get_system_state()
        safety_tension = learner.calculate_tension("safety")
        safety_prediction = learner.predict_future_tension("safety")
        
        print(f"  Safety tension: {safety_tension:.3f}, predicted: {safety_prediction:.3f}")
        print(f"  TD errors: {[f'{k}: {v:.3f}' for k, v in td_errors.items() if v is not None]}")
        print()
    
    # Show final learned state
    print("Final learned state:")
    final_state = learner.get_system_state()
    for concept in ["safety", "certainty", "approach"]:
        tension = learner.calculate_tension(concept)
        value_est = final_state['value_estimates'][concept]
        print(f"  {concept}: tension={tension:.3f}, value_estimate={value_est:.3f}")
    
    # Demonstrate prediction capability
    print(f"\nPredictions (3 steps ahead):")
    for concept in ["safety", "certainty", "approach"]:
        prediction = learner.predict_future_tension(concept, steps_ahead=3)
        print(f"  {concept}: {prediction:.3f}")
    
    return learner

# Run the demonstration
if __name__ == "__main__":
    learner = demonstrate_hypercube_td_learning()
    
    # Uncomment to see visualization (requires matplotlib)
    learner.visualize_learning("safety")
