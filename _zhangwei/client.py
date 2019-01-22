import socket
import cv2
import numpy
import time
import sys
from config import Config
 
def SendVideo():
	con = Config()
	host = con.get("server", "host")
	port = con.get("server", "port")
	
	address = (host, int(port))
	
	# address = ('10.18.96.207', 8002)
	try:
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	except socket.error as msg:
		print(msg)
		sys.exit(1)
		
	#建立图像读取对象
	capture = cv2.VideoCapture(0)
	#读取一帧图像，读取成功:ret=1 frame=读取到的一帧图像；读取失败:ret=0
	ret, frame = capture.read()
	#压缩参数，后面cv2.imencode将会用到，对于jpeg来说，15代表图像质量，越高代表图像质量越好为 0-100，默认95
	encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),15]
	
	while ret:
		#停止0.1S 防止发送过快服务的处理不过来，如果服务端的处理很多，那么应该加大这个值
		time.sleep(0.01)
		ret, frame = capture.read()
		
		s = frame.flatten().tostring()
		for i in range(20):
		    time.sleep(0.001)
		    sock.sendto(s[i*46080:(i+1)*46080]+str.encode(str(i).zfill(2)), address)

		# result, imgencode = cv2.imencode('.jpg', frame, encode_param)
		# data = numpy.array(imgencode)
		# stringData = data.tostring()
		
		# save data
		# cv2.imwrite('read video data.jpg', frame, encode_param)
		# show locally
		# cv2.imshow('read video data.jpg', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		# 读取服务器返回值
		# receive = sock.recvfrom(1024)
		# if len(receive): print(str(receive,encoding='utf-8'))
		# if cv2.waitKey(10) == 27: break
			
	capture.release()
	cv2.destroyAllWindows()
	sock.close();
	exit(404)

	
if __name__ == '__main__':
	SendVideo()
