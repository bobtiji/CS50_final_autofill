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
  Final-Autofill:
    image: bobtiji/cs50_final
    ports:
      - '8003:8003'
    restart: unless-stopped
```

The way it works is very simple. It is a Flask app hosted by gunicorn running inside a docker container. I normally would've used something like nginx host a website like this but some reason, couldn't make it work. The app uses a sqlite DB to create and log users inside one table and their respective data in another. It proposes a simple way to fill out all the data neccessary to complete a daily covid questionnaire that's hosted one google.forms. 

Since this app also needed a login/register/users page, I repurposed the code written previously in the Finance assignment. The html uses some jinja notation to deal with variables but not a lot since i didn't need to iterate through a lot of data per page i found i easier to just hard code it. After all, one user is never gonna have more than one entry in the DATA table to it is very little data total.

The app.py is where the "magic" happens. It uses a couple routes to take in the data and format it in a way that's usable for google forms.

In the latest version, I made variables for the entry codes so that it's easier to modify to fit your own google forms. To do so, one needs to check via developper tools to figure out the container ids of their specific google form and input them there. It should look something like this:

entry.1527757341: aaaaaaaaaaaaaaa
entry.1315296153: 123
entry.2077813938: 
entry.1429378478: Colonel
entry.1170687127: Cie A 2R22R
entry.1910594951: 313
entry.1958299218: Non
entry.507671141: Non
entry.1364729209: Non
entry.1837577196: Oui
dlut: 1647115662537
hud: true
entry.1429378478_sentinel: 
entry.1170687127_sentinel: 
entry.1910594951_sentinel: 
entry.1958299218_sentinel: 
entry.507671141_sentinel: 
entry.1364729209_sentinel: 
entry.1837577196_sentinel: 
entry.1100725150_sentinel: 
fvv: 1
partialResponse: [null,null,"-7951309878151434296"]
pageHistory: 0
fbzx: -7951309878151434296

It's fairly easy to identify the keys you need because of their value.

On the other hand , the page themselves are not very dynamic in their diplay, if you end up changing forms, there's a bunch of container names that are gonna need changing.

The make function is the one that does the most work and it ain't much really. It takes in the data and the entry code and produces a url. The app is really simple but it's going to save so much time to so many people.