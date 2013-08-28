#!/bin/bash
export VCSDIR=$PWD
tmux -f conf/tmux.conf attach -t muxer
