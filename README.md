# PhishBuster 💻
![GitHub last commit](https://img.shields.io/github/last-commit/VFXGamer/PhishBuster?style=for-the-badge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/VFXGamer/PhishBuster?style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/VFXGamer/PhishBuster?style=for-the-badge)<br>
[![DeepSource](https://deepsource.io/gh/VFXGamer/PhishBuster.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/VFXGamer/PhishBuster/?ref=repository-badge)
## How to use 😀:

1. You just have to paste the url in the **enter the url** section and **select the site** it resembles or it is supposed to be and click on **START SCAN** and it will let you know it is a phishing site or not.

![image](https://user-images.githubusercontent.com/62838631/120367512-91629100-c32e-11eb-9a91-8125c31ba186.png)


2. You can go to **CONTRIBUTE** section and click on **reports** to see the list of all the phishing urls saved from the scans and report them to their respective domain name registrar.

![image](https://user-images.githubusercontent.com/62838631/120368102-4b59fd00-c32f-11eb-978f-8dbffde01b61.png)

### API Service
Send a **GET** request to [PhishBuster Site](https://phishbuster-web.herokuapp.com/api/) and add *suspected link* followed by **+** and add the *site it is trying to refer to*.<br>
Eg. https://phishbuster-web.herokuapp.com/api/suspected+refering <br>
**NOTE: To use API use** `call_api.py` **for proper functioning.**

#### Steps:
1. Set **inurl** to the input url and **seurl** to orginal domain.
2. Run `python call_api.py` to use the PhishBuster API.
3. You will recieve a *json* output with 3 fields *Input Url*, *Orginal Url*, *Phishing Site* (boolean output).

### Installation Steps:
1. Run `git clone https://github.com/VFXGamer/PhishBuster.git` in shell.
2. Run `python -m pip install -r requirements.txt` to install all the required python modules.
3. Run `python app.py` to launch the app.
4. Done

### Aim of the project is to reduce phishing victims. 😇


