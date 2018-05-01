# Welcome to Social-Monomania!
This repository is a Senior Project currently under development. The following is the description of the project:

Gamecock Social Media Listening
The USC International Center for Event Research and Education housed in the College of Hospitality, Retail, and Sport Management would like to propose the development of a social media listening tool that will allow USC faculty to engage in research that tracks social media posts and visual content across multiple social media platforms.  Recent research has shown the top five social media platforms according to ebizmba.com (July 2017), are Facebook, YouTube, Instagram, Twitter, and Reddit, but social media research also can include mainstream news, blogs, forums, and forum replies.  By developing an easy to navigate user interface, faculty can undertake searches of social media posts which include specified keywords and phrases and exclude other specified keywords and phrases.   Once the social media searches are concluded, the software will display visually appealing screens for an easy graphical review of "Sentiment" analysis, Wordclouds, keyword and date line-charts and list all original responses for a more detailed review. Searches must be able to be restricted by date and geography (Geofencing).

This will be a web application.

## Requirements To Run
``certifi==2018.1.18
chardet==3.0.4
dj-database-url==0.4.2
Django==1.11.7
facebook-sdk
gunicorn
httplib2==0.10.3
idna==2.6
nltk==3.2.1
numpy==1.14.1
oauth2==1.9.0.post1
oauthlib==1.1.2
pandas==0.22.0
praw==5.4.0
prawcore==0.14.0
psycopg2==2.7.3.2
python-dateutil==2.6.1
pytz==2017.3
requests==2.18.4
requests-oauthlib==0.6.2
six==1.11.0
textblob==0.11.1
update-checker==0.16
urllib3==1.22
whitenoise==3.3.1
XlsxWriter==1.0.2``

**Note: This application directly restarts and updates after each commit, applying all changes. It uses the commands found in both this README and the URL below.**

*This app follows standard Heroku deployment procedures for python, which can be found here:*
https://devcenter.heroku.com/articles/getting-started-with-python#introduction

The command that Heroku's standard procfile uses (and that we use as well) to deploy is:

```web: gunicorn social_monomania.wsgi --log-file -```

## TESTING:

### Behavioral Testing
We are using Selenium to conduct our behavioral testing.  Selenium uses a Firefox addon/Chrome Plugin called Katalon Automation Recorder.  To use this addon:
1. Download the latest version of Firefox: https://www.mozilla.org/en-US/firefox/new/
2. Install the addon from: https://addons.mozilla.org/en-US/firefox/addon/katalon-automation-record/ *or* https://chrome.google.com/webstore/detail/katalon-recorder-selenium/ljdobmomdgdljniojadhoplhkpialdid?hl=en-US
3. Run the addon from the browser toolbar
4. Open the test suite from our GitHub Repository (i.e. open the folder Behavioral Testing, and then the .html file for each test)
5. Play the test cases in the suite to simulate behavioral testing (you can open each file as an individualized test case, and play them each by one or play the entire suite!)

### Unit Testing
1) Install Python 2.X.X
2) Follow this guide for setting up a Django virtual env: https://tutorial.djangogirls.org/en/django_installation/
3) Activate your virtualenv (if not already active)
4) Run 'pip install -r requirements.txt' from a cmd in the root directory of the project
5) Use 'python manage.py runserver' to launch the app from cmd.

redditAPI.py unit test: Using Django unit testing, run the manage.py script with testing conditions and the path to the unit test folder. Examples follow: "./manage.py test utilites.tests"; "python manage.py test utilities.tests"

Note: If you don't have PRAW installed, run 'pip install praw'.  PRAW is the Python Reddit API Wrapper and is needed for testing.

Example Results Graph:
![image](https://user-images.githubusercontent.com/31394858/33293040-5d804612-d399-11e7-8a5e-8e43b2f0e376.png)
