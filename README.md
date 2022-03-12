# CS50_final_autofill

This is my CS50 final project. I call it: Mindless Repetition Avoidance Automaton

It consists of a webapp using python, flask and gunicorn packaged in a very small container.

It's main purpose is to fill out a specific google form that has to be done daily.

Documentation @ https://github.com/bobtiji/CS50_final_autofill

Container @ https://hub.docker.com/r/bobtiji/cs50_final

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