from socket import *
from struct import pack
import threading

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080))


#data.decode('utf-8')

#messageByteCnt.encode('utf-8')

#clientSock.send(message)

# 수신시  : 크기전송 -> 실제전송
# 송신시  : 크기수신 -

def utf8len(s):#utf-8 형태의 바이트 갯수를 반환합니다.
    return len(s.encode('utf-8'))

def sendMsg():
    while True:
        msg = input("input message you want to send\n")
        msgLen=utf8len(msg)
        print("message length utf-8 ",msgLen)

        clientSock.send(str(msgLen).encode('utf-8'))
        print("send real message ")
        #0.3초 기다렸다가 보낼까 말까 싶다. 상대방 PC에서 통신이 밀릴수도 있으니.
        clientSock.send(msg.encode('utf-8'))


def recvMsg():
    recvMsgSizeLoop=True
    recvMsgSize =-1
    recvMsg=False
    print('recv msg thread on')
    while recvMsgSizeLoop: #제일먼저 메세지의 길이를 수신받습니다.
        # 어짜피 단일 파일이 1바이트(int를 환산시 2기가)를 넘을
        #가능성은 사실상 없으니, 1바이트만으로도 수신데이터의 사이즈를 가늠하기에는 충분합니다.

        # data = data+ connectionSock.recv(2).decode('utf-8')
        recvMsgSize = clientSock.recv(1024)#일바이트의 길이(숫자)를 수신합니다.  2억가지는 되니 상관없겠지.

        if (recvMsgSize.decode('utf-8').isdecimal()):#올바르게 숫자값이 돌아왔는지 확인합니다.
            print("data size returned", recvMsgSize)
            recvMsgSizeLoop = False
            recvMsgSize=int(recvMsgSize.decode('utf-8'))

            recvMsg = clientSock.recv(recvMsgSize)#아까 받아온 사이즈를 기반으로 수신한다.
            print(recvMsg.decode('utf-8'))






if __name__ == "__main__":
    # 여기는 클라이언트 입니다.
    recvThread = threading.Thread(target=recvMsg, args=())
    sendThread = threading.Thread(target=sendMsg, args=())
    recvThread.start()
    sendThread.start()







