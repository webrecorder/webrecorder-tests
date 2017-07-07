#!/bin/bash

warc_s3="https://s3.amazonaws.com/webrecorder-builds/tests"

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
		wget -O bin/webrecorder-player "https://s3.amazonaws.com/webrecorder-builds/webrecorder-player/develop/$player"
		chmod +x ./bin/webrecorder-player
	else
		printf "\e[32m PLAYER FOUND \e[39m\n"
	fi
}

download_warcs() {
	warcs=$(awk '/warc-file/ {print $2}' manifest.yml)

	for warc in $warcs; do
		if [ ! -f "./warcs/$warc" ]; then
			printf "\e[31m WARC NOT FOUND \e[39m%s\n" "$warc"
			wget -P ./warcs "$warc_s3"/"$warc"
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
