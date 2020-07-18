#!/bin/bash
feh --bg-fill --randomize ~/Background/* &

exec nm-applet &
exec blueman-applet &
exec numlockx &
