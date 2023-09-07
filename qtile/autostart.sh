#!/bin/bash

xrandr -s 1920x1080
vmware-user-suid-wrapper & #wmare copy/paste
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 & disown # start polkit agent from GNOME
gnome-keyring-daemon --start
xset -b # disable beep
#nitrogen --restore & #wallpaper
feh --bg-scale ~/.config/qtile/wallpaper.jpg

arr=("xfce4-power-manager" "xclip" "xfce4-notifyd" "picom")

for value in ${arr[@]}; do
	if [[ ! $(pgrep ${value}) ]]; then
		exec "$value" &
	fi
done

#if [[ ! $(pgrep xob) ]]; then
#	exec "sxob"
#fi
