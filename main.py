import time
from bs4 import BeautifulSoup

class BruteForce:
    @staticmethod
    def search(text, pattern):
        n = len(text)
        m = len(pattern)
        comparisons = 0
        occurrences = []

        for i in range(n - m + 1):
            j = 0
            while j < m:
                comparisons += 1
                if text[i + j] != pattern[j]:
                    break
                j += 1
            if j == m:
                occurrences.append(i)
        return occurrences, comparisons


class BoyerMoore:
    @staticmethod
    def preprocess_strong_suffix(shift, bpos, pattern, m):
        i = m
        j = m + 1
        bpos[i] = j

        while i > 0:
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                if shift[j] == 0:
                    shift[j] = j - i
                j = bpos[j]
            i -= 1
            j -= 1
            bpos[i] = j

    @staticmethod
    def preprocess_case2(shift, bpos, pattern, m):
        j = bpos[0]
        for i in range(m + 1):
            if shift[i] == 0:
                shift[i] = j
            if i == j:
                j = bpos[j]

    @staticmethod
    def search(text, pattern):
        n = len(text)
        m = len(pattern)
        comparisons = 0
        occurrences = []

        shift = [0 for _ in range(m + 1)]
        bpos = [0 for _ in range(m + 1)]

        BoyerMoore.preprocess_strong_suffix(shift, bpos, pattern, m)
        BoyerMoore.preprocess_case2(shift, bpos, pattern, m)

        # Print the bad character table and good suffix table
        print('Bad Symbol Table:')
        for i, c in enumerate(pattern):
            print(f'{c}: {shift[i + 1]}')

        print('Good Suffix Table:')
        for i in range(m):
            print(f'{pattern[i:]}: {shift[i + 1]}')
        print("\n")

        s = 0
        while s <= n - m:
            j = m - 1
            while j >= 0 and pattern[j] == text[s + j]:
                comparisons += 1
                j -= 1
            if j < 0:
                occurrences.append(s)
                s += shift[0] if s + m < n else 1
            else:
                s += shift[j + 1]
        return occurrences, comparisons

class Horspool:
    @staticmethod
    def preprocess_bad_char_table(pattern):
        m = len(pattern)
        bad_char_table = [-1] * 256  # Assume ASCII character set

        # Fill the table with the last occurrence of each character in the pattern
        for i in range(m):
            char_code = ord(pattern[i])
            if char_code < 256:
                bad_char_table[char_code] = i

        return bad_char_table

    @staticmethod
    def search(text, pattern):
        n = len(text)
        m = len(pattern)
        comparisons = 0
        occurrences = []

        bad_char_table = Horspool.preprocess_bad_char_table(pattern)

        # Print the bad character table
        print('Bad Symbol Table:')
        for i, val in enumerate(bad_char_table):
            if val != -1:
                print(f'{chr(i)}: {val}')

        print("\n")

        s = 0
        while s <= n - m:
            j = m - 1
            while j >= 0 and pattern[j] == text[s + j]:
                comparisons += 1
                j -= 1
            if j < 0:
                occurrences.append(s)
                s += (m - bad_char_table[ord(text[s + m])] if s + m < n and ord(text[s + m]) < 256 else 1)
            else:
                s += max(1, j - bad_char_table[ord(text[s + j])] if ord(text[s + j]) < 256 else m)
        return occurrences, comparisons

def highlight_occurrences(html_text, pattern, occurrences):
    for occurrence in reversed(occurrences):
        html_text = html_text[:occurrence] + "<mark>" + html_text[
                                                        occurrence:occurrence + len(pattern)] + "</mark>" + html_text[
                                                                                                            occurrence + len(
                                                                                                                pattern):]
    return html_text


def run_algorithm(algorithm, html_file, patterns):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_text = file.read()

    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text()

    for pattern in patterns:
        start_time = time.time()
        occurrences, comparisons = algorithm.search(text, pattern)
        end_time = time.time()
        running_time = end_time - start_time

        print(f"Pattern: {pattern}")
        print(f"Occurrences: {len(occurrences)}")
        print(f"Comparisons: {comparisons}")
        print(f"Running time: {running_time} seconds")
        print("-" * 40)

        html_text = highlight_occurrences(html_text, pattern, occurrences)

        with open(f"highlighted_{html_file}", 'w', encoding='utf-8') as file:
            file.write(html_text)


def main():
    html_files = ["shakespeare.html", "war_and_peace.html", "us_cities_by_population.html"]
    patterns = ["the", "population", "Et tu, Brute?", "Tchaikovsky", "New York"]
    test_text = "<HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT </BODY></HTML>"
    test_pattern = "AT_THAT"

    while True:
        print("Please select an algorithm:")
        print("1. Brute Force")
        print("2. Boyer-Moore")
        print("3. Horspool")
        print("4. Test text and pattern")
        print("5. Exit")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            algorithm = BruteForce()
        elif choice == "2":
            algorithm = BoyerMoore()
        elif choice == "3":
            algorithm = Horspool()
        elif choice == "4":
            print("Running test on specific text and pattern...\n" + "-" * 40)
            algorithm = BruteForce()
            start_time = time.time()
            occurrences, comparisons = algorithm.search(test_text, test_pattern)
            end_time = time.time()
            running_time = end_time - start_time
            print(f"Pattern: {test_pattern}")
            print(f"Occurrences: {len(occurrences)}")
            print(f"Comparisons: {comparisons}")
            print(f"Running time: {running_time} seconds")
            print("-" * 40)
            continue
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        for html_file in html_files:
            print(f"Processing {html_file}...\n" + "-" * 40)
            run_algorithm(algorithm, html_file, patterns)
            print("=" * 40)

if __name__ == "__main__":
    main()