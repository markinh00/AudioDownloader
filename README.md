
# VideoDownloader
A small server to download the audio of youtube videos


## Instalation

if you want to clone and run your own version of the project use the following comands for windows:

### Cloning the repository
```bash
  git clone https://github.com/markinh00/VideoDownloader
```
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

now you need to create a new file qith the name ".env" and add the folowing variables:
```bash
  API_KEY="YOUR_RANDOM_API_KEY"
  AUDIO_DIR="FOLDER_NAME"
```

### Running the program
```bash
  python -m uvicorn main:app --reload
```