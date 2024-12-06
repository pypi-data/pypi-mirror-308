"""A module for detecting sensitive words in text using different algorithms.

Available algorithms:
- DFA (Deterministic Finite Automaton)
- Aho-Corasick algorithm
- Regular expression
- String find

Example usage:

```python
from pysenseword import search

text = "This is a test text without a sensitive word."
results = search(text, method='dfa')
print(results)
```

Output:

```
{'find': True, 'words': {('sensitive', 29)}}
```

The `search` function takes three arguments:
- `text`: the text to search for sensitive words
- `method`: the algorithm to use for detecting sensitive words. Available options are:
  - `dfa`: DFA algorithm
  - `ac`: Aho-Corasick algorithm
  - `re`: Regular expression
  - `str`: String find
"""
import sys
import os


sys.path.append(os.path.dirname(__file__))


class DFA:
    def __init__(self, keywords):
        self.trie = {}
        self.build_trie(keywords)
        self.keywords = keywords

    def build_trie(self, keywords):
        for keyword in keywords:
            current = self.trie
            for char in keyword:
                if char not in current:
                    current[char] = {}
                current = current[char]
            current['#'] = True

    def sensitive_word(self, text):
        text = text.lower()
        for i in range(len(text)):
            current = self.trie
            for j in range(i, len(text)):
                char = text[j]
                if char in current:
                    current = current[char]
                    if '#' in current:
                        return {'find':True,'word':text[i:j+1],'dict':{'line':self.keywords.index(text[i:j+1])+1,'index':i+1}}
                else:
                    break
        return {'find':False,'word':'','dict':{'line':0,'index':0}}


def load_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


# Example usage
# THIS IS JUST FOR TESTING PURPOSES
# READ THE DOCUMENATION FOR USAGE
# if __name__ == "__main__":
#     keywords = load_keywords('default_dict.py')
#     dfa_detector = DFA(keywords)

#     text = "This is a test text without a sensitive word."
#     results = dfa_detector.sensitive_word(text)
#     print(results)


class TrieNode:
    def __init__(self):
        self.children = {}
        self.output = []
        self.fail = None

class AhoCorasick:
    def __init__(self, keywords):
        self.root = TrieNode()
        self.build_trie(keywords)
        self.build_failure()

    def build_trie(self, keywords):
        for keyword in keywords:
            current = self.root
            for char in keyword:
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            current.output.append(keyword)

    def build_failure(self):
        from collections import deque

        queue = deque()
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()
            for char, next_node in current.children.items():
                queue.append(next_node)
                fail_state = current.fail
                while fail_state is not None and char not in fail_state.children:
                    fail_state = fail_state.fail
                next_node.fail = fail_state.children[char] if fail_state else self.root
                if next_node.fail and next_node.fail.output:
                    next_node.output.extend(next_node.fail.output)

    def search(self, text):
        current = self.root
        text = text.lower()
        results = set()
        for i, char in enumerate(text):
            while current is not None and char not in current.children:
                current = current.fail
            if current is None:
                current = self.root
                continue
            current = current.children[char]
            if current.output:
                for keyword in current.output:
                    results.add((keyword, i - len(keyword) + 1))

        return {'find': True if results else False, 'words': results}


# Example usage
# THIS IS JUST FOR TESTING PURPOSES
# READ THE DOCUMENATION FOR USAGE
# if __name__ == "__main__":
#     keywords = load_keywords('default_dict.py')
#     ac = AhoCorasick(keywords)

#     text = "This is a test text without a sensitive word."
#     results = ac.search(text.lower())
#     print(results)
import re

class RegexSensitiveWord:
    def __init__(self, keywords):
        self.keywords = keywords
        self.pattern = self.build_pattern(keywords)

    def build_pattern(self, keywords):
        escaped_keywords = [re.escape(keyword) for keyword in keywords]
        return re.compile(r'\b(' + '|'.join(escaped_keywords) + r')\b', re.IGNORECASE)

    def search(self, text):
        matches = self.pattern.finditer(text)
        results = set()
        for match in matches:
            results.add((match.group(), match.start()))

        return {'find': True if results else False, 'words': results}


# Example usage
# THIS IS JUST FOR TESTING PURPOSES
# READ THE DOCUMENATION FOR USAGE
# if __name__ == "__main__":
#     keywords = load_keywords('default_dict.py')
#     regex_detector = RegexSensitiveWord(keywords)

#     text = "This is a test text without a sensitive word."
#     results = regex_detector.search(text)
#     print(results)

