SRC_PATH="$(readlink "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")"
RUN_PATH=${SRC_PATH%/*}/..
cd "$RUN_PATH" || exit
kill $(cat ./application.pid)