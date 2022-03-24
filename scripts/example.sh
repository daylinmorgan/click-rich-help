#!/usr/bin/env bash

# script used to demo click_rich_help.example
# use asciinema to generate an embeddable video
# asciinema rec -c scripts/example.sh -t "click-rich-help demo"
# then update the link/screenshot on the README.md

base_command="python -m click_rich_help.example"
SDELAY=2
LDELAY=5
sleep 1
clear

play_command() {

    echo
    echo $1 | pv -qL 20
    echo
    sleep $SDELAY
    eval "$1"
    sleep $LDELAY
    clear

}


echo "Allow me to demonstrate the power of click-rick-help!"
echo "Let's begin with the example module's main help page"
play_command "${base_command} -h"

echo "Next let's look at the help for cmd1"
play_command "${base_command} cmd1 -h"

echo "Did that say something about cmd2, let's try it now"
play_command "${base_command} cmd2 -h"

echo "Before we test our own commands let me double check cmd3"
play_command "${base_command} cmd3 -h"

echo "One could define their styles using a dict or a rich.theme.Theme"
play_command "${base_command} theme -h"

echo "Hm Let's test some strings and styles"
play_command "${base_command} test --string '[i blue]blue and italic[/i blue] not blue or italic' --style 'bold grey0 on red'"

echo "Lastly, we can take a little quick peek at the src of this example"
play_command "${base_command} src cmd2"

echo "Let's look at the test command!"
play_command "${base_command} src test"

echo
echo
echo "Thanks for watching!"
