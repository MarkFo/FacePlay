from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from FacePlay.models import Student, Teacher, C_S, Course, Photo
import os, base64
import datetime
import numpy as np
# 关闭以提高速度
# import main

IMG_base64 = None
upload_cnt = 0
# Create your views here.
def index(request):
	# if request.method == 'POST':
	# 	email = request.POST.get('lg_email')
	# 	password = request.POST.get('lg_password')
	# 	try:
	# 		user = USER.objects.get(email=email)
	# 		# print(user.password)
	# 		if user.password == password:
	# 			print("#### 登录用户 —— 邮箱：%s 密码：%s\n" % (email, password))
	# 			request.session["name"] = user.name
	# 			return render(request, 'index.html', {'name': user.name})
	# 		return render(request, 'login.html', {"login_msg": "alert('用户不存在或密码错误,请重试!')"})
	# 	except:
	# 		return render(request, 'login.html', {"login_msg": "alert('用户不存在或密码错误,请重试!')"})
	# else:
	# 网站验证暂时关闭
	# if "name" not in request.session.keys():
	# 	return render(request, 'login.html')
	# else:
	# 	print("#### 用户刷新界面")
	return render(request, 'index.html', {'name': request.session["name"]})

def student(request):
	return render(request, 'student.html', {'name': request.session["name"]})

def login(request):
	return render(request, 'login.html')


def forgot(request):
	return render(request, 'forgot-password.html')


