import socket
from time import sleep
import threading
import tkinter
N=15  # 15 seconds for N
R=5  # 5 seconds for R
Current_state = '00010101 01010101'  # stores the current state of the RTU.
CheckWaterInTank = 0  # Indicate the water in tank


def callTime():  # calling time which the motors should be keep on and to V3 on
    global Current_state
    sleep(N)  # wait for N seconds
    Current_state = '00010101 01010101'  # once N seconds gone change the current state which all motors were turned off
    l5.configure(text="M1 OFF", bg='green')
    l6.configure(text="M2 OFF", bg='green')
    sleep(R)  # wait for R seconds
    Current_state = '00010110 01010101'  # once R seconds gone stores the current state which the V3 is turned on
    l7.configure(text="V3 ON", bg='red')  # indicates that v3 turned on


def Find_Recall_Ack(x):  # preparing the recall acknowledgement message which shows the current state of the RTU.
    m='11110001 00001100 00000101'+x+'111111111 11111111 11110110'
    return m


def Received_All_Messages():  # Here all the  messages received by the RTU are identified and sending proper acknowledgement messages.
    while True:
        global Current_state
        global CheckWaterInTank
        sleep(1)
        received_message = c.recv(1024).decode()
        if received_message == Polling_message:
            message = Polling_Ack
            print('sending pol ack')
            c.send(bytes(message, "utf-8"))

        elif received_message == Recall_message:
            Recall_Ack = Find_Recall_Ack(Current_state)
            message = Recall_Ack
            print('sending Recall ack')
            c.send(bytes(message, "utf-8"))

        elif received_message == v1_on_control_message:  # v1 on
            if Current_state == '00010101 01010101':
                Current_state = '00100101 01010101'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l1.configure(text="V1 ON", bg='red')
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == v1_off_control_message:  #v1 off
            if Current_state == '00100101 01010101':
                Current_state = '00010101 01010101'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l1.configure(text="V1 OFF", bg='green')
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == p1_on_control_message:    #p1 on
            if Current_state == '00100101 01010101':
                Current_state = '00100101 10010101'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l2.configure(text="P1 ON", bg='red')
                CheckWaterInTank = CheckWaterInTank + 1
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == p1_off_control_message:  # p1 off
            if Current_state == '00100101 10010101':
                Current_state = '00100101 01010101'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l2.configure(text="P1 OFF", bg='green')
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == v2_on_control_message:  # v2 on
            if Current_state == '00010101 01010101':
                Current_state = '00011001 01010101'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l3.configure(text="V2 ON", bg='red')
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == v2_off_control_message:  # v2 off
            if Current_state == '00011001 01010101':
                Current_state = '00010101 01010101'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l3.configure(text="V2 OFF", bg='green')
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == p2_on_control_message:  # p2 on
            if Current_state == '00011001 01010101':
                Current_state = '00011001 01100101'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l4.configure(text="P2 ON", bg='red')
                CheckWaterInTank=CheckWaterInTank+1
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == p2_off_control_message:  # p2 off
            if Current_state == '00011001 01100101':
                Current_state = '00011001 01010101'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l4.configure(text="P2 OFF", bg='green')
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == m1_on_control_message:  # M1 oN
            if (Current_state == '00010101 01010101') & (CheckWaterInTank >= 2):  # Motors will be turned on if and only waters in the tankes(Ensure pumps has been already functioned before the motors).
                Current_state = '00010101 01011001'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l5.configure(text="M1 ON", bg='red')
            elif (Current_state == '00010101 01010110') & (CheckWaterInTank >= 2):
                Current_state = '00010101 01011010'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l5.configure(text="M1 ON", bg='red')
                threading.Thread(target=callTime).start()
                #CheckWaterInTank =0
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == m2_on_control_message:  # M2 ON
            if (Current_state == '00010101 01010101') & (CheckWaterInTank >= 2):
                Current_state = '00010101 01010110'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l6.configure(text="M2 ON", bg='red')
            elif (Current_state == '00010101 01011001') & (CheckWaterInTank >= 2):
                Current_state = '00010101 01011010'
                message = Positive_Control_Ack
                print('sending Positive Control ack')
                c.send(bytes(message, "utf-8"))
                l6.configure(text="M2 ON", bg='red')
                threading.Thread(target=callTime).start()
                #CheckWaterInTank = 0
            else:
                message = Negetive_Control_Ack
                print('sending Negetive Control ack')
                c.send(bytes(message, "utf-8"))

        elif received_message == v3_off_control_message:  # v3 off
           if Current_state == '00010110 01010101':
               Current_state = '00010101 01010101'
               message = Positive_Control_Ack
               print('sending Positive Control ack')
               c.send(bytes(message, "utf-8"))
               l7.configure(text="V3 OFF", bg='green')
               CheckWaterInTank = 0  # V3 remove water in tank. So CheckWaterInTank should set to zero.
           else:
               message = Negetive_Control_Ack
               print('sending Negetive Control ack')
               c.send(bytes(message, "utf-8"))
        else:
            message = Negetive_Control_Ack
            print('sending Negetive Control ack')
            c.send(bytes(message, "utf-8"))


