# Raspberry Pi 4 IoT Alarm Clock

This project was a capstone project for the EE/CE 4201 Computing Systems Lab. It consists of
a DHT22 humidity and temperature sensor, HC-SR04 ultrasonic sensor, I2C LCD screen, and a Raspberry Pi
camera module.
## Purpose
The purpose of this project was to allow the user to see the date and time as well as the temperature
and humidity in their room. The user can also set an alarm time using a python scheduler, and whenever
the alarm goes off, it stays in an infinite loop until the user is registered as being "near" the
ultrasonic sensor.
## How it works
The alarm uses multithreading to incorporate the time and sensor readings while the alarm module
works in a sequential fashion: it plays an alarm, checks the distance, and then loops back
if the user is not close enough. Once the user is close enough, an email is sent to their email,
letting the user know how close they were to the alarm and how many alarm loops it took to
get up and turn off the alarm.
## Workflow
During the process of the project, most, if not all work, was done in python virtual environments
because we had not coded in Python before. Most of it was self-taught by using online resources
(thank you, Paul McWhorter, for all of your wonderful videos).

We chose to exclusively work inside virtual environments because we were constantly testing
new features on a single device. What if there was a dependency issue? That's why we had virtual
environments. We could simply use a *pip freeze > <file_name>.txt* and retrieve packages.
Thus, it was easier to make directories for tests and subdivide into "feature directories."
We would ensure that each new module worked by itself, and eventually learned new things such
as the

    if __name__ == "__main__"
    
feature that allowed us to only use pieces of code if it was the module directly being ran from
the CLI.

Eventually, Michael learned how to properly use git via the CLI, and that allowed us to have
a much better version control system (VCS). Work could now be done on feature branches instead,
and we could merge or even use pull requests if necessary.
## Security
Among other things, we all needed to use the device one way or another because we only had one...
So we chose to use SSH to connect to our Raspberry Pi. Initially, we just port-forwarded, but
that can be very unsafe. Thus, we began to use remote.it as a VPI, and then we also gave the
Raspberry Pi a static IP in the case that the IP address changed due to DHCP.

.gitignores were also used due to use having sensitive information we did not want to share.
Along with that, those sensitive files were also chmod'd so that only the root-level user
could ever read or write to them.
## Future Improvements
Although the semester is over, this project is still active on occasion, and there are
features that we did not implement because we could not fully integrate them before
the project deadline. Among these things are a weather API that tells you the temperature,
a keypad that Michael worked on that gets a password, and will hopefully allow the user
to set the time, and other such things if you would like to explore them.
