import os
import subprocess

from colors import colors
from screens import screens

from os import environ

from libqtile.config import (
    # KeyChord,
    Key,
    # Screen,
    Group,
    Drag,
    Click,
    ScratchPad,
    DropDown,
    Match,
)

from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy

from libqtile import qtile
from qtile_extras import widget
from typing import List  # noqa: F401
from custom.bsp import Bsp as CustomBsp
from custom.bsp import Bsp as CustomBspMargins
from custom.zoomy import Zoomy as CustomZoomy

# from custom.stack import Stack as CustomStack
# from custom.windowname import WindowName as CustomWindowName

mod = "mod4"
mod1 = "mod1"
terminal = "alacritty"
C = "control"


@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == "tk"
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call([home])


# Resize functions for bsp layout
def resize(qtile, direction):
    layout = qtile.current_layout
    child = layout.current
    parent = child.parent

    while parent:
        if child in parent.children:
            layout_all = False

            if (direction == "left" and parent.split_horizontal) or (
                direction == "up" and not parent.split_horizontal
            ):
                parent.split_ratio = max(5, parent.split_ratio - layout.grow_amount)
                layout_all = True
            elif (direction == "right" and parent.split_horizontal) or (
                direction == "down" and not parent.split_horizontal
            ):
                parent.split_ratio = min(95, parent.split_ratio + layout.grow_amount)
                layout_all = True

            if layout_all:
                layout.group.layout_all()
                break

        child = parent
        parent = child.parent


@lazy.function
def resize_left(qtile):
    resize(qtile, "left")


@lazy.function
def resize_right(qtile):
    resize(qtile, "right")


@lazy.function
def resize_up(qtile):
    resize(qtile, "up")


@lazy.function
def resize_down(qtile):
    resize(qtile, "down")


