import os
import random
import re
from datetime import datetime

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
            vocab = {"name": f}
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
                    notes = get_sub_items_from_following_lines(lines, index+1)
                    if notes:
                        vocab['notes'] = notes
                # antonyms
                if '*antonyms:*' in line:
                    antonyms = get_sub_items_from_following_lines(lines, index+1)
                    if antonyms:
                        vocab['antonyms'] = antonyms
                # siblings
                if '*siblings:*' in line:
                    siblings = get_sub_items_from_following_lines(lines, index+1)
                    if siblings:
                        vocab['siblings'] = siblings
                # parents
                if '*parents:*' in line:
                    parents = get_sub_items_from_following_lines(lines, index+1)
                    if parents:
                        vocab['parents'] = parents
                # children
                if '*children:*' in line:
                    children = get_sub_items_from_following_lines(lines, index+1)
                    if children:
                        vocab['children'] = children
                # pronunciation
                if '*pronunciation:*' in line:
                    pronunciation = get_sub_items_from_following_lines(lines, index+1)
                    if pronunciation:
                        vocab['pronunciation'] = pronunciation
                # images
                if '*images*:' in line:
                    print("image property exists")
                    images = get_sub_items_from_following_lines(lines, index+1)
                    if images:
                        vocab['images'] = images
                # drawing
                if '*drawing:*' in line:
                    print("drawing property exists")
                    drawing = get_sub_items_from_following_lines(lines, index+1)
                    if drawing:
                        vocab['drawing'] = drawing

                
            if valid_vocab_file:
                vocabs.append(vocab)
                print(vocab)
            else:
                print(f"File {f} is not a valid vocab file")

    # generate exercises
    exercises = generate_exercises(vocabs)
    # save
    save_exercises(exercises)

def save_exercises(exercises):
    for name, content in exercises.items():
        with open(os.path.join(OBSIDIAN_LEARN_PATH_EXERCISES, name + ".md"), 'w') as file:
            file.write(content)


def get_sub_items_from_following_lines(lines, start_index):
    items = []
    for i in range(start_index, len(lines)):
        if lines[i].startswith("-"):
            print("breaking at", lines[i])
            break
        # use regex to kill everything like "- a)" or "-" or "- b)"
        clean_line = re.sub(r'-\s[a-z]\)', '', lines[i])
        clean_line = clean_line.replace("- ", "").strip()
        if clean_line:
            items.append(clean_line)
    return items

def generate_exercises(vocabs):
    exercises = {}
    sentence_exercises = generate_exercises_sentence_prompt_double(vocabs)
    exercises.update(sentence_exercises)

    return exercises

def generate_exercises_sentence_prompt_double(vocabs):
    # 10 times
    exercises = {}
    for i in range(10):
        # pick 2 random vocabs, and make a card prompting to make a sentence with them
        # use template_sentence_double
        with open("assets/template_sentence_double.md", 'r') as file:
            template = file.read()
        # replace $DATE, $WORD1_FILE, $WORD1_TARGET, $WORD2_FILE, $WORD2_TARGET
        word1 = random.choice(vocabs)
        word2 = random.choice(vocabs)
        if word1 == word2:
            continue
        template = template.replace("$DATE", datetime.now().strftime("%d.%m.%Y"))
        template = template.replace("$WORD1_FILE", word1['name'])
        template = template.replace("$WORD1_TARGET", word1['target'])
        template = template.replace("$WORD2_FILE", word2['name'])
        template = template.replace("$WORD2_TARGET", word2['target'])
        exercises[f'Sentence Prompt {word1["target"]} and {word2["target"]}'] = template
    return exercises


if __name__ == "__main__":
    main()
