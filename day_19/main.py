"""
--- Day 19: Monster Messages ---
You land in an airport surrounded by dense forest. As you walk to your
high-speed train, the Elves at the Mythical Information Bureau contact
you again. They think their satellite has collected an image of a sea
monster! Unfortunately, the connection to the satellite is having
problems, and many of the messages sent back from the satellite have
been corrupted.

They sent you a list of the rules valid messages should obey and a list
of received messages they've collected so far (your puzzle input).

The rules for valid messages (the top part of your puzzle input) are
numbered and build upon each other. For example:

0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

Some rules, like 3: "b", simply match a single character (in this case,
b).

The remaining rules list the sub-rules that must be followed; for
example, the rule 0: 1 2 means that to match rule 0, the text being
checked must match rule 1, and the text after the part that matched rule
1 must then match rule 2.

Some of the rules have multiple lists of sub-rules separated by a pipe
(|). This means that at least one list of sub-rules must match. (The
ones that match might be different each time the rule is encountered.)
For example, the rule 2: 1 3 | 3 1 means that to match rule 2, the text
being checked must match rule 1 followed by rule 3 or it must match rule
3 followed by rule 1.

Fortunately, there are no loops in the rules, so the list of possible
matches will be finite. Since rule 1 matches a and rule 3 matches b,
rule 2 matches either ab or ba. Therefore, rule 0 matches aab or aba.

Here's a more interesting example:

0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

Here, because rule 4 matches a and rule 5 matches b, rule 2 matches two
letters that are the same (aa or bb), and rule 3 matches two letters
that are different (ab or ba).

Since rule 1 matches rules 2 and 3 once each in either order, it must
match two pairs of letters, one pair with matching letters and one pair
with different letters. This leaves eight possibilities:
aaab, aaba, bbab, bbba, abaa, abbb, baaa, or babb.

Rule 0, therefore, matches a (rule 4), then any of the eight options
from rule 1, then b (rule 5):
aaaabb, aaabab, abbabb, abbbab, aabaab, aabbbb, abaaab, or ababbb.

The received messages (the bottom part of your puzzle input) need to be
checked against the rules so you can determine which are valid and which
are corrupted. Including the rules and the messages together, this might
look like:

0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb

Your goal is to determine the number of messages that completely match
rule 0. In the above example, ababbb and abbbab match, but bababa,
aaabbb, and aaaabbb do not, producing the answer 2. The whole message
must match all of rule 0; there can't be extra unmatched characters in
the message. (For example, aaaabbb might appear to match rule 0 above,
but it has an extra unmatched b on the end.)

How many messages completely match rule 0?
"""
import re
from typing import Dict, List, Optional, Tuple


def parse_input() -> Tuple[Dict[int, str], List[str]]:
    """Parses input for day 19"""
    with open('input.txt') as infile:
        rules, messages = [block.splitlines()
                           for block in infile.read().split('\n\n')]

        rule_regex = re.compile(r'^(\d+): (.+)$')
        rule_dict: Dict[int, str] = {}
        for line in rules:
            match = rule_regex.match(line)
            if not match:
                continue

            rule_num_str, rule = match.groups()
            rule_num = int(rule_num_str)

            rule_dict[rule_num] = rule

    return rule_dict, messages


def parse_concat_rule(rule_dict: Dict[int, str], rule: str) -> str:
    """Parses a concat rule (i.e. "a b c ...") into a regex string"""
    rule_nums = [int(num) for num in rule.split()]
    parsed_list = (parse_rule(rule_dict, num) for num in rule_nums)
    parsed_rule = ''.join(parsed_list)
    return parsed_rule


def parse_rule(
        rule_dict: Dict[int, str],
        rule_num: int,
        parsed_rules: Optional[Dict[int, str]] = None) -> str:
    """Recursively parses a rule into a regex string"""
    if parsed_rules is None:
        parsed_rules = {}

    if parsed_rule := parsed_rules.get(rule_num):
        return parsed_rule

    rule = rule_dict[rule_num]

    literal_regex = re.compile(r'^"([ab])"$')
    concat_regex = re.compile(r'^(\d+ )*\d+$')
    concat_or_regex = re.compile(r'^(\d+ )+\|( \d+)+$')

    if concat_or_regex.match(rule):
        group1, group2 = (nums.strip() for nums in rule.split('|'))
        parsed1 = parse_concat_rule(rule_dict, group1)
        parsed2 = parse_concat_rule(rule_dict, group2)

        parsed_rule = parsed1 + '|' + parsed2
        parsed_rules[rule_num] = '(' + parsed_rule + ')'

    elif concat_regex.match(rule):
        parsed_rule = parse_concat_rule(rule_dict, rule)
        parsed_rules[rule_num] = '(' + parsed_rule + ')'

    elif match := literal_regex.match(rule):
        literal, = match.groups()
        parsed_rules[rule_num] = literal

    return parsed_rules[rule_num]


def part1() -> None:
    """Solution for part 1"""
    rule_dict, messages = parse_input()
    regex_str = parse_rule(rule_dict, 0)
    regex = re.compile(regex_str)

    match_count = 0
    for msg in messages:
        if regex.fullmatch(msg):
            match_count += 1

    print(match_count)


if __name__ == "__main__":
    part1()