keys = [
    Key(
        [mod],
        "r",
        lazy.spawn("rofi -show drun -show-icons"),
    ),
    Key(
        [mod],
        "w",
        lazy.spawn("rofi -show window"),
    ),
    Key(
        [mod],
        "Return",
        lazy.spawn(terminal),
        desc="Launch terminal",
    ),
    Key(
        [mod],
        "Tab",
        lazy.next_layout(),
        desc="Toggle through layouts",
    ),
    Key(
        [mod, "shift"],
        "Tab",
        lazy.prev_layout(),
        desc="Toggle through layouts",
    ),
    Key(
        [mod, "shift"],
        "b",
        lazy.hide_show_bar("top"),
        desc="Hidden top bar",
    ),
    Key(
        [mod],
        "q",
        lazy.window.kill(),
        desc="Kill focused window",
    ),
    Key(
        [mod, "shift"],
        "c",
        lazy.window.kill(),
        desc="Kill focused window",
    ),
    Key(
        [mod, "shift"],
        "q",
        lazy.spawn("xkill"),
        desc="Force kill window",
    ),
    Key(
        [mod, "shift"],
        "r",
        lazy.restart(),
        desc="Restart Qtile",
    ),
    Key(
        [mod, "shift"],
        "Escape",
        lazy.shutdown(),
        desc="Shutdown Qtile",
    ),
   
    Key(
        [mod],
        "F12",
        lazy.spawn("mousepad /home/pio/.local/share/qtile/qtile.log"),
    ),

    #### Apps
    Key(
        [mod],
        "b",
        lazy.spawn("firefox"),
        desc="Launches firefox",
    ),   
    Key(
        [mod],
        "e",
        lazy.spawn("thunar"),
        desc="Launches Thunar",
    ),

    # Window controls

    ##### BEGIN ----> Move focus: j,k,h,l | move window: shift j,k,h,l
    Key(
        [mod],
        "j",
        lazy.layout.down(),
        desc="Move focus down in current stack pane",
    ),
    Key(
        [mod],
        "k",
        lazy.layout.up(),
        desc="Move focus up in current stack pane",
    ),
    Key(
        [mod],
        "h",
        lazy.layout.left(),
        lazy.layout.next(),
        desc="Move focus left in current stack pane",
    ),
    Key(
        [mod],
        "l",
        lazy.layout.right(),
        lazy.layout.previous(),
        desc="Move focus right in current stack pane",
    ),
    Key(
        [mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        desc="Move windows down in current stack",
    ),
    Key(
        [mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        desc="Move windows up in current stack",
    ),
    Key(
        [mod, "shift"],
        "h",
        lazy.layout.shuffle_left(),
        lazy.layout.swap_left(),
        lazy.layout.client_to_previous(),
        desc="Move windows left in current stack",
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        lazy.layout.swap_right(),
        lazy.layout.client_to_next(),
        desc="Move windows right in the current stack",
    ),

    ##### Expand | Shrink | Reset
    Key(
        [C],
        "1",
        lazy.layout.grow(),
        #lazy.layout.increase_nmaster(),
        desc="Expand Window",
    ),
    Key(
        [C],
        "2",
        lazy.layout.shrink(),
        #lazy.layout.decrease_nmaster(),
        desc="Shrink Window",
    ),
    Key(
        [C],
        "3",
        lazy.layout.reset(),
        desc="Reset window size ratios",
    ),

    #### Max and Mini | Fullscreen | Floating
    Key(
        [mod],
        "m",
        lazy.layout.maximize(),
        desc="Toggle window between minimum and maximum sizes",
    ),
    Key(
        [mod, "shift"],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen",
    ),
    Key(
        [mod],
        "f",
        lazy.window.toggle_floating(),
        desc="Toggle floating on focused window",
    ),

    #### Switch side: space | Move Window: up/down/left/right
    Key(   
        [mod],
        "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc="Switch side",
    ),
    Key(
        [mod],
        "Up",
        lazy.layout.shuffle_up(),
        desc="Move up Window",
    ),
    Key(
        [mod],
        "Down",
        lazy.layout.shuffle_down(),
        desc="Move down Window",
    ),
    Key(
        [mod],
        "Left",
        lazy.layout.swap_left(),
    ),
    Key(
        [mod],
        "Right",
        lazy.layout.swap_right()
    ),

    #### Move focus: Win+Ctrl up/down/left/right
    Key(
        [mod, "control"],
        "Up",
        lazy.layout.up(),
        desc="Move focus up",
    ),
    Key(
        [mod, "control"],
        "Down",
        lazy.layout.down(),
        desc="Move focus down",
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.left(),
        lazy.layout.next(),
        desc="Move focus left",
    ),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.right(),
        lazy.layout.previous(),
        desc="Move focus right",
    ),

    #### Shot Screen
    Key(
        [mod1],
        "c",
        lazy.spawn("flameshot gui"),
        desc="Launches flameshot",
    ),
    Key(
        [],
        "Print",
        lazy.spawn("flameshot screen -n 0 -c"),
        desc="Shot display 0",
    ),
    #Key(
    #    [mod],
    #    "Print",
    #    lazy.spawn("flameshot screen -n 1 -c"),
    #    desc="Shot display 1",
    #), # Second Monitor

    #### Audio bindings for media buttons
    Key(
        [],
        "XF86AudioNext",
        lazy.spawn("playerctl next"),
        desc="Play next audio",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Toggle play/pause audio",
    ),
    Key(
        [],
        "XF86AudioPrev",
        lazy.spawn("playerctl previous"),
        desc="Play previous audio",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("amixer -q -D pulse sset Master toggle"),
        desc="Mute audio",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +1%"),
        desc="Raise volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -1%"),
        desc="Lower volume",
    ),
    Key(
        [mod],
        "grave",
        lazy.group["scratchpad"].dropdown_toggle("term"),
        desc="Toggle scratchpad",
    ),
]

