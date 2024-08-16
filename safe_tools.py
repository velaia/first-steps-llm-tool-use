# write a function count_characters that takes a string as input and returns the number of times the character n occurs in the string
def count_characters(word_phrase, chr):
    return word_phrase.count(chr)

# test the function
assert count_characters("functioning", "n") == 3