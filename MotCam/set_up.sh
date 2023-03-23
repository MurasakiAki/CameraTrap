#!/bin/bash

# Change the permission of the motcam script to executable
chmod u+x motcam

# Add the current directory to the PATH variable
export PATH=$PATH:$(pwd)

# Save the updated PATH variable to the bashrc or profile file - depends on the system
echo "export PATH=\$PATH:$(pwd)" >> ~/.profile
#echo "export PATH=\$PATH:$(pwd)" >> ~/.bashrc

echo "Your motcam is set up."