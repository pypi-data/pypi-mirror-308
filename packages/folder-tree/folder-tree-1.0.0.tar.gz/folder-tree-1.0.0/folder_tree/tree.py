import argparse
import os 

def display_tree(path, prefix=""):
    if not(os.path.exists(path)):
        print(f"Error:Path '{path}' does not exists")
        return 
    entries = os.listdir(path)
    entries.sort()
    
    for index,entry in enumerate(entries):
        entry_path = os.path.join(path,entry)
        is_last = len(entries)==index
        connector = "└──" if is_last else "├──"
        print(f"{prefix}{connector} {entry}")

        if os.path.isdir(entry_path):
            next_prefix= f"{prefix}    " if is_last else f"{prefix}│   "
            display_tree(entry_path, next_prefix)

def main():
    parser = argparse.ArgumentParser(description="Display folder structure in a tree format.")
    parser.add_argument("path", nargs="?", default='.', help="The path to the folder (default is current directory).")
    args = parser.parse_args()
    
    print(os.path.basename(os.path.abspath(args.path)))
    display_tree(args.path, prefix="")
if __name__=="__main__":
    main()