import os
from datetime import datetime
import datetime as dt
from pathlib import Path
import random

def main():
    current_directory = Path.cwd()
    print("Current Dir: ", current_directory)

    total_day = int(input("Enter total number of days: "))
    commit_frequency = int(input("Enter commit frequency (commits per day): "))
    repo_link = input("Enter repo link: ")
    off_weekends = str(input("Should I skip weekends? (Y/N): ")).lower() == "y"
    add_empty_days = str(input("Should I add empty days? (Y/N): ")).lower() == "y"

    emptyDays = 0
    if add_empty_days:
        emptyDays = int(input("Enter max empty days frequency (e.g., 5): "))

    tl = total_day  # Total days to process
    ctr = 1
    now = datetime.now()
    
    f = open(f"{current_directory}/gitgen.txt", "w")
    os.system("git config user.name")
    os.system("git config user.email")
    os.system("git init")

    pointer = 0
    skip_days_left = 0  # Track how many consecutive days to skip

    while tl > 0:
        current_date = now + dt.timedelta(days=-pointer)

        # Handle skipping weekends if the option is enabled
        if off_weekends and current_date.weekday() in (5, 6):  # 5 = Saturday, 6 = Sunday
            print(f"Skipping weekend: {current_date.strftime('%Y-%m-%d')}")
            pointer += 1
            continue

        # Randomly decide if we should skip days
        if add_empty_days and skip_days_left == 0 and random.random() < 0.2:  # 20% chance to skip
            # Randomly decide how many days to skip (1 to emptyDays)
            skip_days_left = random.randint(1, emptyDays)
            print(f"Randomly skipping {skip_days_left} days.")
        
        # Handle the current skip period
        if skip_days_left > 0:
            print(f"Skipping day: {current_date.strftime('%Y-%m-%d')}")
            pointer += 1
            tl -= 1
            skip_days_left -= 1
            continue

        # Determine the number of commits for the current day
        ct = random.randint(0 if emptyDays == 0 else 1, commit_frequency)
        while ct > 0:
            with open("gitgen.txt", "a+") as f:
                l_date = now + dt.timedelta(days=-pointer)
                formatdate = l_date.strftime("%Y-%m-%d")
                f.write(f"gitgen commit {ctr}: {formatdate}\n")
            
            os.system("git add .")
            os.system(f"git commit --date=\"{formatdate} 12:15:10\" -m \"gitgen commit {ctr}\"")
            print(f"gitgen commit {ctr}: {formatdate}")
            
            ct -= 1
            ctr += 1

        pointer += 1
        tl -= 1

    os.system(f"git remote add origin {repo_link}")
    os.system("git branch -M main")
    os.system("git push -u origin main -f")


if __name__ == "__main__":
    main()
