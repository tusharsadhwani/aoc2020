"""
--- Day 18: Operation Order ---
As you look out the window and notice a heavily-forested continent
slowly appear over the horizon, you are interrupted by the child sitting
next to you. They're curious if you could help them with their math
homework.

Unfortunately, it seems like this "math" follows different rules than
you remember.

The homework (your puzzle input) consists of a series of expressions
that consist of addition (+), multiplication (*), and parentheses
((...)). Just like normal math, parentheses indicate that the expression
inside must be evaluated before it can be used by the surrounding
expression. Addition still finds the sum of the numbers on both sides of
the operator, and multiplication still finds the product.

However, the rules of operator precedence have changed. Rather than
evaluating multiplication before addition, the operators have the same
precedence, and are evaluated left-to-right regardless of the order in
which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6
are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71

Parentheses can override this order; for example, here is what happens
if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51

Here are a few more examples:

- 2 * 3 + (4 * 5) becomes 26.
- 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
- 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
- ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

Before you can help with the homework, you need to understand it
yourself. Evaluate the expression on each line of the homework; what is
the sum of the resulting values?

--- Part Two ---
You manage to answer the child's questions and they finish part 1 of
their homework, but get stuck when they reach the next section:
advanced math.

Now, addition and multiplication have different precedence levels, but
they're not the ones you're familiar with. Instead, addition is
evaluated before multiplication.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6
are now as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
  3   *   7   * 5 + 6
  3   *   7   *  11
     21       *  11
         231

Here are the other examples from above:

- 1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
- 2 * 3 + (4 * 5) becomes 46.
- 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
- 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
- ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.

What do you get if you add up the results of evaluating the homework
problems using these new rules?
"""

from typing import List


def is_higher_precedence(operator: str, operator_stack: List[str]) -> bool:
    """If the operator is of higher precedence than top of the stack"""
    stack_top = operator_stack[-1]
    if operator == '*' and stack_top == '+':
        return True

    return False


def evaluate(operand1: int, operand2: int, operator: str) -> int:
    """Evaluate expression"""
    if operator == '+':
        return operand1 + operand2
    if operator == '*':
        return operand1 * operand2

    raise AssertionError('Invalid operator value', operator)


def process_operation(
        operand_stack: List[int],
        operator_stack: List[str]) -> None:
    """Process the top operator and two top operands from the stacks"""
    operator = operator_stack.pop()
    operand1 = operand_stack.pop()
    operand2 = operand_stack.pop()

    result = evaluate(operand1, operand2, operator)
    operand_stack.append(result)


def part1() -> None:
    """Solution for part 1"""
    with open('input.txt') as infile:
        lines = infile.read().splitlines()

    total = 0
    for line in lines:
        operand_stack: List[int] = []
        operator_stack: List[str] = []

        for char in line:
            if char == ' ':
                continue

            if char == '(':
                operator_stack.append(char)

            elif char.isdigit():
                operand_stack.append(int(char))

            elif char in ['+', '*']:
                while operator_stack:
                    operator_stack_top = operator_stack[-1]
                    if operator_stack_top == '(':
                        break

                    process_operation(operand_stack, operator_stack)

                operator_stack.append(char)

            elif char == ')':
                opening_parenthesis_found = False
                while not opening_parenthesis_found:
                    operator_stack_top = operator_stack[-1]
                    if operator_stack_top == '(':
                        opening_parenthesis_found = True
                        operator_stack.pop()
                    else:
                        process_operation(operand_stack, operator_stack)

            else:
                raise AssertionError(f'unknown character: {char}')

        while operator_stack:
            process_operation(operand_stack, operator_stack)

        result = operand_stack.pop()
        assert len(operand_stack) == 0, 'Non-empty stack'
        total += result

    print(total)


def part2() -> None:
    """Solution for part 2"""
    with open('input.txt') as infile:
        lines = infile.read().splitlines()

    total = 0
    for line in lines:
        operand_stack: List[int] = []
        operator_stack: List[str] = []

        for char in line:
            if char == ' ':
                continue

            if char == '(':
                operator_stack.append(char)

            elif char.isdigit():
                operand_stack.append(int(char))

            elif char in ['+', '*']:
                while operator_stack:
                    operator_stack_top = operator_stack[-1]
                    if operator_stack_top == '(':
                        break

                    if is_higher_precedence(char, operator_stack):
                        process_operation(operand_stack, operator_stack)
                    else:
                        break

                operator_stack.append(char)

            elif char == ')':
                opening_parenthesis_found = False
                while not opening_parenthesis_found:
                    operator_stack_top = operator_stack[-1]
                    if operator_stack_top == '(':
                        opening_parenthesis_found = True
                        operator_stack.pop()
                    else:
                        process_operation(operand_stack, operator_stack)

            else:
                raise AssertionError(f'unknown character: {char}')

        while operator_stack:
            process_operation(operand_stack, operator_stack)

        result = operand_stack.pop()
        assert len(operand_stack) == 0, 'Non-empty stack'
        total += result

    print(total)


if __name__ == "__main__":
    part1()
    part2()
