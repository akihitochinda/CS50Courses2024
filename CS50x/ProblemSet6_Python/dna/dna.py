import csv
import sys

def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit(1)

    # TODO: Read database file into a variable
    rows = []
    with open(sys.argv[1], 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as file:
        dna_sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence: compute how many times the STR repeats starting at that position by keep checking substrings until the STR repeats no longer.
    subsequences = list(rows[0].keys())[1:]
    result = {}
    for subsequence in subsequences:
        result[subsequence] = longest_match(dna_sequence, subsequence)

    # TODO: Check database for matching profiles by comparing he STR counts against each row in the CSV file
    for person in rows:
        match = 0
        for subsequence in subsequences:
            # int(x) takes the string x and turns it into an integer
            if int(person[subsequence]) == result[subsequence]:
                match += 1
        # check if each STR count matches. If so, print out the person's name
        if match == len(subsequences):
            print(person["name"])
            return

    print("No match")
    return

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
