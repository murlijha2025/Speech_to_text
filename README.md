Speech to Text with IBM Watson
Converts a recorded audio file to text using IBM Watson Speech to Text. It joins all the transcribed segments into clean sentences, saves the result to a text file, and prints the average confidence score.
Setup
You need Python 3.9+ and a free IBM Cloud account.
Create a Speech to Text service on IBM Cloud.
Copy the API key and URL from the service's credentials page.
Install and set your credentials:
```bash
git clone https://github.com/murlijha2025/live-Speech-and-Recorded-Sound-to-Text.git
cd live-Speech-and-Recorded-Sound-to-Text
pip install -r requirements.txt
```
Windows (PowerShell):
```powershell
$env:IBM_STT_APIKEY = "your-api-key"
$env:IBM_STT_URL = "your-service-url"
```
Mac/Linux:
```bash
export IBM_STT_APIKEY="your-api-key"
export IBM_STT_URL="your-service-url"
```
Never paste your key into the code or commit it to GitHub.
Usage
```bash
# basic
python speech_to_text.py speech.mp3

# different model and output file
python speech_to_text.py speech.wav -m en-AU_Multimedia -o transcript.txt
```
Option	What it does
`audio`	Path to the audio file (mp3, wav, flac, ogg, webm)
`-m`, `--model`	Watson model name (default: `en-US_Multimedia`)
`-o`, `--output`	Where to save the transcript (default: `output.txt`)
Models
Use a `Multimedia` model for normal audio (16 kHz or higher) and a `Telephony` model for phone-quality audio (8 kHz). Examples: `en-US_Multimedia`, `en-AU_Multimedia`, `en-US_Telephony`. See IBM's model list for other languages.
The old `Narrowband` and `Broadband` models were removed by IBM in 2023, so they won't work.
Limitations
It works on recorded audio files only. There's no live microphone input yet.
Accuracy depends on audio quality and accent. Check the confidence score.
IBM Cloud plans and free-tier limits change, so check what your account includes.
Dependencies
`ibm-watson`
