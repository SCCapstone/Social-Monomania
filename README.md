# Welcome to Social-Monomania!
This repository is a Senior Project currently under development. The following is the description of the project:

Gamecock Social Media Listening
The USC International Center for Event Research and Education housed in the College of Hospitality, Retail, and Sport Management would like to propose the development of a social media listening tool that will allow USC faculty to engage in research that tracks social media posts and visual content across multiple social media platforms.  Recent research has shown the top five social media platforms according to ebizmba.com (July 2017), are Facebook, YouTube, Instagram, Twitter, and Reddit, but social media research also can include mainstream news, blogs, forums, and forum replies.  By developing an easy to navigate user interface, faculty can undertake searches of social media posts which include specified keywords and phrases and exclude other specified keywords and phrases.   Once the social media searches are concluded, the software will display visually appealing screens for an easy graphical review of "Sentiment" analysis, Wordclouds, keyword and date line-charts and list all original responses for a more detailed review. Searches must be able to be restricted by date and geography (Geofencing).

This will be a web application.

Example Results Graph:
![image](https://user-images.githubusercontent.com/31394858/33293040-5d804612-d399-11e7-8a5e-8e43b2f0e376.png)

TESTING:

1) Install Python 2.X
2) Follow this guide for setting up a Django virtual env: https://tutorial.djangogirls.org/en/django_installation/
3) Activate your virtualenv (if not already active)
4) Run 'pip install -r requirements.txt' from a cmd in the root directory of the project
5) Use 'python manage.py runserver' to launch the app from cmd.

redditAPI.py unit test: Using Django unit testing, run the manage.py script with testing conditions and the path to the unit test folder. Examples follow: "./manage.py test utilites.tests"; "python manage.py test utilities.tests"

Note: If you don't have PRAW installed, run 'pip install praw'.  PRAW is the Python Reddit API Wrapper and is needed for testing.
