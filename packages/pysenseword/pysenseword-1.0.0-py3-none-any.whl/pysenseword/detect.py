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
#     keywords = load_keywords('default_dict.txt')
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
#     keywords = load_keywords('default_dict.txt')
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
#     keywords = load_keywords('default_dict.txt')
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
#     keywords = load_keywords('default_dict.txt')
#     string_find_detector = StringFindSensitiveWord(keywords)

#     text = "This is a test text without a sensitive word."
#     results = string_find_detector.search(text)
#     print(results)
