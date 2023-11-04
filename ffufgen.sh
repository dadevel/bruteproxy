#!/usr/bin/env bash
set -eu
shopt -s nullglob

main() {
    for file in ./logins/http-*.req.txt; do
        fuzz "$file" http "$@"
    done
    for file in ./logins/https-*.req.txt; do
        fuzz "$file" https "$@"
    done
}

fuzz() {
    echo -n ffuf -request "$1" -request-proto "$2" -of csv -o "${1%.req.txt}.ffuf.csv"
    for arg in "${@:3}"; do
        printf ' %q' "${arg}"
    done
    echo
}

main "$@"
