from i3pystatus import Status, get_module
from latency import Latency

status = Status(standalone=True)

# Displays clock like this:
# Tue 30 Jul 11:59:46 PM KW31
#                          ^-- calendar week
status.register("clock",
        format="%Y-%m-%d %H:%M:%S",)

# Shows the average load of the last minute and the last 5 minutes
# (the default value for format is used)
status.register("load",
        format="{avg1}",
        on_leftclick="urxvt -e htop",
)

status.register("mem",
        format="RAM: {used_mem}/{total_mem}MiB ({percent_used_mem}%)",
        color="#FFFFFF")

# Shows your CPU temperature, if you have a Intel CPU
status.register("temp",
        format="{temp:.0f}°C",)

# The battery monitor has many formatting options, see README for details

# This would look like this, when discharging (or charging)
# ↓14.22W 56.15% [77.81%] 2h:41m
# And like this if full:
# =14.22W 100.0% [91.21%]
#
# This would also display a desktop notification (via D-Bus) if the percentage
# goes below 5 percent while discharging. The block will also color RED.
# If you don't have a desktop notification demon yet, take a look at dunst:
#   http://www.knopwob.org/dunst/
status.register("battery",
        format="{status}/{consumption:.1f}W {percentage:.2f}% {remaining:%E%H:%M}",
        alert=True,
        alert_percentage=5,
        full_color="#FFFFFF",
        status={
            "DIS": "↓",
            "CHR": "↑",
            "FULL": "=",
            },)

# Shows the address and up/down state of eth0. If it is up the address is shown in
# green (the default value of color_up) and the CIDR-address is shown
# (i.e. 10.10.10.42/24).
# If it's down just the interface name (eth0) will be displayed in red
# (defaults of format_down and color_down)
#
# Note: the network module requires PyPI package netifaces
@get_module
def cycle_format(self, formats):
    formats.append(self.format_up)
    self.format_up = formats.pop(0)

status.register("network",
        interface="enp0s25",
        format_up="{interface}: UP",
        color_up="#FFFFFF",
        dynamic_color=False,
        on_rightclick=[cycle_format, ["{interface}: {v4cidr}", "{interface}: {v6cidr}"]]
)

# Note: requires both netifaces and basiciw (for essid and quality)
status.register("network",
        interface="wlp4s0",
        format_up="{interface}: {essid} ({quality:03.0f}%)",
        color_up="#FFFFFF",
        dynamic_color=False,
        on_rightclick=[cycle_format, ["{interface}: {v4cidr}", "{interface}: {v6cidr}"]]
)

status.register("ping")

# Shows disk usage of /
# Format:
# 42/128G [86G]
status.register("disk",
        path="/",
        format="{used:.1f}/{total:.1f}GiB",)

# Shows pulseaudio default sink volume
#
# Note: requires libpulseaudio from PyPI
status.register("pulseaudio",
        format="♪{volume}%",)

# Shows mpd status
# Format:
# ▶ Song name - Song artist
status.register("mpd",
        format="{status} {filename}{title}[ - {artist}]",
        status={
            "pause": "▷",
            "play": "▶",
            "stop": "◾",
            },
        on_rightclick="urxvt -e ncmpcpp"
)

status.run()

