# Credentials Folder

## The purpose of this folder is to store all credentials needed to log into your server and databases. This is important for many reasons. But the two most important reasons is
    1. Grading , servers and databases will be logged into to check code and functionality of application. Not changes will be unless directed and coordinated with the team.
    2. Help. If a class TA or class CTO needs to help a team with an issue, this folder will help facilitate this giving the TA or CTO all needed info AND instructions for logging into your team's server. 


# Below is a list of items required. Missing items will causes points to be deducted from multiple milestone submissions.

1. Server URL or IP: 
   Server IPv4 DNS for login: ec2-18-223-160-96.us-east-2.compute.amazonaws.com
   Server IP to get to website: http://18.223.160.96:5000/ (HTTPS not enabled in NGINX)
2. SSH username: ubuntu
3. SSH password or key.(Key inside credentials folder)
    <br> If a ssh key is used please upload the key to the credentials folder.
4. Database URL or IP and port used.
    <br><strong> NOTE THIS DOES NOT MEAN YOUR DATABASE NEEDS A PUBLIC FACING PORT.</strong> But knowing the IP and port number will help with SSH tunneling into the database. The default port is more than sufficient for this class.
5. Database username: team1
6. Database password: 12345678
7. Database name (basically the name that contains all your tables)
8. Instructions on how to use the above information.

Command to make pem key accessible: sudo chmod 400 ./team2.pem

Command to start server: ssh -i "team2.pem" ubuntu@ec2-18-223-160-96.us-east-2.compute.amazonaws.com

URL: http://18.223.160.96:5000/ (No https!)

To access mysql: mysql -u team1 -p

Password: 12345678


# Most important things to Remember
## These values need to kept update to date throughout the semester. <br>
## <strong>Failure to do so will result it points be deducted from milestone submissions.</strong><br>
## You may store the most of the above in this README.md file. DO NOT Store the SSH key or any keys in this README.md file.
