#!/bin/bash

s3="https://s3.amazonaws.com/webrecorder-builds"
player_version="develop"

download_player() {
	case $(uname -s) in
		"Linux")
			player="webrecorder-player-linux"
			;;
		"Darwin")
			player="webrecorder-player-osx"
			;;
	esac

	if [ ! -f "./bin/webrecorder-player" ]; then
		printf "\e[31m PLAYER NOT FOUND \e[39m\n"
		wget -O bin/webrecorder-player "$s3/webrecorder-player/$player_version/$player"
		chmod +x ./bin/webrecorder-player
	else
		printf "\e[32m PLAYER FOUND \e[39m\n"
	fi
}

download_warcs() {
    warcs=$(find manifests/ -name \*.yml -exec awk 'match($0,/warc-file:\s"warcs\/([^"]+)"/, arr) {print arr[1]}' {} \;)
    for warc in ${warcs}; do
		if [ ! -f "./warcs/$warc" ]; then
			printf "\e[31m WARC NOT FOUND \e[39m%s\n" "$warc"
			wget -P ./warcs "$s3/tests/$warc"
		else
			printf "\e[32m WARC FOUND \e[39m%s\n" "$warc"
		fi
	done
}

main() {
	download_player
	download_warcs
}

main
