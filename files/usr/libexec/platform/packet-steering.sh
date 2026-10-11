#!/bin/sh
# WF810DF mixed plane: preserve NSS IRQ placement and steer host-only LAN.
if [ "$(cat /tmp/sysinfo/board_name 2>/dev/null)" = "fpt,wf810df" ] &&
   [ "$(uci -q get nss.general.enabled)" = "1" ] &&
   [ -e /var/run/wf810df-nss-plane-ready ]; then
    for q in /sys/class/net/wan/queues/rx-*/rps_cpus; do
        [ ! -w "$q" ] || echo 2 > "$q"
    done
    for q in /sys/class/net/lan/queues/rx-*/rps_cpus; do
        [ ! -w "$q" ] || echo 1 > "$q"
    done
    for q in /sys/class/net/phy*/queues/rx-*/rps_cpus; do
        [ ! -w "$q" ] || echo 2 > "$q"
    done
    ethtool -K lan tx off >/dev/null 2>&1
    exit 0
fi
flows="$(uci -q get network.@globals[0].steering_flows)"
case "$flows" in
    ''|*[!0-9]*) exec /usr/libexec/network/packet-steering.uc "$1" ;;
    *) exec /usr/libexec/network/packet-steering.uc -l "$flows" "$1" ;;
esac
