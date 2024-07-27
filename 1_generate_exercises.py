import os
import random
import re


OBSIDIAN_LEARN_PATH_DATA = "/home/b/MEGA/Obsidian/Zettelkasten/FrequentWordsLearning/Data"
OBSIDIAN_LEARN_PATH_EXERCISES = "/home/b/MEGA/Obsidian/Zettelkasten/FrequentWordsLearning/Exercises"


def main():
    # create paths if they don't exist
    if not os.path.exists(OBSIDIAN_LEARN_PATH_DATA):
        os.makedirs(OBSIDIAN_LEARN_PATH_DATA)
    if not os.path.exists(OBSIDIAN_LEARN_PATH_EXERCISES):
        os.makedirs(OBSIDIAN_LEARN_PATH_EXERCISES)

    # loop all md files in data and read them in
    md_files_in_path = [f for f in os.listdir(OBSIDIAN_LEARN_PATH_DATA) if f.endswith('.md')]
    vocabs = []
    for f in md_files_in_path:
        with open(os.path.join(OBSIDIAN_LEARN_PATH_DATA, f), 'r') as file:
            content = file.read()
            vocab = {}
            valid_vocab_file = False
            # loop lines
            lines = content.split("\n")
            for index, line in enumerate(lines):
                if '*target:*' in line:
                    if len(line.strip().split(":")) > 1:
                        target = line.split(":")[1].replace("*", "").strip()
                        if target:
                            # print(target)
                            vocab['target'] = target
                            valid_vocab_file = True
                # same process for "native"
                if '*native:*' in line:
                    if len(line.strip().split(":")) > 1:
                        source = line.split(":")[1].replace("*", "").strip()
                        if source:
                            print(source)
                            vocab['native'] = source
                # word_type
                if '*word_type:*' in line:
                    if len(line.strip().split(":")) > 1:
                        word_type = line.split(":")[1].replace("*", "").strip()
                        if word_type:
                            vocab['word_type'] = word_type
                # transliteration
                if '*transliteration:*' in line:
                    if len(line.strip().split(":")) > 1:
                        transliteration = line.split(":")[1].replace("*", "").strip()
                        if transliteration:
                            vocab['transliteration'] = transliteration
                # for the following one's, we're actually interested in the following lines
                # search for following lines, until it starts with - or doesn't exist
                # 1) "notes"
                if '*notes:*' in line:
                    notes = []
                    for i in range(index+1, len(lines)):
                        if lines[i].startswith("-"):
                            break
                        # use regex to kill everything like "- a)" or "-" or "- b)"
                        clean_line = re.sub(r'-\s[a-z]\)', '', lines[i])
                        clean_line = clean_line.replace("- ", "").strip()
                        if clean_line:
                            notes.append(clean_line)
                    vocab['notes'] = notes
                    print("notes:", notes)


                
            if not valid_vocab_file:
                # print(f"File {f} is not a valid vocab file")
                continue


if __name__ == "__main__":
    main()
