export WS="/home/ubuntu"

function start_pineapple() {
    echo "Starting"
    screen -S controller -d -m "$HOME/code/pineapple/setup_files/start_pineapple.bash"
    sleep 3
    echo "$(screen -ls)"
}

function compile_and_start_pineapple() {
    cd $WS/code/catkin_ws/
    catkin_make install
    sleep 5
    start_pineapple
}
