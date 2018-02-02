# Welcome to Social-Monomania!
This repository is a Senior Project currently under development. The following is the description of the project:

Gamecock Social Media Listening
The USC International Center for Event Research and Education housed in the College of Hospitality, Retail, and Sport Management would like to propose the development of a social media listening tool that will allow USC faculty to engage in research that tracks social media posts and visual content across multiple social media platforms.  Recent research has shown the top five social media platforms according to ebizmba.com (July 2017), are Facebook, YouTube, Instagram, Twitter, and Reddit, but social media research also can include mainstream news, blogs, forums, and forum replies.  By developing an easy to navigate user interface, faculty can undertake searches of social media posts which include specified keywords and phrases and exclude other specified keywords and phrases.   Once the social media searches are concluded, the software will display visually appealing screens for an easy graphical review of "Sentiment" analysis, Wordclouds, keyword and date line-charts and list all original responses for a more detailed review. Searches must be able to be restricted by date and geography (Geofencing).

This will be a web application.

## Requirements To Run
``python=2.7.12
Django==1.11.7
dj-database-url==0.4.1
gunicorn==19.6.0
psycopg2==2.6.2
whitenoise==3.3.1``

**Note: This application directly restarts and updates after each commit, applying all changes. It uses the commands found in both this README and the URL below.**

*This app follows standard Heroku deployment procedures for python, which can be found here:*
https://devcenter.heroku.com/articles/getting-started-with-python#introduction

The command that Heroku's standard procfile uses (and that we use as well) to deploy is:

```web: gunicorn social_monomania.wsgi --log-file -```

## Testing
### Behavioral Testing
We are using Selenium to conduct our behavioral testing.  Selenium uses a Firefox addon called Katalon Automation Recorder.  To use this addon:

1.) Download the latest version of Firefox: https://www.mozilla.org/en-US/firefox/new/
2.) Install the addon: https://addons.mozilla.org/en-US/firefox/addon/katalon-automation-record/
3.) Run the addon from the browser toolbar
4.) Open the test suite from our github
5.) Play the test cases in the suite to simulate behavioral testing


## Example Results Graph:
![image](https://user-images.githubusercontent.com/31394858/33293040-5d804612-d399-11e7-8a5e-8e43b2f0e376.png)
