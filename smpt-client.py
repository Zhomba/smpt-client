from socket import *
from base64 import *
import ssl

#prompt
userEmail = input("Enter your email: ")
userPassword = input("Enter your password: ")
userDestinationEmail = input("Enter Destination: ")
userSubject = input("Enter Subject: ")
userBody = input("Enter Message: ")


msg = '{}.\r\n !ENTER YOUR MESSAGE HERE!'.format(userBody)
endmsg = "\r\n.\r\n"

#Choose mail server and port
mailServer = 'smtp.gmail.com'
mailPort = 587

#Create socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailPort))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

#account authentication
strtlscmd = "STARTTLS\r\n".encode()
clientSocket.send(strtlscmd)
recv2 = clientSocket.recv(1024)

sslClientSocket = ssl.wrap_socket(clientSocket)

emailA = b64encode(userEmail.encode())
emailB = b64encode(userPassword.encode())

authorizationCMD = "AUTH LOGIN\r\n"

sslClientSocket.send(authorizationCMD.encode())
recv2 = sslClientSocket.recv(1024)
print(recv2)

sslClientSocket.send(emailA + "\r\n".encode())
recv3 = sslClientSocket.recv(1024)
print(recv3)

sslClientSocket.send(emailB + "\r\n".encode())
recv4 = sslClientSocket.recv(1024)
print(recv4)

#send mail from command and print server response
mailFrom = "Mail from: <{}>\r\n".format(userDestinationEmail)
sslClientSocket.send(mailFrom.encode())
recv5 = sslClientSocket.recv(1024)
print(recv5)

#send RCPT TO command and print response
rcptto = "RCPT TO: <{}>\r\n".format(userDestinationEmail)
sslClientSocket.send(rcptto.encode())
recv6 = sslClientSocket.recv(1024)
print(recv6)

#send DATA command
data = 'DATA\r\n'
sslClientSocket.send(data.encode())
recv7 = sslClientSocket.recv(1024)
print(recv7)

#send message data
sslClientSocket.send("Subject: {}\n\n{}".format(userSubject, msg).encode())

#message ends with a single period
sslClientSocket.send(endmsg.encode())
recv8 = sslClientSocket.recv(1024)
print(recv8)

#send QUIT command and get response
quitCMD = 'QUIT\r\n'
sslClientSocket.send(quitCMD.encode())
recv9 = sslClientSocket.recv(1024)
print(recv9)

sslClientSocket.close()
print('Success')