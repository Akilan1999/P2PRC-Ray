# P2PRC-Ray
<img width="1155" alt="shapes at 23-11-16 11 20 24" src="https://github.com/Akilan1999/P2PRC-Ray/assets/31743758/e5bda3df-15f4-490f-82ff-0a8247c03fe9">

## What is P2PRC ?
P2PRC is a custom peer-to-peer network designed to orchestrate tasks on machines behind NAT.
- P2PRC source code: https://github.com/Akilan1999/p2p-rendering-computation

## What is Ray ?
Ray is an open-source unified compute framework that makes it easy to scale AI and Python workloads.
- Ray source code: https://github.com/ray-project/ray


## Flow of the setup
The following sections talks about how Ray is setup accross a P2P network.
The main aim is to get the most basic form of the Ray Cluster working.
Since this is currently a proof of concept repo, Later releases will focus
on making it more stable based on the interest of the community.

<img width="1762" alt="shapes at 23-11-16 20 07 15" src="https://github.com/Akilan1999/P2PRC-Ray/assets/31743758/b5fab822-76fe-422b-be53-7b8a75db2f76">

## Just to get rid of my internal frustration
I did this minor porting effort to help a friend out.
Porting Ray was massive nightmare. I respect all open
source projects, But setting up ray on multiple cluster
does definelty trigger a normal humain being.

### Ray forces all remote nodes to have the same version of Python:
I am pretty sure there is sensible reason for backwards compatability.
Seriously just set it as a warning.

### F\*\*k off with your networking
Why in the f\*\*king hell is ray using 127.0.0.1 as the head node when I clearly set the public NAT traversed IP
from worker node.

I would rant more but it's a waste of time.


