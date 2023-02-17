import sys
from googleapiclient.discovery import build


# Global Variables
MAX_ITERATIONS = 10
ALPHA = 1
BETA = 0.75
GAMMA = 0.15
SEARCH_JSON_API_KEY = ""
SEARCH_ENGINE_ID = ""
TARGET_PRECISION = 0.0
QUERY = ""

def get_parameters():
    """
    Get parameters from the inputs, and store the value in global variables.
    """
    inputs = sys.argv
    global SEARCH_JSON_API_KEY, SEARCH_ENGINE_ID, TARGET_PRECISION, QUERY
    # If the input format or value is incorrect, print the error message
    if len(sys.argv) != 5:
        print("Correct format: main.py <google api key> <google engine id> <precision> <query>")
    elif float(sys.argv[3]) < 0 or float(sys.argv[3]) > 1:
        print("The range of <precision> is 0 - 1")
    else:
        SEARCH_JSON_API_KEY = inputs[1]
        SEARCH_ENGINE_ID = inputs[2]
        TARGET_PRECISION = float(inputs[3])
        QUERY = inputs[4]
        i = 5
        while i < len(inputs):
            QUERY += " " + inputs[i]
            i += 1
        # Print to console
        print("Search Key: " + SEARCH_JSON_API_KEY)
        print("Search Engine ID: " + SEARCH_ENGINE_ID)
        print("Target Precision: " + str(TARGET_PRECISION))
        print("QUERY: " + QUERY)


def google_search(**kwargs):
    """
        Get the result from Google Search Engine.
    """
    service = build("customsearch", "v1", developerKey=SEARCH_JSON_API_KEY)
    res = service.cse().list(q=QUERY, cx=SEARCH_ENGINE_ID, **kwargs).execute()
    result = res['items']
    return result


def collect_feedback():
    """
        Collect the feedback of the search results and store relevant and non-relevant results to two lists.
    """
    results = []
    relevant_list = []
    non_relevant_list = []
    num_total, num_relevant, num_non_relevant = 0, 0, 0
    search_results = google_search()
    for item in search_results:
        num_total += 1
        title = item['title']
        url = item['link']
        summary = item['snippet']
        item_data = {
            "title": title,
            "url": url,
            "summary": summary,
            "relevant": False
        }
        results.append(item_data)
    for idx in range(len(results)):
        item = results[idx]
        print("Result " + str(idx + 1))
        print("[")
        print(" URL: " + item['url'])
        print(" Title: " + item['title'])
        print(" Summary: " + item['summary'])
        print("]")

        feedback = input("Relevant(Y/N)? ")
        # Get the feedback from user.
        if feedback == 'Y' or feedback == 'y':
            num_relevant += 1
            relevant_list.append(title + summary)
            item['relevant'] = True
        else:
            num_non_relevant += 1
            non_relevant_list.append(title + summary)
    return num_total, num_relevant, num_non_relevant, relevant_list, non_relevant_list


def augment_query(relevant_docs, non_relevant_docs, query):
    """
    Augment the query with two new words using Rocchio algorithm.
    """


def main():
    # Get the value of the input parameters.
    get_parameters()
    curr_query = QUERY
    for i in range(MAX_ITERATIONS):
        print(f'This is iteration #{i + 1}')

        results = google_search(num=10)

        # The results returned are not enough
        if len(results) < 10:
            print('The number of results are less the 10')
            break

        # Collect the feedback from users.
        num_total, num_relevant, num_non_relevant, relevant_list, non_relevant_list = collect_feedback()

        if num_relevant == 0:
            print('Terminate: No result is relevant in the first iteration')
            break

        # Calculate the current precision
        curr_precision = num_relevant / num_total
        print(f'Current Query : {curr_query}')

        # check if desired precision is reached
        if curr_precision < TARGET_PRECISION:
            print(f'Current Precision : {curr_precision}')
            print(f'Still below the desired precision of {TARGET_PRECISION}')

            # augment current query by adding two words
            new_query, expand_word_1, expand_word_2 = augment_query(relevant_list, non_relevant_list, curr_query)
            print(f'Using these two words to augment the query: {expand_word_1} {expand_word_2}')
            curr_query = new_query
            print("Current query: " + curr_query)
        else:
            print(f'Current Precision : {curr_precision}')
            print("Reached the target precision.")
            break


if __name__ == '__main__':
    main()