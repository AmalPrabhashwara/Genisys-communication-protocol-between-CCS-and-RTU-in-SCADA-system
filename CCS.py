import socket
import tkinter  # package for creating thr GUI
import threading
from time import sleep
a=0


def TakeRecallAck(): # Receiving acknowledgement for Recall message and indicating the current state of the RTU in the CCS.
    Recall_Ack = c.recv(1024).decode()
    global a
    if Recall_Ack == Recall_Ack_for_v1_on:
        print("Receiving the Ack for Recall message ")
        l1.configure(text="V1 ON", bg='red')  # Indicating V1 on
    if Recall_Ack == Recall_Ack_for_v1_off:
        print("Receiving the Ack for Recall message ")
        l1.configure(text="V1 OFF", bg='green')  # Indicating V1 off
    if Recall_Ack == Recall_Ack_for_p1_on:
        print("Receiving the Ack for Recall message ")
        l2.configure(text="P1 ON", bg='red')  # Indicating p1 on
    if Recall_Ack == Recall_Ack_for_p1_off:
        print("Receiving the Ack for Recall message ")
        l2.configure(text="P1 OFF", bg='green')  # Indicating p1 off
    if Recall_Ack == Recall_Ack_for_v2_on:
        print("Receiving the Ack for Recall message ")
        l3.configure(text="V2 ON", bg='red')  # Indicating V2 on
    if Recall_Ack == Recall_Ack_for_v2_off:
        print("Receiving the Ack for Recall message ")
        l3.configure(text="V2 OFF", bg='green')  # Indicating V2 off
    if Recall_Ack == Recall_Ack_for_p2_on:
        print("Receiving the Ack for Recall message ")
        l4.configure(text="P2 ON", bg='red')  # Indicating p2 on
    if Recall_Ack == Recall_Ack_for_p2_off:
        print("Receiving the Ack for Recall message ")
        l4.configure(text="P2 OFF", bg='green')  # Indicating p2 off
    if Recall_Ack == Recall_Ack_for_M1_on:
        print("Receiving the Ack for Recall message ")
        l5.configure(text="M1 ON", bg='red')  # Indicating M1 on
        a = 1  # set a to 1 if M1 is on

    if Recall_Ack == Recall_Ack_for_M2_on:
        print("Receiving the Ack for Recall message ")
        l6.configure(text="M2 ON", bg='red')
        a = 2  # set variable 'a' to 2 if M2 is on

    # here variable 'a' shows the motor which was turned on first.

    if Recall_Ack == Recall_Ack_for_M1andM2_on:
        print("Receiving the Ack for Recall message ")
        if a == 1:  # here variable 'a' equals to 1 means M1 has been been already turned on.
            l6.configure(text="M2 ON", bg='red')  # Next it need to indicate M2 on only.
        if a == 2: # here variable 'a' equals to 2 means M2 has been been already turned on.
            l5.configure(text="M1 ON", bg='red')  # Next it need to indicate M1 on only.
        x = 0
        while True:  # wait for recall acknowledgement message which is all motors turned off.
            sleep(2)
            c.send(bytes(Recall_m, 'utf-8'))
            print("Send the Recall message")
            message = c.recv(1024).decode()
            # repply=threading.Thread(target=TakeReply(b)).start()
            if (message == Recall_Ack_for_M1_off) & (x == 0):
                print("Receiving he Ack for Recall message ")
                l5.configure(text="M1 OFF", bg='green')
                l6.configure(text="M2 OFF", bg='green')
                x = 1
            if message == Recall_Ack_for_v3_on:
                print("Receiving the Ack for Recall message ")
                l7.configure(text="V3 ON", bg='red')
                a=0
                break

    if Recall_Ack == Recall_Ack_for_M1_off:
        print("Receiving the Ack for Recall message ")
        l5.configure(text="M1 OFF", bg='green')

    if Recall_Ack == Recall_Ack_for_M2_off:
        print("Receiving the Ack for Recall message ")
        l6.configure(text="M2 OFF", bg='green')

    if Recall_Ack == Recall_Ack_for_v3_off:
        print("Receiving the Ack for Recall message ")
        l7.configure(text="V3 OFF", bg='green')


def TakeControlAck():  # Receiving acknowledgement message for control message and once acknowledgement comes sending the recall message
    message = c.recv(1024).decode()
    if message == Positive_Control_Ack:
        print("Receiving the Positive ack for control message")
        z = Recall_m
        c.send(bytes(z, 'utf-8'))
        print("Send the Recall message")
        threading.Thread(target=TakeRecallAck).start()
    if message == Negetive_Control_Ack:
        print("Receiving the Negative ack for control message")


def TakePollAck(control_message):  # Receiving acknowledgement message for polling message and once acknowledgement comes sending the control message
    received_message = c.recv(1024).decode()
    if received_message == Polling_Ack:
        print("Receiving the Ack for polling message ")
        c.send(bytes(control_message, 'utf-8'))
        print("Sending the Control message ")


def SendPollingMessage(control_message):   # sending polling message
    c.send(bytes(Polling_m, 'utf-8'))
    print("Send the polling message")
    threading.Thread(target=TakePollAck(control_message)).start()


def OnClick(control_message):  # Sending messages once control button are pressed in CCS.
    threading.Thread(target=SendPollingMessage(control_message)).start()
    threading.Thread(target=TakeControlAck).start()


# Initializing types of messages
Polling_m = "11111011 00001100 00000101 11111111 00000000 11111111 11111111 11110110"
Polling_Ack = '11110001 00001100 00000101 11111111 00000001 1111111 11111111 11110110'

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

