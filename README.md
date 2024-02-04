# Dynamic wallpaper

A dynamic wallpaper setter with weekdays and weekends.

First, test your setup with
```
$ ./dynamic-wallpaper-with-workhours.py -r "$(pwd)" -w work_wallpaper -t images/forest
```
and then use the additional `-cron` flag to get corresponding crontab command
```fi
$ ./dynamic-wallpaper-with-workhours.py -r "$(pwd)" -w work_wallpaper -t images/forest
# Edit your crontab and add a job
$ crontab -e

# Add this line
0 * * * * env DISPLAY=":0" DESKTOP_SESSION="gnome" DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus" XDG_RUNTIME_DIR="/run/user/1000"  /xxx/dynamic-wallpaper-with-workhours.py -r /xxx -w work_wallpaper -t images/forest
```

You can then put the corresponding line in crontab with
```sh
$ crontab -e
```