def register(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		tel = request.POST.get('tel')
		ID = request.POST.get('id')
		password = request.POST.get('password')
		face_base64 = request.POST.get('upload_img').split(',')[1]  # 获取base64编码
		imgdata = base64.b64decode(face_base64)  # 解码
		try:
			os.mkdir('FACEs/' + ID)
		except:
			pass
		now = datetime.datetime.now()
		# cv2无法读取'-'和中文
		register_time = str(now).split()[0].replace("-", '')
		file = open('FACEs/' + ID + '/' + tel + '.png', 'wb')  # 保存为[时间].png的图片
		file.write(imgdata)
		file.close()
		print("### " + str(now) + " SAVE A FACE IMAGE")
		print("#### 新注册用户 —— 姓名：%s ID：%s 密码：%s\n" % (name, id, password))
		if ID[0] == '2':
			new_user = Student()
			new_user.s_id = ID
			new_user.s_name = name
			new_user.s_tel = tel
			new_user.s_pwd = password
			new_user.s_face = "FACEs/" + ID + '/' + tel + '.png'
		else:
			new_user = Teacher()
			new_user.t_id = ID
			new_user.t_name = name
			new_user.t_tel = tel
			new_user.t_pwd = password
			new_user.t_face = "FACEs/" + ID + '/' + tel + '.png'
		new_user.save()
		request.session["name"] = name
		if ID[0] == '2':
			return render(request, 'student.html', {'name': name})
		else:
			return render(request, 'index.html', {'name': name})
	else:
		return render(request, 'register.html')

# Not use
def upload(request):
	if request.method == 'POST':
		strs = request.POST.get('upload_img').split(',')[1]  # 获取base64编码
		imgdata = base64.b64decode(strs)  # 解码
		now = datetime.datetime.now()
		file = open('face_tmp.png', 'wb')  # 保存为face_tmp.png的图片
		file.write(imgdata)
		file.close()
		print("### " + str(now) + " SAVE A IMAGE")
		# main.test(srcimg='face_tmp.png')

		# pimg = Image.open('0.png')  # 获取图片
		# cv2.namedWindow("Image")  # 创建窗口
		# cv2.imshow("Image", pimg)  # 显示图片
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
	return render(request, 'index.html')

def identify_face(request):
	global IMG_base64
	if request.method == 'POST':
		image_base64 = request.POST.get('image_base64')
		img_strs = image_base64.split(',')[1]
		imgdata = base64.b64decode(img_strs)  # 解码
		now = datetime.datetime.now()
		file = open('face_tmp.png', 'wb')  # 保存为face_tmp.png的图片
		file.write(imgdata)
		file.close()
		print("### " + str(now) + " SAVE A IMAGE")
		# print(type(img_strs))
		face_image_base64 = main.get_face(img_strs)
		face_identify = False
		is_face = True
		if face_image_base64 is None:
			is_face = False
		else:
			# print(type(face_image_base64))
			image_base64 = "data:image/png;base64," + face_image_base64
			IMG_base64 = image_base64
		no_face_show = entry_show = strange_face_show = face_show = 'none'
		if not is_face:
			no_face_show = "display"
		else:
			process_show = "block"
			face_show = "block"
			# 检测到人脸后进行识别，不重复发送
			# face_name = main.identfiy_all(origin_img='face_tmp.png')
			# if face_name:
			# 	face_identify = True
			# if not face_identify:
			# 	strange_face_show = "block"
			# else:
			# 	entry_show = "block"
		# print(no_face_show, entry_show, strange_face_show, face_show)
		return render(request, 'face.html', locals())
	else:
		return render(request, "face.html")

def face_result(request):
	if request.method == 'POST':
		image_base64 = IMG_base64
		face_identify = False
		no_face_show = entry_show = strange_face_show = face_show = 'none'
		face_show = "block"
		face_name = main.identfiy_all(origin_img='face_tmp.png')
		process_show = "none"
		if face_name:
			face_identify = True
		if not face_identify:
			strange_face_show = "block"
		else:
			entry_show = "block"
		# print(no_face_show, entry_show, strange_face_show, face_show)
		return render(request, 'face.html', locals())
	else:
		return render(request, "face.html")

def login_check(request):
	ID = request.POST.get('lg_id')
	password = request.POST.get('lg_pwd')
	print(ID + " " + password)

	try:
		if ID[0] == '1':
			user = Teacher.objects.get(t_id=ID)
			pwd = user.t_pwd
			name = user.t_name
		else:
			user = Student.objects.get(s_id=ID)
			pwd = user.s_pwd
			name = user.s_name
		# print(user.password)
		if pwd == password:
			print("#### 登录用户 —— ID：%s 密码：%s\n" % (ID, password))
			request.session["name"] = name
			print("登陆进去")
			# bug
			if ID[0] == '2':
				return render(request, 'student.html', {'name': name})
			else:
				return render(request, 'index.html', {'name': name})
		return render(request, 'login_unsuccess.html')
	except:
		return render(request, 'login_unsuccess.html')

def charts(request):
	return render(request, 'class_info.html')

def record(request):
	if not os.path.exists('imgs.npy'):
		imgs = []
		for i in range(1, 6):
			try:
				with open('Recognition/' + str(i) + '.jpg', "rb") as f:
					base64_data = base64.b64encode(f.read())
				base64_data = str(base64_data, encoding="utf-8")
				image_base64 = "data:image/png;base64," + base64_data
				imgs.append(image_base64)
			except:
				pass
		np.save('imgs.npy', imgs)
	else:
		imgs = np.load('imgs.npy')
	try:
		imgs = imgs.tolist()
	except:
		pass
	if len(imgs) < 5:
		for i in range(5 - len(imgs)):
			imgs.append('')
	return render(request, 'record.html', {'img_1': imgs[0], 'img_2': imgs[1],'img_3': imgs[2],'img_4': imgs[3],'img_5': imgs[4],})

def message(request):
	return render(request, 'message.html')

def read_record(request):
	if not os.path.exists('imgs.npy'):
		imgs = []
		for i in range(1, 6):
			try:
				with open('Recognition/' + str(i) + '.jpg', "rb") as f:
					base64_data = base64.b64encode(f.read())
				base64_data = str(base64_data, encoding="utf-8")
				image_base64 = "data:image/png;base64," + base64_data
				imgs.append(image_base64)
			except:
				pass
		np.save('imgs.npy', imgs)
	else:
		imgs = np.load('imgs.npy')
	try:
		imgs = imgs.tolist()
	except:
		pass
	if len(imgs) < 5:
		for i in range(5 - len(imgs)):
			imgs.append('')
	return render(request, 'read_record.html', {'img_1': imgs[0], 'img_2': imgs[1],'img_3': imgs[2],'img_4': imgs[3],'img_5': imgs[4],})

def send_message(request):
	return render(request, 'send_message.html')

def send_image(request):
	return render(request, 'send_image.html')

# 教师上传图片
def upload_image(request):
	global upload_cnt
	if request.method == 'POST':
		image_base64 = request.POST.get('t_image')
		img_strs = image_base64.split(',')[1]
		imgdata = base64.b64decode(img_strs)  # 解码
		now = datetime.datetime.now()
		file = open('face_tmp.png', 'wb')  # 保存为face_tmp.png的图片
		file.write(imgdata)
		file.close()
		upload_cnt += 1
		# 上传合照并返回未识别的已注册id
		un_ids = main.compilface('face_tmp.png', upload_cnt)
		print("未识别到：")
		print(un_ids)
		print('upload_cnt: %d' % (upload_cnt))
		# 采取直接读取一张的操作
		# with open('Recognition/' + str(upload_cnt) + '.jpg', "rb") as f:
		# 	base64_data = base64.b64encode(f.read())
		# base64_data = str(base64_data, encoding="utf-8")
		# image_base64 = "data:image/png;base64," + base64_data

		# 存储进numpy里加快读取速度
		if not os.path.exists('imgs.npy'):
			imgs = []
			for i in range(1, 6):
				try:
					with open('Recognition/' + str(i) + '.jpg', "rb") as f:
						base64_data = base64.b64encode(f.read())
					base64_data = str(base64_data, encoding="utf-8")
					image_base64 = "data:image/png;base64," + base64_data
					imgs.append(image_base64)
				except:
					pass
			np.save('imgs.npy', imgs)
		else:
			imgs = np.load('imgs.npy')
			try:
				imgs = imgs.tolist()
			except:
				pass
			with open('Recognition/' + str(upload_cnt) + '.jpg', "rb") as f:
				base64_data = base64.b64encode(f.read())
			base64_data = str(base64_data, encoding="utf-8")
			image_base64 = "data:image/png;base64," + base64_data
			if len(imgs) == 5:
				imgs.pop(0)
				imgs.append(image_base64)
			else:
				imgs.append(image_base64)
			np.save('imgs.npy', imgs)
		if len(imgs) < 5:
			for i in range(5 - len(imgs)):
				imgs.append('')
		return render(request, 'record.html',
		              {'img_1': imgs[0], 'img_2': imgs[1], 'img_3': imgs[2], 'img_4': imgs[3], 'img_5': imgs[4], })