Positive_Control_Ack='11110001 00001100 00000101 11111111 00000010 1111111 11111111 11110110'
Negetive_Control_Ack='11110001 00001100 00000101 11111111 00000100 1111111 11111111 11110110'

Recall_m = '11110010 00001100 00000101 11111111 00000000 11111111 11111111 11110110'

Recall_Ack_for_v1_on='11110001 00001100 00000101'+'00100101 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_v1_off='11110001 00001100 00000101'+'00010101 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_p1_on='11110001 00001100 00000101'+'00100101 10010101'+'111111111 11111111 11110110'
Recall_Ack_for_p1_off='11110001 00001100 00000101'+'00100101 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_v2_on='11110001 00001100 00000101'+'00011001 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_v2_off='11110001 00001100 00000101'+'00010101 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_p2_on='11110001 00001100 00000101'+'00011001 01100101'+'111111111 11111111 11110110'
Recall_Ack_for_p2_off='11110001 00001100 00000101'+'00011001 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_M1_on='11110001 00001100 00000101'+'00010101 01011001'+'111111111 11111111 11110110'
Recall_Ack_for_M1_off='11110001 00001100 00000101'+'00010101 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_M2_on='11110001 00001100 00000101'+'00010101 01010110'+'111111111 11111111 11110110'
Recall_Ack_for_M2_off='11110001 00001100 00000101'+'00010101 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_v3_on='11110001 00001100 00000101'+'00010110 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_v3_off='11110001 00001100 00000101'+'00010101 01010101'+'111111111 11111111 11110110'
Recall_Ack_for_M1andM2_on='11110001 00001100 00000101'+'00010101 01011010'+'111111111 11111111 11110110'

# Creating socket and waiting for client to connect with server.
s = socket.socket()
print("Socket successfully created")
port = 9999
s.bind(('localhost', port))
print("socket binded to")
s.listen(5)
print("socket is listening")

c, addr = s.accept()
print('Got connection from', addr)

# Building the GUI for CCS including all controlling buttons and other indication labels
window = tkinter.Tk()
window.title("GUI")
window.geometry('1200x300')
label = tkinter.Label(window, text="CCS", font=("Arial Bold", 20)).pack()
V1on = tkinter.Button(window, text="V1 On", width=8, height=2, fg="green", activebackground="red", command=lambda: OnClick(v1_on_control_message)).place(x=20, y=50)
V1off = tkinter.Button(window, text="V1 Off", width=8, height=2, fg="red", activebackground="red", command=lambda: OnClick(v1_off_control_message)).place(x=90, y=50)
P1on = tkinter.Button(window, text="P1 On", width=8, height=2, fg="green", activebackground="red", command=lambda: OnClick(p1_on_control_message)).place(x=190, y=50)
P1off = tkinter.Button(window, text="P1 Off", width=8, height=2, fg="red", activebackground="red", command=lambda: OnClick(p1_off_control_message)).place(x=260, y=50)
V2on = tkinter.Button(window, text="V2 On", width=8, height=2, fg="green", activebackground="red", command=lambda: OnClick(v2_on_control_message)).place(x=360, y=50)
V2off = tkinter.Button(window, text="V2 Off", width=8, height=2, fg="red", activebackground="red", command=lambda: OnClick(v2_off_control_message)).place(x=430, y=50)
P2on = tkinter.Button(window, text="P2 On", width=8, height=2, fg="green", activebackground="red", command=lambda: OnClick(p2_on_control_message)).place(x=530, y=50)
P2off = tkinter.Button(window, text="P2 Off", width=8, height=2, fg="red", activebackground="red", command=lambda: OnClick(p2_off_control_message)).place(x=600, y=50)
M1on = tkinter.Button(window, text="M1 On", width=8, height=2, fg="green", activebackground="red", command=lambda: OnClick(m1_on_control_message)).place(x=700, y=50)
M1off = tkinter.Button(window, text="M1 Off", width=8, height=2, fg="red", activebackground="red", command=lambda: OnClick(m1_off_control_message)).place(x=770, y=50)
M2on = tkinter.Button(window, text="M2 On", width=8, height=2, fg="green", activebackground="red", command=lambda: OnClick(m2_on_control_message)).place(x=870, y=50)
M2off = tkinter.Button(window, text="M2 Off", width=8, height=2, fg="red", activebackground="red", command=lambda: OnClick(m2_off_control_message)).place(x=930, y=50)
V3on = tkinter.Button(window, text="V3 On", width=8, height=2, fg="green", activebackground="red", command=lambda: OnClick(v3_on_control_message)).place(x=1030, y=50)
V3off = tkinter.Button(window, text="V3 Off", width=8, height=2, fg="red", activebackground="red", command=lambda: OnClick(v3_off_control_message)).place(x=1090, y=50)

l1 = tkinter.Label(window, text="V1 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l2 = tkinter.Label(window, text="P1 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l3 = tkinter.Label(window, text="V2 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l4 = tkinter.Label(window, text="P2 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l5 = tkinter.Label(window, text="M1 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l6 = tkinter.Label(window, text="M2 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l7 = tkinter.Label(window, text="V3 off", width=8, height=2, font=("Arial Bold", 10), bg='green')
l1.place(x=200, y=150)
l2.place(x=300, y=150)
l3.place(x=400, y=150)
l4.place(x=500, y=150)
l5.place(x=600, y=150)
l6.place(x=700, y=150)
l7.place(x=800, y=150)

window.mainloop()








