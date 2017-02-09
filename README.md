# RaspberryPi Thermostat

This is my most recent project and I've just begun working on it.  It is likely that most of what is here now will be heavily modified by the time I feel it is close to finished

In the end I hope to have this well documented however that will probably be an afterthought considering I don't know how to do documentation in python currently (This is my first project using python in years, I'm relearning it as I go)

~~For now I'm going with a straightforward Restfulish api interface for the gpio pins.  It should be decently secure since it requires the user to be logged in beforehand, however there are almost definitely security issues here.~~
Decided to go with a daemon approach, it just seems better overall.