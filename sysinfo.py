#!/usr/bin/env python3
"""Compact system information CLI tool."""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import time

try:
    import psutil
except ImportError:
    print("psutil not found. Install with: pip install psutil")
    sys.exit(1)

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
DIM = "\033[2m"


def color_percent(pct: float) -> str:
    if pct >= 90:
        c = RED
    elif pct >= 70:
        c = YELLOW
    else:
        c = GREEN
    return f"{c}{pct:5.1f}%{RESET}"


def bar(pct: float, width: int = 20) -> str:
    filled = int(pct / 100 * width)
    if pct >= 90:
        c = RED
    elif pct >= 70:
        c = YELLOW
    else:
        c = GREEN
    return f"{c}{'█' * filled}{'░' * (width - filled)}{RESET}"


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def section(title: str) -> None:
    term_width = shutil.get_terminal_size().columns
    print(f"\n{BOLD}{CYAN}{title}{RESET} {DIM}{'─' * (term_width - len(title) - 2)}{RESET}")


def show_cpu(per_core: bool) -> None:
    section("CPU")
    freq = psutil.cpu_freq()
    count_phys = psutil.cpu_count(logical=False)
    count_logi = psutil.cpu_count(logical=True)
    load = psutil.getloadavg()

    overall = psutil.cpu_percent(interval=0.3)
    print(f"  Usage   : {bar(overall)} {color_percent(overall)}")
    print(f"  Cores   : {count_phys} physical, {count_logi} logical")
    if freq:
        print(f"  Freq    : {freq.current:.0f} MHz  (max {freq.max:.0f} MHz)")
    print(f"  Load avg: {load[0]:.2f}  {load[1]:.2f}  {load[2]:.2f}  (1m / 5m / 15m)")

    if per_core:
        percpu = psutil.cpu_percent(interval=0.3, percpu=True)
        for i, p in enumerate(percpu):
            print(f"  Core {i:>2}  : {bar(p, 10)} {color_percent(p)}")


def show_memory() -> None:
    section("Memory")
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()

    print(f"  RAM     : {bar(vm.percent)} {color_percent(vm.percent)}"
          f"  {human(vm.used)} / {human(vm.total)}")
    print(f"  Swap    : {bar(sw.percent)} {color_percent(sw.percent)}"
          f"  {human(sw.used)} / {human(sw.total)}")


def show_disk() -> None:
    section("Disk")
    parts = psutil.disk_partitions(all=False)
    for p in parts:
        try:
            usage = psutil.disk_usage(p.mountpoint)
        except PermissionError:
            continue
        pct = usage.percent
        print(f"  {p.mountpoint:<18} {bar(pct)} {color_percent(pct)}"
              f"  {human(usage.used)} / {human(usage.total)}"
              f"  {DIM}[{p.fstype}]{RESET}")


def show_network() -> None:
    section("Network")
    stats = psutil.net_io_counters(pernic=True)
    for nic, s in stats.items():
        if s.bytes_sent == 0 and s.bytes_recv == 0:
            continue
        print(f"  {nic:<12}  ↑ {human(s.bytes_sent):>10}  ↓ {human(s.bytes_recv):>10}"
              f"  {DIM}err↑{s.errout} err↓{s.errin}{RESET}")


def show_processes(n: int, sort_by: str) -> None:
    section(f"Top {n} Processes  (sorted by {sort_by})")
    key = "cpu_percent" if sort_by == "cpu" else "memory_percent"
    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Warm up CPU measurements
    time.sleep(0.1)
    procs.sort(key=lambda x: x.get(key) or 0, reverse=True)

    print(f"  {'PID':>7}  {'CPU%':>6}  {'MEM%':>6}  {'STATUS':<10}  NAME")
    for p in procs[:n]:
        cpu = p.get("cpu_percent") or 0.0
        mem = p.get("memory_percent") or 0.0
        print(f"  {p['pid']:>7}  {color_percent(cpu)}  {color_percent(mem)}"
              f"  {DIM}{p.get('status', '?'):<10}{RESET}  {p['name']}")


def show_system() -> None:
    section("System")
    boot = psutil.boot_time()
    uptime_s = time.time() - boot
    h, rem = divmod(int(uptime_s), 3600)
    m, s = divmod(rem, 60)
    uname = platform.uname()
    print(f"  Host    : {uname.node}")
    print(f"  OS      : {uname.system} {uname.release}")
    print(f"  Kernel  : {uname.version[:60]}")
    print(f"  Uptime  : {h}h {m}m {s}s")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sysinfo",
        description="Compact system information overview",
    )
    parser.add_argument("--cpu", action="store_true", help="Show CPU info (default: all)")
    parser.add_argument("--mem", action="store_true", help="Show memory info")
    parser.add_argument("--disk", action="store_true", help="Show disk info")
    parser.add_argument("--net", action="store_true", help="Show network info")
    parser.add_argument("--procs", action="store_true", help="Show top processes")
    parser.add_argument("--per-core", action="store_true", help="Show per-core CPU usage")
    parser.add_argument("--top", type=int, default=10, metavar="N", help="Number of processes (default: 10)")
    parser.add_argument("--sort", choices=["cpu", "mem"], default="cpu", help="Sort processes by cpu or mem")
    parser.add_argument("--watch", type=float, metavar="SEC", help="Refresh every SEC seconds (e.g. --watch 2)")

    args = parser.parse_args()
    show_all = not any([args.cpu, args.mem, args.disk, args.net, args.procs])

    def render() -> None:
        if args.watch:
            os.system("clear")
        if show_all or args.cpu:
            show_cpu(args.per_core)
        if show_all or args.mem:
            show_memory()
        if show_all or args.disk:
            show_disk()
        if show_all or args.net:
            show_network()
        if show_all or args.procs:
            show_processes(args.top, args.sort)
        if show_all:
            show_system()
        print()

    if args.watch:
        try:
            while True:
                render()
                time.sleep(args.watch)
        except KeyboardInterrupt:
            pass
    else:
        render()


if __name__ == "__main__":
    main()
