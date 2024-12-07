## Installation


### Installtion via Pip
```bash
pip install gitgen
```

If above method doesn't work via pip. Then install this via brew:

### Installation via Homebrew

To install `gitgen` using Homebrew, follow the steps below:

Step 1: Tap the Repository  
First, you need to tap the repository to make the `gitgen` formula available via Homebrew:

```
brew tap mubashardev/gitgen
```

Step 2: Install GitGen  
Once the repository is tapped, you can install `gitgen` with:

```
brew install gitgen
```


## Usage Guide for `gitgen`

### Prerequisites

1. **Python 3**:
   Ensure Python 3 is installed on your machine. You can verify the installation by running the following command:

   ```bash
   python --version
   ```

2. **Git**:
   Ensure Git is installed and configured on your machine. You can verify this by running:

   ```bash
   git --version
   ```

3. **GitHub Configuration**:
   Make sure your GitHub account is already linked to Git on your local machine. To check if your Git is configured with your GitHub credentials, run the following commands:

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your-email@example.com"
   ```

   These should return your GitHub username and email. If not configured, run the above commands with your actual name and GitHub email.

### Setup Instructions

#### Step 1: Create an Empty GitHub Repository

1. Go to your [GitHub profile](https://github.com) and create a new repository. 
2. You can set it to either public or private. However, **private** is recommended for personal testing.
3. **Do not initialize** the repository with a README, `.gitignore`, or license.

#### Step 2: Create a Local Directory

1. Create an empty directory on your local machine where you want to run `gitgen`. You can name the folder anything you like. For example:

   ```bash
   mkdir my-new-project
   cd my-new-project
   ```

2. Open a command prompt (Windows) or terminal (Mac/Linux) in that directory.

#### Step 3: Run `gitgen`

1. With the terminal or command prompt open in your project directory, execute the `gitgen` command:

   ```bash
   gitgen
   ```

2. The CLI will ask you for the following information:
   - **Total number of days**: The number of days over which you want commits to be spread.
   - **Commit frequency (commits per day)**: The number of commits you want per day.
   - **Repository link**: Paste the URL of the **empty GitHub repository** you just created.

3. Example of inputs:

   ```
   Enter total number of days: 5
   Enter commit frequency (commits per day): 3
   Enter repo link: https://github.com/yourusername/my-new-repo
   ```

4. The script will then:
   - Initialize the Git repository.
   - Automatically create and commit changes.
   - Push the commits to your GitHub repository over the number of days and commit frequency you've specified.

#### Step 4: Watch the Magic Happen

After `gitgen` completes the task, it will push the commits to your GitHub repository. GitHub might take a few minutes to index and show the contributions on your profile.

You can check the status of your repository by visiting the GitHub repository link you provided earlier. You'll see multiple commits as per the inputs you gave.

### Note:
If the changes or commits do not immediately reflect on your GitHub profile, give it a few minutes as GitHub may take some time to index the changes.