# initializing all messages
Polling_message = "11111011 00001100 00000101 11111111 00000000 11111111 11111111 11110110"

v1_on_control_message = "11110011 00001100 00000101 00100000 00000000 11111111 11111111 11110110"
v1_off_control_message = "11110011 00001100 00000101 00010000 00000000 11111111 11111111 11110110"
p1_on_control_message = "11110011 00001100 00000101 00000000 10000000 11111111 11111111 11110110"
p1_off_control_message = "11110011 00001100 00000101 00000000 01000000 11111111 11111111 11110110"
v2_on_control_message = "11110011 00001100 00000101 00001000 00000000 11111111 11111111 11110110"
v2_off_control_message = "11110011 00001100 00000101 00000100 00000000 11111111 11111111 11110110"
p2_on_control_message = "11110011 00001100 00000101 00000000 00100000 11111111 11111111 11110110"
p2_off_control_message = "11110011 00001100 00000101 00000000 00010000 11111111 11111111 11110110"
m1_on_control_message = "11110011 00001100 00000101 00000000 00001000 11111111 11111111 11110110"
m1_off_control_message = "11110011 00001100 00000101 00000000 00000100 11111111 11111111 11110110"
m2_on_control_message = "11110011 00001100 00000101 00000000 00000010 11111111 11111111 11110110"
m2_off_control_message = "11110011 00001100 00000101 00000000 00000001 11111111 11111111 11110110"
v3_on_control_message = "11110011 00001100 00000101 00000010 00000000 11111111 11111111 11110110"
v3_off_control_message = "11110011 00001100 00000101 00000001 00000000 11111111 11111111 11110110"

Recall_message = '11110010 00001100 00000101 11111111 00000000 11111111 11111111 11110110'

Polling_Ack='11110001 00001100 00000101 11111111 00000001 1111111 11111111 11110110'
Positive_Control_Ack='11110001 00001100 00000101 11111111 00000010 1111111 11111111 11110110'
Negetive_Control_Ack='11110001 00001100 00000101 11111111 00000100 1111111 11111111 11110110'

# Create a socket object
c = socket.socket()
# Define the port on which you want to connect
port =9999
# connect to the server on local computer

c.connect(('localhost', port))

threading.Thread(target=Received_All_Messages).start()

# Creating the GUI for RTU.
window = tkinter.Tk()
window.title("GUI")
window.geometry('160x350')
label = tkinter.Label(window, text="RTU",  font=("Arial Bold", 20)).pack()
l1 = tkinter.Label(window, text="V1 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l2 = tkinter.Label(window, text="P1 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l3 = tkinter.Label(window, text="V2 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l4 = tkinter.Label(window, text="P2 off ", width=8, height=2, font=("Arial Bold", 10), bg='green')
l5 = tkinter.Label(window, text="M1 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l6 = tkinter.Label(window, text="M2 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l7 = tkinter.Label(window, text="V3 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l1.place(x=40, y=40)
l2.place(x=40, y=80)
l3.place(x=40, y=120)
l4.place(x=40, y=160)
l5.place(x=40, y=200)
l6.place(x=40, y=240)
l7.place(x=40, y=280)

window.mainloop()


