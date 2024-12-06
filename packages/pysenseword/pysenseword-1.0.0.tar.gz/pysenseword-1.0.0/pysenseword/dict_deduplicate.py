def remove_duplicates(input_file, output_file):
    unique_keywords = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            keyword = line.strip()
            if keyword:
                unique_keywords.add(keyword.lower())

    with open(output_file, 'w', encoding='utf-8') as f:
        for keyword in unique_keywords:
            f.write(keyword + '\n')

if __name__ == "__main__":
    input_file = 'dict.txt'
    output_file = 'deduplicated_dict.txt'

    remove_duplicates(input_file, output_file)
    print(f"Deduplicated keywords saved to {output_file}。")
