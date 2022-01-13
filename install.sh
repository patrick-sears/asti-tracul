#!/bin/bash


name="asti-tracul"
pname="prs-$name"

wd=`pwd -P`

cd "$HOME/bin"

if [[ -L "$pname" ]]; then
  unlink "$pname"
fi

ln -s "$wd/main.py" "$pname"


