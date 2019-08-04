import argparse
import os
import pandas as pd
import pyperclip
import time

from tqdm import tqdm
from termcolor import cprint


def get_questions_df(file_name):
    """Grabs all questions in a single TSV file"""
    df = pd.read_csv(file_name, sep="\t")
    return df


def get_all_questions(directory_path):
    """Grabs all questions from a directory path and creates a big dataframe"""
    dfs = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".tsv"):
            path_to_file = f"{directory_path}/{filename}"
            # print(f"Adding {path_to_file}")
            dfs.append(get_questions_df(path_to_file))

    df = pd.concat(dfs, sort=False)
    print(f"Loading {df.shape[0]} questions from {len(dfs)} files.")
    return df


def parse_arguments():
    """Parses all command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("time_for_problem", help="Integer umber of seconds for the problem", type=int)
    return parser.parse_args()


def display_random_question(df):
    """Display a random question selected from the supplied dataframe"""
    new_df = df.sample(n=1)
    question = list(new_df["Question"])[0]
    title = list(new_df["Title"])[0]
    cprint("Title:", "green")
    print(f"{title}\n")
    cprint("Question:", "yellow")
    print(f"{question}\n")
    copy_to_clipboard(title, question)

    return new_df


def copy_to_clipboard(title, question):
    cprint("Your question has been copied to your internal clipboard, you can now paste it into an editor", "yellow")
    pyperclip.copy(f'"""\nTitle:\n\t{title}\nQuestion:\n\t{question}\n"""\n\n')


def display_timer():
    """Display a timer, that can be interrupted with CTRL + C"""
    cprint("You can press CTRL + C at any time to stop the timer", "blue")
    cprint("Elapsed Time", 'red')
    keep_running = True
    try:
        while keep_running:
            for counter in tqdm(range(args.time_for_problem)):
                time.sleep(1)

            # Sound an audible timer for when the time is up.
            for i in range(5):
                print("\007")
                time.sleep(0.25)

            keep_running = False
    except KeyboardInterrupt:
        print("\007")
        cprint(f"Processing keyboard interrupt.", "blue")

    if not keep_running:
        print(f"You ran out of time!")
    else:
        print(f"You finished with {args.time_for_problem - counter} seconds remaining.")


if __name__ == "__main__":
    """This script picks a random question and presents it to the user to solve in a limited amout of time"""
    args = parse_arguments()
    # Collect questions from data directory
    df = get_all_questions("./data")

    # Prompt user to start
    input(f"You will have {args.time_for_problem} seconds to answer the question, press ENTER to start")
    print("\007")

    new_df = display_random_question(df)
    display_timer()

    chapter = list(new_df["Major"])[0]
    question = list(new_df["Minor"])[0]
    print(f"\nThe program selected Chapter {chapter} Question {question}")




