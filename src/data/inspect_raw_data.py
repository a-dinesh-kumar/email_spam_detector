from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw dataset directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def count_emails(folder):
    """Count files inside a dataset folder."""
    
    files = [
        file
        for file in folder.iterdir()
        if file.is_file()
    ]

    return len(files)


def main():

    folders = {
        "easy_ham": RAW_DATA_DIR / "easy_ham",
        "hard_ham": RAW_DATA_DIR / "hard_ham",
        "spam": RAW_DATA_DIR / "spam"
    }

    print("\n===== SpamAssassin Dataset =====\n")

    for label, folder in folders.items():

        count = count_emails(folder)

        print(f"{label:<10} : {count} emails")


if __name__ == "__main__":
    main()