# Command to find out wm_class of window: xprop | grep WM_CLASS
workspaces = [
    {
        "name": "1",
        "key": "1",
        "label": "",
        "layout": "monadtall",
        "matches": [
        ],
        "spawn": [],
        #"spawn": ["solaar"],

    },
    {
        "name": "2",
        "key": "2",
        "label": "",
        "layout": "monadtall",
        "matches": [
        ],
        "spawn": [],
    },
    {
        "name": "3",
        "key": "3",
        "label": "",
        "layout": "monadtall",
        "matches": [
            #Match(wm_class="microsoft-edge"),
            Match(wm_class="google-chrome"),
            #Match(wm_class="firefox"),
        ],
        "spawn": [],
    },
    {
        "name": "4",
        "key": "4",
        "label": "",
        "layout": "monadtall",
        "matches": [
        ],
        "spawn": [],
    },
    {
        "name": "5",
        "key": "5",
        "label": "",
        "layout": "monadtall",
        "matches": [
            Match(wm_class="mpv"),
        ],
        "spawn": [],
    },
    {
        "name": "6",
        "key": "6",
        "label": "",
        "layout": "monadtall",
        "matches": [
           #Match(wm_class="VirtualBox Manager"),
           #Match(wm_class="VirtualBox Machine"),
           #Match(wm_class="Vmware"),
        ],
        "spawn": [],
    },
    {
        "name": "7",
        "key": "7",
        "label": "",
        "layout": "monadtall",
        "matches": [
            #Match(wm_class="icalingua"),
        ],
        "spawn": [],
    },
    {
        "name": "8",
        "key": "8",
        "label": "",
        "layout": "max",
        "matches": [
            #Match(wm_class="TelegramDesktop"),
        ],
        "spawn": [],
    },
    {
        "name": "9",
        "key": "9",
        "label": "",
        "layout": "floating",
        "matches": [
            #Match(wm_class="qbittorrent"),
        ],
        "spawn": [],
    },
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(
        Group(
            workspace["name"],
            matches=matches,
            layout=workspace["layout"],
            spawn=workspace["spawn"],
            label=workspace["label"],
        )
    )
    keys.append(
        Key(
            [mod],
            workspace["key"],
            lazy.group[workspace["name"]].toscreen(),
            desc="Focus certain workspace",
        )
    )
    keys.append(
        Key(
            [mod, "shift"],
            workspace["key"],
            lazy.window.togroup(workspace["name"]),
            desc="Move focused window to another workspace",
        )
    )

groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "term",
                "wezterm",
                x=0.7,
                y=0.01,
                width=0.3,
                height=0.3,
                on_focus_lost_hide=False,
            ),
        ],
    )
)

layout_theme = {
    "border_width": 3,
    "margin": 5,
    "border_focus": "d8dee9",
    "border_normal": "3b4252",
    "font": "FiraCode Nerd Font",
    "grow_amount": 4,
}

layout_theme_margins = {
    "name": "bsp-margins",
    "border_width": 3,
    "margin": [150, 300, 150, 300],
    "border_focus": "3b4252",
    "border_normal": "3b4252",
    "font": "FiraCode Nerd Font",
    "grow_amount": 4,
}

layout_audio = {
    "name": "monadwide-audio",
    "border_width": 3,
    "margin": 100,
    "border_focus": "3b4252",
    "border_normal": "3b4252",
    "font": "FiraCode Nerd Font",
    "ratio": 0.65,
    "new_client_position": "after_current",
}

layouts = [
    # layout.Bsp(**layout_theme, fair=False),
    CustomBsp(**layout_theme, fair=False),
    layout.Max(**layout_theme),
    layout.TreeTab(
        **layout_theme,
        active_bg=colors[1],
        active_fg=colors[0],
        bg_color=colors[1],
        fontsize=16,
        inactive_bg=colors[1],
        inactive_fg=colors[0],
        sections=["", "", ""],
        section_fontsize=18,
        section_fg=colors[0],
    ),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Floating(**layout_theme),
    # layout.Columns(
    #    **layout_theme,
    #    border_on_single=True,
    #    num_columns=3,
    #    # border_focus_stack=colors[2],
    #    # border_normal_stack=colors[2],
    #    split=False,
    # ),
    # layout.RatioTile(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Matrix(**layout_theme, columns=3),
    # layout.Slice(**layout_theme),
    # layout.Tile(shift_windows=True, **layout_theme),
    # CustomBspMargins(**layout_theme_margins),
]

floating_layout = layout.Floating(float_rules=[
            *layout.Floating.default_float_rules,
            Match(wm_type="utility"),
            Match(wm_type="notification"),
            Match(wm_type="toolbar"),
            Match(wm_type="splash"),
            Match(wm_type="dialog"),
            Match(wm_class="file_progress"),
            Match(wm_class="confirm"),
            Match(wm_class="dialog"),
            Match(wm_class="download"),
            Match(wm_class="error"),
            Match(wm_class="notification"),
            Match(wm_class="splash"),
            Match(wm_class="toolbar"),
            Match(func=lambda c: c.has_fixed_size()),
            Match(func=lambda c: c.has_fixed_ratio()),
            Match(wm_class="xdman-Main"),
            Match(wm_class="nitrogen"),
            Match(wm_class="lxappearance"),
            Match(wm_class="Lxappearance"),
            Match(wm_class="pavucontrol"),
            Match(wm_class="gcolor3"),            
])

# Setup bar

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono Medium",
    fontsize=12,
    padding=3,
    background=colors[0],
)
extension_defaults = widget_defaults.copy()

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
#main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
#bring_front_click = "floating_only"
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
