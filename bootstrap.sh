#!/usr/bin/env bash

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

	if [[ ! -f "./bin/webrecorder-player" ]]; then
		printf "\e[31m PLAYER NOT FOUND \e[39m\n"
		wget -O bin/webrecorder-player "$s3/webrecorder-player/$player_version/$player"
		chmod +x ./bin/webrecorder-player
	else
		printf "\e[32m PLAYER FOUND \e[39m\n"
	fi
}

download_warcs() {
    for manifest in $(find manifests/ -name \*.yml); do
        warcfile=$(grep "warc-file:" "./$manifest")
        : "${warcfile##warc-file: \"warcs/}"
        : "${_%%\"}"
        warc="$_"
        if [[ ! -f "./warcs/$warc" ]]; then
			printf "\e[31m WARC NOT FOUND \e[39m%s\n" "$warc"
			wget -P ./warcs "$s3/tests/$warc"
		else
			printf "\e[32m WARC FOUND \e[39m%s\n" "$warc"
		fi
    done
}

download_geckodriver() {
    case $(uname -s) in
		"Linux")
			dlurl="https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz"
			;;
		"Darwin")
			dlurl="https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-macos.tar.gz"
			;;
	esac

	if [[ ! -f "./bin/geckodriver" ]]; then
	    printf "\e[31m GEKODRIVER NOT FOUND \e[39m\n"
	    wget -O bin/gekodriver.tar.gz "${dlurl}"
	    tar xvzf ./bin/gekodriver.tar.gz -C ./bin/
	    rm ./bin/gekodriver.tar.gz
	else
	    printf "\e[32m GEKODRIVER FOUND \e[39m\n"
	fi
}

main() {
	download_player
	download_warcs
	download_geckodriver
}


main
