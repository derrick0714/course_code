echo "compiling $1"
g++ "$1" -o out.bin
echo "finish compiling"
echo "running $1"
./out.bin
