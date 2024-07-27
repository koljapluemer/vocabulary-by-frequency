import os
import random
import re
from datetime import datetime
import uuid

OBSIDIAN_LEARN_PATH_DATA = "/home/b/MEGA/Obsidian/Zettelkasten/FrequentWordsLearning/Data"
OBSIDIAN_LEARN_PATH_EXERCISES = "/home/b/MEGA/Obsidian/Zettelkasten/FrequentWordsLearning/Exercises"

NUMBER_OF_DESIRED_EXERCISES = 100

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

                    drawing = get_sub_items_from_following_lines(lines, index+1)
                    if drawing:
                        vocab['drawing'] = drawing              
                # images
                if '*images*:' in line:

                    images = get_sub_items_from_following_lines(lines, index+1)
                    if images:
                        vocab['images'] = images


                
            if valid_vocab_file:
                vocabs.append(vocab)


    # generate exercises
    exercises = generate_exercises(vocabs)
    # save
    save_exercises(exercises)

def save_exercises(exercise_collections):
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
    used_keys = []
    # while exercises missing, pick a random exercise_collection, pick a random element from it, and then remove that from the list
    while nr_of_exercises_to_add > 0:
        exercise_collection = random.choice(exercise_collections)
        keys_as_list = list(exercise_collection.keys())
        if len(keys_as_list) == 0:
            continue
        random_key = random.choice(keys_as_list)
        if random_key in used_keys:
            continue
        used_keys.append(random_key)
        with open(os.path.join(OBSIDIAN_LEARN_PATH_EXERCISES, random_key + ".md"), 'w') as file:
            file.write(exercise_collection[random_key])
        nr_of_exercises_to_add -= 1



def get_sub_items_from_following_lines(lines, start_index):
    items = []
    for i in range(start_index, len(lines)):
        if lines[i].startswith("-"):

            break
        # use regex to kill everything like "- a)" or "-" or "- b)"
        clean_line = re.sub(r'-\s[a-z]\)', '', lines[i])
        clean_line = clean_line.replace("- ", "").strip()
        if clean_line:
            items.append(clean_line)
    return items

def generate_exercises(vocabs):
    exercise_collections = [
        generate_exercises_sentence_prompt_double(vocabs),
        generate_exercises_sentence_prompt_single(vocabs),
        generate_exercises_image_to_target(vocabs),
        generate_native_to_target(vocabs),
        generate_target_to_native(vocabs),
        generate_pick_correct_image(vocabs),
        generate_exercises_with_prompt(vocabs),
        generate_exercises_target_pronounce(vocabs)
    ]

    return exercise_collections

def generate_exercises_sentence_prompt_double(vocabs):
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

def generate_exercises_sentence_prompt_single(vocabs):
    exercises = {}
    for i in range(NUMBER_OF_DESIRED_EXERCISES):
        # pick 1 random vocab, and make a card prompting to make a sentence with it
        # use template_sentence_single
        with open("assets/template_sentence_single.md", 'r') as file:
            template = file.read()
        # replace $DATE, $WORD_FILE, $WORD_TARGET
        word = random.choice(vocabs)
        template = template.replace("$DATE", datetime.now().strftime("%d.%m.%Y"))
        template = template.replace("$FILE", word['name'])
        template = template.replace("$TARGET", word['target'])
        exercises[f'Sentence Prompt {word["target"]}'] = template
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

def generate_exercises_target_pronounce(vocab):
    # pronunciation field required, replace target and $file
    vocabs_with_pronunciation = [v for v in vocab if 'pronunciation' in v]
    exercises = {}
    for v in vocabs_with_pronunciation:
        # use template_target_pronounce
        with open("assets/template_target_pronounce.md", 'r') as file:
            template = file.read()
        template = template.replace("$DATE", datetime.now().strftime("%d.%m.%Y"))
        template = template.replace("$TARGET", v['target'])
        template = template.replace("$FILE", v['name'])
        exercises[f'Pronounce {v["target"]}'] = template

    return exercises

def generate_exercises_with_prompt(vocab):
    prompts = {
        "$TARGET — Last Seen":  "When did you last see $TARGET?",
        "$TARGET — Opinion": "What do you think about $TARGET?",
        "$TARGET — Explain": "Explain $TARGET in Egyptian Arabic as best as you can:",
        "$TARGET — Nearest": "What is the $TARGET nearest to you:"
    }
    exercises = {}
    for _ in range(NUMBER_OF_DESIRED_EXERCISES):
        # pick a random vocab, and a random prompt
        # use template_prompt
        with open("assets/template_prompt.md", 'r') as file:
            template = file.read()
        # replace $DATE, $TARGET, $FILE, $PROMPT
        word = random.choice(vocab)
        prompt_key = random.choice(list(prompts.keys()))
        prompt = prompts[prompt_key]
        prompt = prompt.replace("$TARGET", f'[[{word["name"]}|{word["target"]}]]')
        template = template.replace("$DATE", datetime.now().strftime("%d.%m.%Y"))
        template = template.replace("$PROMPT", prompt)
        prompt_key = prompt_key.replace("$TARGET", word["target"])
        exercises[prompt_key] = template
    return exercises


def generate_pick_correct_image(vocabs):
    vocabs_with_images = [v for v in vocabs if 'images' in v]
    exercises = {}
    for v in vocabs_with_images:
        for img in v['images']:
            # pick 3 random images from *other* vocab with images
            images = [img]
            for _ in range(3):
                other_v = random.choice(vocabs_with_images)
                if other_v == v:
                    continue
                other_img = random.choice(other_v['images'])
                if other_img in images:
                    continue
                images.append(other_img)
            # if list is at least 2 img
            if len(images) > 1:
                # shuffle
                random.shuffle(images)
                # use template_pick_correct_image
                with open("assets/template_pick_correct_image.md", 'r') as file:
                    template = file.read()
                template = template.replace("$DATE", datetime.now().strftime("%d.%m.%Y"))
                template = template.replace("$TARGET", v['target'])
                template = template.replace("$FILE", v['name'])

                
                # template = template.replace("$IMAGE1", images[0].replace("]]", "|200]]|"))
                # template = template.replace("$IMAGE2", images[1].replace("]]", "|200]]"))
                # template = template.replace("$IMAGE3", images[2].replace("]]", "|200]]"))
                # template = template.replace("$IMAGE4", images[3].replace("]]", "|200]]"))
                for j in range(4):
                    # first check if list goes so far, if not, just delete the placeholder
                    if j >= len(images):
                        template = template.replace(f"$IMAGE{j+1}", "")
                    else:
                        img = images[j]
                        template = template.replace(f"$IMAGE{j+1}", images[j].replace("]]", "|200]]|"))
                exercises[f'Which image is {v["target"]}﹖'] = template
    return exercises
                

if __name__ == "__main__":
    main()
