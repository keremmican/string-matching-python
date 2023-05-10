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
    def search(text, pattern):
        # TODO: Implement Boyer-Moore algorithm
        pass


class Horspool:
    @staticmethod
    def search(text, pattern):
        # TODO: Implement Horspool's algorithm
        pass


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