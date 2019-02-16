
# Note: the script itself is untested but the commands work
mkdir ~/build-git-lfs
cd ~/build-git-lfs

# If you are in the future, maybe check
# https://github.com/git-lfs/git-lfs/issues/2464
# to see if ARM git-lfs package has been added.
#
# We need go in order to build git lfs manually
# The version package from apt was too old, so have manually install it too
wget --content-disposition https://dl.google.com/go/go1.11.5.linux-armv6l.tar.gz
sudo tar -C /usr/local -xzf go1.11.5.linux-armv6l.tar.gz

export PATH=$PATH:/usr/local/go/bin
mkdir ~/go
export GOPATH=~/go


# On to git-lfs.
# Instead of cloning with git, theres also
#go get github.com/git-lfs/git-lfs
# I think cloning was the one that worked but don't remember
git clone --recursive https://github.com/git-lfs/git-lfs.git -b v2.5.2
cd git-lfs
make
cd bin
sudo cp git-lfs /usr/local/bin/git-lfs
