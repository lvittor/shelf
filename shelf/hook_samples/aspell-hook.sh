#!/bin/bash

ASPELL=$(which aspell)
if [ $? -ne 0 ]; then
    echo "Aspell not installed - unable to check spelling" >&2
    exit 1
else
    WORDS=$($ASPELL --mode=email --add-email-quote='#' list < "$1" | sort -u)
fi
if [ -n "$WORDS" ]; then
    printf "\e[1;33m  Possible spelling errors found in commit message:\n\e[0m\e[0;31m%s\n\e[0m\e[1;33m  Use git commit --amend to change the message.\e[0m\n\n" "$WORDS" >&2
    exit 1
fi