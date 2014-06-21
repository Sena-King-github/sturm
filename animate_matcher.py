"""
Animate matching a set of literal patterns against a string.
"""

import sturm

def main():
    with sturm.cbreak_mode():
        run(['rat', 'cat', 'catalog'], 'cats are fat')

def run(patterns, string):
    i = 0
    tails = patterns

    while True:
        show_states = (((pattern or sturm.green('match!')), '\n')
                       for pattern in sorted(tails))
        sturm.render((show_states, '\n',
                      string[:i], sturm.cursor, string[i:]))
        key = sturm.get_key()
        if key == sturm.esc: break
        if i == len(string): break

        ch = string[i]
        tails = [tail[1:] for tail in tails if tail.startswith(ch)]
        i += 1

# From github.com/darius/regexercise_solutions -- this is the logic
# eviscerated above.
def search(strings, chars):
    """Given a sequence of strings and an iterator of chars, return True
    if any of the strings would be a prefix of ''.join(chars); but
    only consume chars up to the end of the match."""
    if not all(strings):
        return True
    tails = strings
    for ch in chars:
        tails = [tail[1:] for tail in tails if tail[0] == ch]
        if not all(tails):
            return True
    return False

if __name__ == '__main__':
    main()
