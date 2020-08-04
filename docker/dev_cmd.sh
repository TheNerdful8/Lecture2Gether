#!/bin/bash
set -e

function send() {
    tmux send -t lecture2gether "$1
"
    sleep 0.1
}

tmux new-session -c /app/src -d -s lecture2gether

send "tmux set-window-option remain-on-exit on"
send "tmux split-window -d -c /app/src/frontend 'npm install && npm run serve'"
send "tmux split-window -d -c /app/src/backend 'poetry install --no-root && poetry run ./app.py'"
send "tmux split-window -d 'redis-server'"
send "tmux select-layout tiled"
send "clear"
send "# You can quit by pressing 'CTRL+B D' or issuing the command 'tmux kill-session'"

tmux attach-session -t lecture2gether

