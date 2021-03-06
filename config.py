# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2020 tazrog
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
import os
import subprocess

from typing import List  # noqa: F401

mod = "mod4"
term="xterm"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

keys = [
    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q -D pulse sset Master 1%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q -D pulse sset Master 1%+")),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("xterm")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "f", lazy.spawn("firefox")),
    Key([mod], "F3", lazy.spawn("pcmanfm")),
    Key([mod], "v", lazy.spawn("vlc")),
    Key([mod], "F1", lazy.spawn("dmenu_run")),
    Key([mod], "g", lazy.spawn ("/home/tazrog/Godot/./Godot3")),
    Key([mod], "F12", lazy.spawn("eqtile")),
    Key([mod], "e", lazy.spawn("/home/tazrog/Programs/./tutanota-desktop-linux.AppImage")),
    Key([mod], "b", lazy.spawn("/home/tazrog/BurpSuiteCommunity/./BurpSuiteCommunity")),
    Key([mod], "t", lazy.spawn("/home/tazrog/Programs/tor-browser_en-US/Browser/./start-tor-browser")),
    Key([mod], "a", lazy.spawn("atom")),
    Key([mod], "s", lazy.spawn("/opt/sublime_text/./sublime_text")),

    #MonadTall Key Bindings
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "shift"], "space", lazy.layout.flip()),
]

groups = [
    Group('1'),
    Group('2'),
    Group('3'),
    Group('4'),
    Group('5'),
    Group('6'),
    Group('7'),
    Group('8'),

]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.MonadTall(border_focus='#00ffab', border_normal='#ff0000'),
    #layout.Max(),
    #layout.Stack(num_stacks=2,border_focus='#00ffab', border_normal='#ff0000'),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    layout.Matrix(border_focus='#00ffab', border_normal='#ff0000'),
    #layout.MonadTall(),
    #layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Roboto-Regular',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(padding=5),
                #widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Sep(linewidth=2),
                #widget.Prompt(),
                widget.WindowName(),
                widget.Cmus(padding=5),
                widget.TextBox('Updates-', 
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(term + ' -e sudo pacman -Syu')}),
                widget.Pacman(mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(term + ' -e sudo pacman -Syu')}),
                widget.Sep(),
                widget.TextBox(text='???'),
                widget.ThermalSensor(metric=False, 
                    threshold=160, 
                    padding=3),
                widget.TextBox(text='???', 
                    padding=5),
                widget.Memory(mouse_callbacks ={'Button1': lambda qtile: qtile.cmd_spawn(term + ' -e htop')}),
                widget.MemoryGraph(mouse_callbacks ={'Button1': lambda qtile: qtile.cmd_spawn(term + ' -e htop')}),
                widget.CPU(padding=5, 
                    mouse_callbacks ={'Button1': lambda qtile: qtile.cmd_spawn(term + '- e htop')}),
                widget.CPUGraph(type='box', 
                    fill_color='00ffab',
                    border_color='00ffab', 
                    mouse_callbacks ={'Button1': lambda qtile: qtile.cmd_spawn(term + ' -e htop')}),
                widget.TextBox(text='???', 
                    padding=5),
                widget.Volume(),
                widget.Systray(padding=5),
                widget.Clock(format='%m/%d/%y %a %H%M', 
                    padding =5),
                widget.Sep(linewidth=2),
                widget.QuickExit(default_text=' ??? ',
                    countdown_start=5),
                widget.Sep(linewidth=2),
                widget.QuickRestart(default_text= ' ??? '),
                widget.Sep(linewidth=2),

            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
