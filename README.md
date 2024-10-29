
# AudioDownloader
A small server to download the audio of youtube videos


## Instalation

If you want to clone and run your own version of the project use the following the instructions for windows:

### Cloning the repository
Open the cmd in a desired folder and run the command bellow:
```bash
  git clone https://github.com/markinh00/VideoDownloader
```
Now open the project in the IDE of your choice (like vscode or pycharm) and run the below commands in the terminal:
### Creating a virtual environment
```bash
  python -m venv .venv
```
```bash
  ./venv/Scripts/activate.ps1
```
### Installing the requirements
```bash
  pip install -r requirements.txt
```

Now you need to create a new folder on the root of the project with the name ".env" and add the following variables to it:
```bash
  API_KEY="YOUR_RANDOM_API_KEY"
  AUDIO_DIR="/tmp/YOUR_ARBITRARY_FOLDER_NAME"
```

### Running the program
```bash
  python -m uvicorn main:app --reload
```