class StringFindSensitiveWord:
    def __init__(self, keywords):
        self.keywords = keywords

    def search(self, text):
        text = text.lower()
        results = set()

        for keyword in self.keywords:
            start = 0
            while True:
                start = text.find(keyword.lower(), start)
                if start == -1:
                    break
                results.add((keyword, start))
                start += 1

        return {'find': True if results else False, 'words': results}


# Example usage
# THIS IS JUST FOR TESTING PURPOSES
# READ THE DOCUMENATION FOR USAGE
# if __name__ == "__main__":
#     keywords = load_keywords('default_dict.py')
#     string_find_detector = StringFindSensitiveWord(keywords)

#     text = "This is a test text without a sensitive word."
#     results = string_find_detector.search(text)
#     print(results)


class NoMethodError(Exception):
    pass


class NoDictionaryError(Exception):
    pass


def search(text,method='dfa',dictionary='default'):
    """search(text,method='dfa',dictionary='default')

    A function to search for sensitive words in text using different algorithms.
       
    Args:
        text (str): The text to search for sensitive words.
        method (str, optional): The algorithm to use for detecting sensitive words. Available options are:
            - 'dfa': DFA algorithm
            - 'ac': Aho-Corasick algorithm
            - 're': Regular expression
            - 'str': String find
        dictionary (list, optional): The path to the dictionary file. Defaults to 'default_dict.py' in the same directory as the module.

    Returns:
        A dictionary with two keys: 'find' and 'words'. 'find' should be a boolean value indicating whether any sensitive words were found, and 'words' should be a set of tuples containing the sensitive words and their starting indices.
    """
    if dictionary == 'default':
        dictionary = load_keywords(os.path.dirname(__file__)+'\\default_dict.py')
    if not dictionary:
        raise NoDictionaryError('No dictionary found')
    
    keywords=dictionary
    mathod=method.lower()

    if method == 'dfa':
        dfa_detector = DFA(keywords)
        results = dfa_detector.sensitive_word(text)
    elif method == 'ac':
        ac_detector = AhoCorasick(keywords)
        results = ac_detector.search(text)
    elif method in   ['re','regex','regexp','regular expression','pattern']:
        re_detector = RegexSensitiveWord(keywords)
        results = re_detector.search(text)
    elif mathod in ['str','string','text','string search','search string','search text','search', 'word search']:
        str_detector = StringFindSensitiveWord(keywords)
        results = str_detector.search(text)
    else:
        raise NoMethodError('No such method: %s' % method)
    return results


def search_advanced(text,method='dfa',dictionary='default',method_function=None, run_before=None, run_after=None):
    """search_advanced(text,method='dfa',dictionary='default',method_function=None, run_before=None, run_after=None)

    A function to search for sensitive words in text using different algorithms.
       
    Args:
        text (str): The text to search for sensitive words.
        method (str, optional): The algorithm to use for detecting sensitive words. Available options are:
            - 'dfa': DFA algorithm
            - 'ac': Aho-Corasick algorithm
            - 're': Regular expression
            - 'str': String find
        dictionary list, optional): The path to the dictionary file. Defaults to 'default_dict.py' in the same directory as the module.
        method_function (str, optional): A function that takes two arguments: text and keywords. The function should return a dictionary with two keys: 'find' and 'words'. 'find' should be a boolean value indicating whether any sensitive words were found, and 'words' should be a set of tuples containing the sensitive words and their starting indices. If this argument is provided, the method argument is ignored.
        run_before (str, optional): A string of Python code to execute before running the search algorithm.
        run_after (str, optional): A string of Python code to execute after running the search algorithm.

    Returns:
        A dictionary with two keys: 'find' and 'words'. 'find' should be a boolean value indicating whether any sensitive words were found, and 'words' should be a set of tuples containing the sensitive words and their starting indices.
    """
    if run_before:
        exec(run_before)
    
    if dictionary == 'default':
        dictionary = load_keywords(os.path.dirname(__file__)+'\\default_dict.py')

    keywords=dictionary
    mathod=method.lower()

    if not method_function:
        if method == 'dfa':
            dfa_detector = DFA(keywords)
            results = dfa_detector.sensitive_word(text)
        elif method == 'ac':
            ac_detector = AhoCorasick(keywords)
            results = ac_detector.search(text)
        elif method in   ['re','regex','regexp','regular expression','pattern']:
            re_detector = RegexSensitiveWord(keywords)
            results = re_detector.search(text)
        elif mathod in ['str','string','text','string search','search string','search text','search', 'word search']:
            str_detector = StringFindSensitiveWord(keywords)
            results = str_detector.search(text)
        else:
            raise NoMethodError('No such method: %s' % method)
        return results
    else:
        results = method_function(text,keywords)
    
    if run_after:
        exec(run_after)
    
    return results
