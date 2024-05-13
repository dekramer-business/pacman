from pacai.agents.learning.value import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate=0.9, iters=100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the values for each state.

        # Compute the values here.
        # use value iteration iters number of times, store
        oldValues = {}
        states = mdp.getStates()
        for i in range(0, iters):  # for each iteration
            for state in states:  # for each state
                max_val = None
                for action in mdp.getPossibleActions(state):
                    avg_val = 0
                    for (next_state, prob) in mdp.getTransitionStatesAndProbs(state, action):
                        avg_val += prob * (mdp.getReward(state, action, next_state)
                             + (discountRate * oldValues.get(next_state, 0)))

                    if (max_val is None) or (avg_val > max_val):  # Set max val on first pass
                        max_val = avg_val
                if max_val is None:  # Catches terminal states
                    max_val = 0
                self.values[state] = max_val
            oldValues.update(self.values)

    def getPolicy(self, state):
        """
        The policy is the best action in the given state
        according to the values computed by value iteration.
        You may break ties any way you see fit.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return None.
        """

        best_action = None
        max_val = None
        for action in self.mdp.getPossibleActions(state):
            avg_val = 0
            for (next_state, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
                avg_val += prob * (self.mdp.getReward(state, action, next_state)
                                   + (self.discountRate * self.values.get(next_state, 0)))
            if (max_val is None) or (avg_val > max_val):
                max_val = avg_val
                best_action = action

        return best_action

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)

    def getQValue(self, state, action):
        """
        The q-value of the state action pair (after the indicated number of value iteration passes).
        Note that value iteration does not necessarily create this quantity,
        and you may have to derive it on the fly.

        Take an action, then get avg of all those values
        """

        qval = 0
        for (next_state, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
            qval += prob * (self.mdp.getReward(state, action, next_state)
                            + (self.discountRate * self.values.get(next_state, 0)))

        return qval
