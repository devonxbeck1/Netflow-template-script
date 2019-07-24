from ciscoconfparse import CiscoConfParse
import time
from netmiko import ConnectHandler


# Declare netmiko variables and netmiko dictionary


device = { 
    'device_type': 'cisco_ios_telnet',
    'ip': "19.211.82.17",
    'username': 'dbeck51',
    'password': 'Thematrix123!',
    'secret' :  'Thematrix123!'
} 

net_connect = ConnectHandler(**device)
net_connect.enable()
output = net_connect.send_command('show run')
fileconf = open("conffile.txt", "w+")
file2 = fileconf.write(output) 
print(output) 

# Declare CiscoConfParse variables
parse = CiscoConfParse("conffile.txt")
all_ints = parse.find_objects("^interf")
flowmon = parse.find_objects("^flow monitor")
nf_ints = list()
hostname = parse.re_match_iter_typed(r'^hostname\s+(\S+)', default='')



# loop that finds interfaces with netflow and appends to list
for faces in all_ints:
    if faces.re_search_children(r"ip flow monitor") or faces.re_search_children(r"flow ipv4 monitor"):
        nf_ints.append(faces)
        #adds title using hostnames
    with open("nftemplate.txt",'w+') as f:
     f.write(">>Reconfiguring Netflow on routers" + " " + hostname)
     f.write("\n")
     f.write("\n")
     f.write("""*************
**%s**
************* """ % hostname)
     f.write("\n")
     f.write("\n")
     f.write("\n")   
     f.write("Step1> Remove netflow from interfaces\n")
     f.write("*************************************************************\n")
     for item in nf_ints:
        f.write("%s\n" % item.text)
        f.write(" no ip flow monitor FlowMonitorv9 input\n")
    with open("nftemplate.txt",'a') as f:
        f.write("\n")
        f.write("Step2> Update flow monitor cache timeout and cache entries\n")
        f.write("***************************************************\n")
        f.write("\n")
        f.write("!\n")
        f.write("flow monitor FlowMonitorv9\n")
        f.write(" cache timeout inactive 15\n")
        f.write(" cache entries 800000\n")
        f.write("!\n")
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("Step3> Add netflow to interfaces\n")
        f.write("*************************************************************\n")
        f.write("\n")
    with open("nftemplate.txt",'a') as f:
        for item in nf_ints:
         f.write("%s\n" % item.text)
         f.write(" ip flow monitor FlowMonitorv9 input\n")
          
    
        
    
    

# opens template file and writes the interfaces to the file
