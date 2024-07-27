import os
import random


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
            # loop lines
            for line in content.split("\n"):
                if '*target:*' in line:
                    if len(line.split(":")) > 1:
                        vocab['target'] = line.split(":")[1].replace("*", "").strip()
                        print(vocab['target'])


if __name__ == "__main__":
    main()
