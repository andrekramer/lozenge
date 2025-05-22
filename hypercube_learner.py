# Coded by Gemini-2.5-pro (preview-05-06) as prompted by Andre Kramer
import random
import matplotlib.pyplot as plt

class HypercubeLearner2D:
    def __init__(self, dim1_name="Bell", dim2_name="Food", learning_rate=0.1,
                 p_dim1_prior=0.5, p_dim2_prior=0.1):
        """
        Initializes the 2D hypercube learner.
        Args:
            dim1_name (str): Name of the first dimension (e.g., "Bell").
            dim2_name (str): Name of the second dimension (e.g., "Food").
            learning_rate (float): η, how much to adjust weights per trial.
            p_dim1_prior (float): Agent's general prior expectation of dim1's positive pole being active.
            p_dim2_prior (float): Agent's general prior expectation of dim2's positive pole being active (baseline).
        """
        self.dim1_name = dim1_name
        self.dim2_name = dim2_name
        self.w_12 = 0.0  # Weight representing association between dim1 and dim2.
                         # w_12 > 0: dim1 predicts dim2
                         # w_12 < 0: dim1 predicts NOT dim2
        self.eta = learning_rate
        self.p_dim1_prior = p_dim1_prior
        self.p_dim2_prior = p_dim2_prior
        self.history = []

    def _clip_probability(self, value):
        return max(0.0, min(1.0, value))

    def get_dim2_expectation(self, dim1_actual_state):
        """
        Calculates the expected probability of dim2's positive pole being active,
        given the actual state of dim1 and the current learned association w_12.
        Args:
            dim1_actual_state (int): 0 or 1, the observed state of dimension 1.
        Returns:
            float: Expected probability of dim2's positive pole.
        """
        # This represents P(Dim2_active | Dim1_state, w_12)
        # If dim1_actual_state is 1, the learned association w_12 fully contributes.
        # If dim1_actual_state is 0, w_12's direct contribution (as modeled here) is nullified.
        # This models a simple scenario where dim1 is a cue for dim2.
        raw_expectation = self.p_dim2_prior + (self.w_12 * dim1_actual_state)
        return self._clip_probability(raw_expectation)

    def update(self, x1_actual, x2_actual):
        """
        Update the association weight w_12 based on an observation (a node in the 2D hypercube).
        Args:
            x1_actual (int): Observed state of dimension 1 (0 or 1).
            x2_actual (int): Observed state of dimension 2 (0 or 1).
        """
        # 1. Surprise for dimension 1
        # (Observed state of dim1 - Prior expectation of dim1)
        surprise_dim1 = x1_actual - self.p_dim1_prior

        # 2. Expected state of dimension 2, given the observed state of dimension 1
        # This uses the current learned association w_12.
        p_dim2_expected_this_trial = self.get_dim2_expectation(x1_actual)

        # 3. Surprise for dimension 2
        # (Observed state of dim2 - Expected state of dim2 in this trial)
        surprise_dim2 = x2_actual - p_dim2_expected_this_trial

        # 4. Update the weight w_12
        # The product captures correlated deviation.
        delta_w_12 = self.eta * surprise_dim1 * surprise_dim2
        self.w_12 += delta_w_12

        # Store history
        self.history.append({
            'trial': len(self.history) + 1,
            'x1': x1_actual,
            'x2': x2_actual,
            'p_dim1_prior': self.p_dim1_prior,
            'p_dim2_expected': p_dim2_expected_this_trial,
            'surprise_dim1': surprise_dim1,
            'surprise_dim2': surprise_dim2,
            'delta_w_12': delta_w_12,
            'w_12': self.w_12,
            f'E[{self.dim2_name}|{self.dim1_name}=1]': self.get_dim2_expectation(1), # Current prediction if dim1 is active
            f'E[{self.dim2_name}|{self.dim1_name}=0]': self.get_dim2_expectation(0)  # Current prediction if dim1 is inactive
        })

    def print_trial_info(self, trial_data):
        print(f"Trial {trial_data['trial']}: {self.dim1_name}={trial_data['x1']}, {self.dim2_name}={trial_data['x2']}. "
              f"w_12={trial_data['w_12']:.3f}. "
              f"E[{self.dim2_name}|{self.dim1_name}=1]={trial_data[f'E[{self.dim2_name}|{self.dim1_name}=1]']:.3f}")

