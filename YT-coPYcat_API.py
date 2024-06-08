import googleapiclient.discovery
import itertools
import time
import os

# You need to set up a project in Google Developer Console and get your YouTube Data API key.
API_KEY = ""
max_results=0

# Define common letter replacements
LETTER_REPLACEMENTS = {
    'a': ['s', 'q', 'z', 'o'],
    'b': ['v', 'g', 'n'],
    'c': ['x', 'v', 'f'],
    'd': ['s', 'f', 'e'],
    'e': ['w', 'r', 'd', '3'],
    'f': ['d', 'g', 'r'],
    'g': ['f', 'h', 'b'],
    'h': ['g', 'j', 'y'],
    'i': ['u', 'o', 'k', 'e', '1'],
    'j': ['h', 'k', 'u'],
    'k': ['j', 'l', 'i'],
    'l': ['k', 'o', 'i', '1'],
    'm': ['n', 'j'],
    'n': ['b', 'm', 'j'],
    'o': ['i', 'p', 'l', 'a', 'u', '0'],
    'p': ['o', 'l'],
    'q': ['w', 'a'],
    'r': ['e', 't', 'f'],
    's': ['a', 'd', 'w'],
    't': ['r', 'y', 'g'],
    'u': ['y', 'i', 'j'],
    'v': ['c', 'b', 'g'],
    'w': ['q', 'e', 's'],
    'x': ['z', 'c', 's'],
    'y': ['t', 'u', 'h'],
    'z': ['a', 'x']
}

def generate_variants(name, max_typos=0):
    variants = set()
    # Generate all combinations of positions for the typos
    positions = list(range(len(name)))
    for num_typos in range(1, max_typos + 1):
        for typo_positions in itertools.combinations(positions, num_typos):
            variant = list(name)
            # Generate all combinations of replacements for the selected positions
            for replacements in itertools.product(*[LETTER_REPLACEMENTS.get(name[pos], [name[pos]]) for pos in typo_positions]):
                for pos, replacement in zip(typo_positions, replacements):
                    variant[pos] = replacement
                variants.add("".join(variant))
    return list(variants)

def search_youtube(query, api_key, cache):
    global max_results
    if query in cache:
        return cache[query]

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=query,
        type="channel"
    )

    try:
        response = request.execute()
        results = []
        for item in response['items']:
            channel = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channelId': item['id']['channelId']
            }
            results.append(channel)
        cache[query] = results
        return results
    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")
        time.sleep(5)
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
        return []

def main():
    global max_results
    print('\033[37m__   _______     \033[31m _____      ________   __        _   ')
    print('\033[37m\ \ / /_   _|    \033[31m/  __ \     | ___ \ \ / /       | |  ')
    print('\033[37m \ V /  | |______\033[31m| /  \/ ___ | |_/ /\ V /___ __ _| |_ ')
    print('\033[37m  \ /   | |______\033[31m| |    / _ \|  __/  \ // __/ _` | __|')
    print('\033[37m  | |   | |      \033[31m| \__/\ (_) | |     | | (_| (_| | |_ ')
    print('\033[37m  \_/   \_/      \033[31m \____/\___/\_|     \_/\___\__,_|\__|\033[37m')
    print('Created by Mio \nAtago66 on Github\n\nYoutube Data API Key can be obtained at \033[34mhttps://console.cloud.google.com/apis/dashboard \033[37m\nStandard API Quota is \033[31m10,000\033[37m Per Day')
    time.sleep(2)
    print('\n')
    API_KEY = input("Enter your YouTube Data API key:\033[32m ")
    input_name = input("\033[37mEnter the YouTube channel name:\033[36m ")
    try:
        max_results = int(input("\033[37mEnter the maximum number of results to return per typo:\033[35m "))
    except:
        print("\033[31mInvalid input. Defaulting to 0.")
        max_results = 0
    variants = generate_variants(input_name, max_typos=1)  # Limiting to one typo
    cache = {}  # Define the cache dictionary here
    all_results = []

    for variant in variants:
        print(f"\033[37mSearching for: {variant}")
        results = search_youtube(variant, API_KEY, cache)
        all_results.extend(results)
      
    unique_results = {result['channelId']: result for result in all_results}.values()

    print("\nFound Channels:")
    for result in unique_results:
        print(f"Title: {result['title']}")
        print(f"Description: {result['description']}")
        print(f"Channel ID: {result['channelId']}")
        print("----")

if __name__ == "__main__":
    main()