"""
--- Day 16: Ticket Translation ---
As you're walking to yet another connecting flight, you realize that one
of the legs of your re-routed trip coming up is on a high-speed train.
However, the train ticket you were given is in a language you don't
understand. You should probably figure out what it says before you get
to the train station after the next flight.

Unfortunately, you can't actually read the words on the ticket. You can,
however, read the numbers, and so you figure out the fields these
tickets must have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and
the numbers on other nearby tickets for the same train service (via the
airport security cameras) together into a single document you can
reference (your puzzle input).

The rules for ticket fields specify a list of fields that exist
somewhere on the ticket and the valid ranges of values for each field.
For example, a rule like class: 1-3 or 5-7 means that one of the fields
in every ticket is named class and can be any value in the ranges 1-3 or
5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is
not).

Each ticket is represented by a single line of comma-separated values.
The values are the numbers on the ticket in the order they appear; every
ticket has the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'

Here, ? represents text in a language you don't understand. This ticket
might be represented as 101,102,103,104,301,302,303,401,402,403; of
course, the actual train tickets you're looking at are much more
complicated. In any case, you've extracted just the numbers in such a
way that the first number is always the same specific field, the second
number is always a different specific field, and so on - you just don't
know what each position actually means!

Start by determining which tickets are completely invalid; these are
tickets that contain values which aren't valid for any field. Ignore
your ticket for now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12

It doesn't matter which position corresponds to which field; you can
identify invalid nearby tickets by considering only whether tickets
contain values that are not valid for any field. In this example, the
values on the first nearby ticket are all valid for at least one field.
This is not true of the other three nearby tickets: the values 4, 55,
and 12 are are not valid for any field. Adding together all of the
invalid values produces your ticket scanning error rate: 4 + 55 + 12 =
71.

Consider the validity of the nearby tickets you scanned. What is your
ticket scanning error rate?

--- Part Two ---
Now that you've identified which tickets contain invalid values, discard
those tickets entirely. Use the remaining valid tickets to determine
which field is which.

Using the valid ranges for each field, determine what order the fields
appear on the tickets. The order is consistent between all tickets: if
seat is the third field, it is the third field on every ticket,
including your ticket.

For example, suppose you have the following notes:

class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9

Based on the nearby tickets in the above example, the first position
must be row, the second position must be class, and the third position
must be seat; you can conclude that in your ticket, class is 12, row is
11, and seat is 13.

Once you work out which field is which, look for the six fields on your
ticket that start with the word departure. What do you get if you
multiply those six values together?
"""
import re
from typing import Dict, List, TextIO, Tuple


def validate_tickets(
        fields: Dict[str, Tuple[int, int, int, int]],
        infile: TextIO) -> Tuple[List[List[int]], List[int]]:
    """Validates the tickets in rest of the file"""
    ranges = list(fields.values())

    valid_tickets: List[List[int]] = []
    invalids: List[int] = []

    for line in infile:
        ticket_values = [int(x) for x in line.split(',')]
        for value in ticket_values:
            for start1, end1, start2, end2 in ranges:
                if start1 <= value <= end1 or start2 <= value <= end2:
                    break
            else:
                invalids.append(value)
                break
        else:
            valid_tickets.append(ticket_values)

    return valid_tickets, invalids


def scan_fields(infile: TextIO) -> Dict[str, Tuple[int, int, int, int]]:
    """Scan all fields in input"""
    field_rules = re.compile(r'^([\w ]+): ([\w\-]+) or ([\w\-]+)$')
    fields: Dict[str, Tuple[int, int, int, int]] = {}

    for line in infile:
        match = field_rules.match(line)
        if match:
            field, range1, range2 = match.groups()
            start1, end1 = (int(x) for x in range1.split('-'))
            start2, end2 = (int(x) for x in range2.split('-'))
            fields[field] = start1, end1, start2, end2
        else:
            break

    return fields


def part1() -> None:
    """Solution for part 1"""

    with open('input.txt') as infile:
        fields = scan_fields(infile)

        for line in infile:
            if line.startswith('nearby tickets'):
                _, invalids = validate_tickets(fields, infile)
                print(sum(invalids))


def guess_fields(
        fields: Dict[str, Tuple[int, int, int, int]],
        tickets: List[List[int]]) -> List[str]:
    """Guess the order of ticket fields"""
    column_count = len(tickets[0])
    possible_indices = {field: set(range(column_count))
                        for field in fields}

    for ticket_values in tickets:
        for index, value in enumerate(ticket_values):
            for field, (start1, end1, start2, end2) in fields.items():
                if start1 <= value <= end1 or start2 <= value <= end2:
                    continue

                # invalid index for field
                possible_indices[field].remove(index)

    # for f, v in possible_indices.items():
    #     print(f, v)

    correct_indices = {}
    while True:
        for field, indices in possible_indices.items():
            if len(indices) == 1:
                index = indices.pop()
                correct_indices[field] = index+1  # 1-indexed
                for _field in possible_indices:
                    try:
                        possible_indices[_field].remove(index)
                    except KeyError:
                        pass
                break
        else:
            break

    # for c, v in correct_indices.items():
    #     print(c, v)

    return []


def part2() -> None:
    """Solution for part 2"""
    with open('input.txt') as infile:
        fields = scan_fields(infile)

        my_ticket: List[int] = []

        for line in infile:
            if line.startswith('your ticket'):
                ticket_line = infile.readline()
                my_ticket = [int(x) for x in ticket_line.split(',')]
                break

        for line in infile:
            if line.startswith('nearby tickets'):
                valid_tickets, _ = validate_tickets(fields, infile)

                print('valid tickets:')
                for v in valid_tickets:
                    print(v)
                print()
                field_names = guess_fields(fields, valid_tickets)
                # print(field_names)


if __name__ == "__main__":
    part1()
    part2()
