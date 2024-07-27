import os
import random
import re
from datetime import datetime
import uuid

OBSIDIAN_LEARN_PATH_DATA = "/home/b/MEGA/Obsidian/Zettelkasten/FrequentWordsLearning/Data"
OBSIDIAN_LEARN_PATH_EXERCISES = "/home/b/MEGA/Obsidian/Zettelkasten/FrequentWordsLearning/Exercises"

NUMBER_OF_DESIRED_EXERCISES = 50

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
                # drawing
                if '*drawing:*' in line:
                    print("drawing property exists")
                    drawing = get_sub_items_from_following_lines(lines, index+1)
                    if drawing:
                        vocab['drawing'] = drawing              
                # images
                if '*images*:' in line:
                    print("image property exists")
                    images = get_sub_items_from_following_lines(lines, index+1)
                    if images:
                        vocab['images'] = images


                
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
    nr_of_undone_exercises = 0
    # count how many files in exercises that are "todo" and not "todo-done"
    for f in os.listdir(OBSIDIAN_LEARN_PATH_EXERCISES):
        with open(os.path.join(OBSIDIAN_LEARN_PATH_EXERCISES, f), 'r') as file:
            content = file.read()
            if "q-type: todo" in content:
                if not "q-type: todo-done" in content:
                    nr_of_undone_exercises += 1

    # fill up with exercises
    nr_of_exercises_to_add = max(0, NUMBER_OF_DESIRED_EXERCISES - nr_of_undone_exercises)
    keys = list(exercises.keys())
    for i in range(nr_of_exercises_to_add):
        # pick a random key, use it, then remove from keys list
        # if list empty, break
        if not keys:
            break
        key = random.choice(keys)
        keys.remove(key)
        with open(os.path.join(OBSIDIAN_LEARN_PATH_EXERCISES, key + ".md"), 'w') as file:
            file.write(exercises[key])



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
    exercises.update(generate_exercises_sentence_prompt_double(vocabs))
    exercises.update(generate_exercises_image_to_target(vocabs))
    exercises.update(generate_native_to_target(vocabs))
    exercises.update(generate_target_to_native(vocabs))

    return exercises

def generate_exercises_sentence_prompt_double(vocabs):
    # 10 times
    exercises = {}
    for i in range(NUMBER_OF_DESIRED_EXERCISES):
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

def generate_exercises_image_to_target(vocabs):
    vocabs_with_images = [v for v in vocabs if 'images' in v]
    exercises = {}
    for v in vocabs_with_images:
        for img in v['images']:
            # use template_image_to_target
            with open("assets/template_image_to_target.md", 'r') as file:
                template = file.read()
            template = template.replace("$DATE", datetime.now().strftime("%d.%m.%Y"))
            template = template.replace("$TARGET", v['target'])
            template = template.replace("$FILE", v['name'])
            template = template.replace("$IMAGE", img)
            exercises[f'Image Exercise {uuid.uuid4()}'] = template
    return exercises

def generate_native_to_target(vocabs):
    exercises = {}
    for v in vocabs:
        # use template_native_to_target
        with open("assets/template_native_to_target.md", 'r') as file:
            template = file.read()
        template = template.replace("$DATE", datetime.now().strftime("%d.%m.%Y"))
        template = template.replace("$TARGET", v['target'])
        template = template.replace("$NATIVE", v['native'])
        template = template.replace("$FILE", v['name'])
        exercises[f'Native to Target {v["native"]}'] = template
    return exercises

def generate_target_to_native(vocabs):
    exercises = {}
    for v in vocabs:
        # use template_target_to_native
        with open("assets/template_target_to_native.md", 'r') as file:
            template = file.read()
        template = template.replace("$DATE", datetime.now().strftime("%d.%m.%Y"))
        template = template.replace("$TARGET", v['target'])
        template = template.replace("$NATIVE", v['native'])
        template = template.replace("$FILE", v['name'])
        exercises[f'Target to Native {v["target"]}'] = template
    return exercises

if __name__ == "__main__":
    main()