# --- Simulation ---
learner = HypercubeLearner2D(dim1_name="Bell", dim2_name="Food",
                             learning_rate=0.2,
                             p_dim1_prior=0.5,  # Bell rings 50% of the time in general (prior)
                             p_dim2_prior=0.05) # Food appears 5% of the time without any cue (baseline)

print("--- Phase 1: Learning Association (Bell -> Food) ---")
# Node: (Bell=1, Food=1)
num_trials_phase1 = 20
for i in range(num_trials_phase1):
    learner.update(x1_actual=1, x2_actual=1) # Bell rings, Food is present
    learner.print_trial_info(learner.history[-1])

print(f"\nLearned w_12 after Phase 1: {learner.w_12:.4f}")
print(f"Current expectation of Food if Bell rings: {learner.get_dim2_expectation(1):.4f}")
print(f"Current expectation of Food if NO Bell rings: {learner.get_dim2_expectation(0):.4f}")


print("\n--- Phase 2: Extinction (Bell -> No Food) ---")
# Node: (Bell=1, Food=0)
num_trials_phase2 = 15
for i in range(num_trials_phase2):
    learner.update(x1_actual=1, x2_actual=0) # Bell rings, Food is ABSENT
    learner.print_trial_info(learner.history[-1])

print(f"\nLearned w_12 after Phase 2: {learner.w_12:.4f}")
print(f"Current expectation of Food if Bell rings: {learner.get_dim2_expectation(1):.4f}")


print("\n--- Phase 3: Learning Negative Correlation (Bell -> No Food from scratch) ---")
# Reset learner for a different scenario
learner_neg = HypercubeLearner2D(dim1_name="Bell", dim2_name="Food", learning_rate=0.2,
                                  p_dim1_prior=0.5, p_dim2_prior=0.5) # Higher food baseline for clearer neg corr.
num_trials_phase3 = 20
for i in range(num_trials_phase3):
    learner_neg.update(x1_actual=1, x2_actual=0) # Bell rings, Food is ABSENT
    learner_neg.print_trial_info(learner_neg.history[-1])

print(f"\nLearned w_12 after Phase 3: {learner_neg.w_12:.4f}")
print(f"Current expectation of Food if Bell rings: {learner_neg.get_dim2_expectation(1):.4f}")


print("\n--- Phase 4: No Correlation (Food appears randomly regardless of Bell) ---")
learner_no_corr = HypercubeLearner2D(dim1_name="Bell", dim2_name="Food", learning_rate=0.1,
                                     p_dim1_prior=0.5, p_dim2_prior=0.5)
num_trials_phase4 = 50
for i in range(num_trials_phase4):
    bell_rings = random.choice([0, 1])
    food_present = random.choice([0, 1]) # Food is completely random
    learner_no_corr.update(x1_actual=bell_rings, x2_actual=food_present)
    if (i + 1) % 10 == 0: # Print every 10 trials
        learner_no_corr.print_trial_info(learner_no_corr.history[-1])

print(f"\nLearned w_12 after Phase 4 (random): {learner_no_corr.w_12:.4f}")
print(f"Current expectation of Food if Bell rings: {learner_no_corr.get_dim2_expectation(1):.4f}")
print(f"Current expectation of Food if NO Bell rings: {learner_no_corr.get_dim2_expectation(0):.4f} (should be close to p_dim2_prior)")


# Plotting for the first learner (Phases 1 & 2)
history_to_plot = learner.history
trials = [h['trial'] for h in history_to_plot]
w_12_values = [h['w_12'] for h in history_to_plot]
e_dim2_if_dim1_active = [h[f'E[{learner.dim2_name}|{learner.dim1_name}=1]'] for h in history_to_plot]

plt.figure(figsize=(12, 7))
plt.subplot(2,1,1)
plt.plot(trials, w_12_values, label=f'w_12 ({learner.dim1_name}-{learner.dim2_name} Assoc. Strength)')
plt.axvline(num_trials_phase1, color='gray', linestyle=':', label='End Phase 1 (Learning)')
plt.title(f"Learning Association between {learner.dim1_name} and {learner.dim2_name}")
plt.ylabel("Weight w_12")
plt.legend()
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(trials, e_dim2_if_dim1_active, label=f'E[{learner.dim2_name} | {learner.dim1_name}=1] (Learned Expectation)', color='orange')
plt.axvline(num_trials_phase1, color='gray', linestyle=':', label='End Phase 1 (Learning)')
plt.xlabel("Trial Number")
plt.ylabel("Conditional Probability")
plt.ylim(0, 1.05)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
