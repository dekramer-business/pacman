"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    Low noise means the agent always acts optimally
    (I think optimally is the right word for it)
    They always go where they want to
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    Low noise means they brave cliff
    High discount means they choose closer
    High discount means its highly discounted, discount bad word
    """

    answerDiscount = 0.3
    answerNoise = 0.0
    answerLivingReward = 0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    High noise means they fear the cliff
    Low discount means they choose farther
    """

    answerDiscount = 0.9
    answerNoise = 0.5
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    Low noise means brave the cliff
    Low discount means they choose farther
    """

    answerDiscount = 0.9
    answerNoise = 0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    High noise means fear the cliff
    Low discount means they choose farther
    """

    answerDiscount = 0.9
    answerNoise = 0.4
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return NOT_POSSIBLE

def question6():
    """
    [Enter a description of what you did here.]
    """

    answerEpsilon = 0.3
    answerLearningRate = 0.5

    return answerEpsilon, answerLearningRate

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
