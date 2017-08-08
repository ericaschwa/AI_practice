from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    or_list = []
    for rule in rules:
        match_bindings = match(rule.consequent()[0], hypothesis)
        if match_bindings is not None:
            ant = populate(rule.antecedent(), match_bindings)
            if   isinstance(ant, str):
                or_list.append(backchain_to_goal_tree(rules, ant))
            elif isinstance(ant, AND):
                or_list.append(AND([backchain_to_goal_tree(rules, a) for a in ant]))
            elif isinstance(ant, OR):
                or_list.append( OR([backchain_to_goal_tree(rules, a) for a in ant]))
            else:
                print "ERROR:", ant, "is not str, AND, or OR"
    return simplify(OR([hypothesis] + or_list))

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
