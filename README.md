# Mindless Repetition Avoidance Automaton

This is my CS50 final project. I call it: Mindless Repetition Avoidance Automaton

It consists of a webapp using python, flask and gunicorn packaged in a very small container.

It's main purpose is to fill out a specific google form that has to be done daily by hundreds of coworker.

Documentation @ https://github.com/bobtiji/CS50_final_autofill

Container @ https://hub.docker.com/r/bobtiji/cs50_final

Video presentation @ https://www.youtube.com/watch?v=eXka62k927w

Docker-compose looks something like this

```
version: '3'
services:
  cs50-final:
    image: bobtiji/cs50_final:latest
    ports:
      - '8003:8003'
    restart: unless-stopped
```

The way it works is very simple. It is a Flask app hosted by gunicorn running inside a docker container. The app uses a sqlite DB to create and log users inside one table and their respective data in another.

Since this app also needed a login/register/users page, I repurposed the code written previously in the Finance assignment.

It proposes a simple way to fill out all the data neccessary to complete a daily covid questionnaire that's hosted one google.forms. 

I normally would've used something like nginx host a website like this but some reason, couldn't make it work.

The app.py is where the "magic" happens. It uses a couple routes to take in the data and format it in a way that's usable for google forms.

In the latest version, I made variables for the entry codes so that it's easier to modify to fit your own google forms. On the other hand , the page themselves are not very dynamic in their diplay, if you end up changing forms, there's a bunch of container names that are gonna need changing.

The make function is the one that does the most work and it ain't much really. It takes in the data and the entry code and produces a url. The app is really simple but it's going to save so much time to so many people.