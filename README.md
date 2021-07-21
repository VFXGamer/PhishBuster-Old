![PhishBuster](https://user-images.githubusercontent.com/62838631/125227704-042d3780-e2f1-11eb-8f09-90ecd521f617.png)
<div align='center'>
<a href="https://www.codefactor.io/repository/github/vfxgamer/phishbuster"><img src="https://www.codefactor.io/repository/github/vfxgamer/phishbuster/badge" alt="CodeFactor" height="25"/></a>
<img src="https://img.shields.io/github/languages/code-size/VFXGamer/PhishBuster?style=for-the-badge" alt="GitHub code size in bytes" height="25"/></a>
<img src="https://img.shields.io/github/contributors/VFXGamer/PhishBuster?style=for-the-badge" alt="GitHub contributors" height="25"/></a>
<a href="https://deepsource.io/gh/VFXGamer/PhishBuster/?ref=repository-badge"><img src="https://deepsource.io/gh/VFXGamer/PhishBuster.svg/?label=active+issues&show_trend=true" alt="DeepSource" height="25"/></a>
</div>

## Sites:
For more details visit our [Blog](http://blog.cybervfx.tech/2021/06/phishbuster.html).<br>
Link to [PhishBuster](https://phishbuster-web.herokuapp.com/).

## How to use 😀:

1. You just have to paste the url in the **enter the url** section and **select the site** it resembles or it is supposed to be and click on **START SCAN** and it will let you know it is a phishing site or not.

![home](https://user-images.githubusercontent.com/62838631/126097957-b0fce4a7-2ece-4275-b80f-2805ec23f41c.jpg)

2. You can manually add phishing site in <a href="https://phishbuster-web.herokuapp.com/reports">reports</a>, click on add button to manually add phishing site.

![manualadd](https://user-images.githubusercontent.com/62838631/125229831-2fb22100-e2f5-11eb-90e1-e33130a89c28.jpg)

3. You can go to **CONTRIBUTE** section and click on **reports** to see the list of all the phishing urls saved from the scans and manual add.

![contribute](https://user-images.githubusercontent.com/62838631/120368102-4b59fd00-c32f-11eb-978f-8dbffde01b61.png)

4. Report the phishing sites by clicking on the **report** button.

![reports](https://user-images.githubusercontent.com/62838631/125227856-45bde280-e2f1-11eb-9cb2-a7770964842e.jpg)

### PhishBuster API
Send a **GET** request to [PhishBuster Site](https://phishbuster-web.herokuapp.com/api/) and add *suspected link* followed by **+** and add the *site it is trying to refer to*.<br>
Eg. https://phishbuster-web.herokuapp.com/api/suspected+refering+True/False <br>

**NOTE: To use API use** `call_api.py` **for proper functioning.**

#### Steps:
1. Set **inurl** to the input url and **seurl** to original domain.
2. Run `python call_api.py` to use the PhishBuster API.
3. You will receive a *json* output with 4 fields *Input Url*, *Original Url*, *Phishing Site* (boolean output) and *Data Saved* for confirming the input data was saved or not.

### Aim of the project is to reduce phishing victims. 😇