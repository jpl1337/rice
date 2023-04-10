# Basic aliases
alias aliases='vim ~/.bash_aliases; source ~/.bashrc'
alias rl='source ~/.bashrc'
alias c='clear'
alias x='exit'
alias l='ls -alh --color=auto'
alias g='grep --color=auto'
alias svim='sudo vim'

# APT aliases
alias upup='sudo apt update'
alias upup='sudo apt update; sudo apt upgrade -y'
alias apti='sudo apt install -y'
alias aptar='sudo apt autoremove'
alias aptr='sudo apt remove -y'
alias ptest='ping -c1 8.8.8.8; ping -c1 google.com; dig fb.com'