from ctypes import *
from ctypes import cdll
import ray
import json
import time
import subprocess
import os
import atexit



# Class to create string to pass as string function 
# parameter to shared object file
class go_string(Structure):
    _fields_ = [
    ("p", c_char_p),
    ("n", c_int)]

def P2PRCMappingRay(port=""):

    # Local Port intended to be escaped outside NAT
    # Converting to the appropirate datatype to be
    # passed as a string to GoLang.
    b = go_string(c_char_p(port.encode('utf-8')), len(port))

    # Defining the response type of the GoLang function 
    # function
    p2prc.MapPort.restype = c_char_p
    # Calling the Go function
    address = p2prc.MapPort(b)
    res = str(address).strip("b'")
    return res

# Start P2PRC Container 
def StartContainer(ip=""):
    ipAddr = go_string(c_char_p(ip.encode('utf-8')), len(ip))
    # Defining the response type of the GoLang function 
    # function
    p2prc.StartContainer.restype = c_char_p
    # Calling the Go function
    res = p2prc.StartContainer(ipAddr)
    return str(res).strip("b'")

# Setup sample Ray worker Node and connect it to 
# the Ray head node
def SetupRayWorker(HeadNode="", ServerIP="", ServerPort=""):
    print(HeadNode + " " + ServerPort)
    # Setup Ray worker node on the Docker container and connect 
    # it to the head node.
    subprocess.call(["sh","setup_ray_worker.sh",ServerIP,ServerPort, HeadNode])




# Load P2PRC shared object files
p2prc = cdll.LoadLibrary("SharedOBjects/p2prc.so")

# Initialise P2PRC 
p2prc.Init("")

# # Initialise ray
# ray.init(dashboard_port=2301)

subprocess.call(["ray", "start","--head","--dashboard-port", "2301","--port","5801"])

# Map Port for Ray dashboard
Dashboard = P2PRCMappingRay(port="2301")

print(Dashboard)

headNode = P2PRCMappingRay(port="5801")

print(headNode)

# View IP Table information 
p2prc.ViewIPTable.restype = c_char_p
ipTable = p2prc.ViewIPTable()
# View IP Table as 
ipTableObject = json.loads((str(ipTable).strip("b'")))

# Start P2PRC as a server mode 
# Add local node as a part of 
# of the test network 
p2prc.Server()

time.sleep(5)


for node in ipTableObject["ip_address"]: 
    # Start Ray on all Nodes except the root node
    # For testing reasons (Note this is not true orchestration)
    ContainerResponse = StartContainer(ip="0.0.0.0" + ":" + "8088")
    Container = json.loads(ContainerResponse)
    # Parse response
    for port in Container["Ports"]["Port"]:
        if port["PortName"] == "SSH":
            SetupRayWorker(ServerIP="0.0.0.0",ServerPort=str(port["ExternalPort"]),HeadNode=headNode)

# Run Ray sample program 
# Ex: RAY_ADDRESS='http://139.59.162.154:54792' ray job submit -- python sample_ray_program.py
# os.environ["RAY_ADDRESS"] = "http://" + res
# subprocess.call(["ray","job", "submit", "--", "python", "sample_ray_program.py"])




# Run infinelty as a foreground process unless 
# killed by the user.
def StallLoop():
    for _ in iter(int, 1):
        pass

StallLoop()

# Exit handler to kill ray
def exit_handler():
    print("exit handler triggered to stop Ray processes")
    subprocess.call(["ray","stop"])

atexit.register(exit_handler)