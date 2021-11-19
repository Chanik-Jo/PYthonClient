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

class socketMsg:
    nickname="익명"
    message="없음"
    mode=0
    '''
    normal send Msg 1
    log in  2
    log out 3    
    '''


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
        #알고싶은건 클래스도 ENCODE로 전송이 가능한가 에 있다.


def recvMsg():
    recvMsgSizeLoop=True
    recvMsgSize =-1
    recvMsg=False
    print('recv msg thread on')
    while recvMsgSizeLoop:
        recvMsgSize = clientSock.recv(10)#원리는 서버와 같다. 10자리면 용량 한계를 거의 100억단위로 표시 가능하고,
        #사실상 10기가 까지는 표기하고 전송가능하다.
        recvMsgSize = recvMsgSize.decode('utf-8')
        if (recvMsgSize.isdecimal()):#올바르게 숫자크기값 이 돌아왔는지 확인합니다.
            print("data size returned", recvMsgSize)

            recvMsgSize=int(recvMsgSize)#이거 안해줬다가 str고쳐달라고 오류 나온다.

            recvMsg = clientSock.recv(recvMsgSize)#아까 받아온 사이즈를 기반으로 수신한다.
            print("받은 데이터는 ",recvMsg.decode('utf-8'))






if __name__ == "__main__":
    # 여기는 클라이언트 입니다.
    recvThread = threading.Thread(target=recvMsg, args=())
    sendThread = threading.Thread(target=sendMsg, args=())
    recvThread.start()
    sendThread.start()







