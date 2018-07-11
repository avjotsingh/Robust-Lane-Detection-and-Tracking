import cv2
import ast
import matplotlib.pyplot as plt
import numpy as np
from points import *
import os
import pickle
import math
import pandas as pd
import random



def SaveFigureAsImage(fileName,fig=None,**kwargs):
    ''' Save a Matplotlib figure as an image without borders or frames.
       Args:
            fileName (str): String that ends in .png etc.
 
            fig (Matplotlib figure instance): figure you want to save as the image
        Keyword Args:
            orig_size (tuple): width, height of the original image used to maintain 
            aspect ratio.
    '''
    fig_size = fig.get_size_inches()
    w,h = fig_size[0], fig_size[1]
    fig.patch.set_alpha(0)
    if kwargs.has_key('orig_size'): # Aspect ratio scaling if required
        w,h = kwargs['orig_size']
        w2,h2 = fig_size[0],fig_size[1]
        fig.set_size_inches([(w2/w)*w,(w2/w)*h])
        fig.set_dpi((w2/w)*fig.get_dpi())
    a=fig.gca()
    a.set_frame_on(False)
    a.set_xticks([]); a.set_yticks([])
    plt.axis('off')
    plt.xlim(0,h); plt.ylim(w,0)
    fig.savefig(fileName, transparent=True, bbox_inches='tight', \
                        pad_inches=0)


def process_point(pt1,pt2,xmax,ymax):

	print (xmax,ymax)
	if (pt2[0]-pt1[0]) != 0:
		m = float(pt2[1]-pt1[1])/(pt2[0]-pt1[0])
	else:
		m = float(pt2[1]-pt1[1])/(pt2[0]-pt1[0]+0.0001)

	c = float(pt1[1] - m*pt1[0])

	xmin = ymin = 0

	# x =0
	x1 = 0 
	y1 =c  
	# x=xmax 
	x2 = xmax 
	y2 = m*x2 + c
	# y = 0
	x3 = -c/m
	y3 = 0 
	# y = ymax 
	x4 = (ymax-c)/m
	y4 = ymax 

	print x1,y1
	print x2,y2
	print x3,y3
	print x4,y4
	point = []
	for x,y in zip([x1,x2,x3,x4],[y1,y2,y3,y4]):
		if (x>=0 and x<=xmax) and (y>=0 and y<=ymax):
			point.append([int(x),int(y)])

	# print "UP",unique_point
	print "P",point
	# point = unique_point
	if len(point) !=2:
		unique_point = [list(x) for x in set(tuple(x) for x in point)]
		if len(unique_point) == 2:
			return unique_point
		else:
			print ("erro==================")


	else:
		return point
		

def prep_data():

	global_grad = []
	final_grad = []
	# path = '/home/ayush/lane/swarath_confidence_lstm/ann_data'
	# path = '/home/ayush/lane/data_latest'
	path = '/home/ayush/lane/ext_image+data_latest'
	# path = '/home/ayush/Documents/swarath_lane/swarath/src/lanedetection_shubhamIITK/src/new_hough'
	# path = '/home/ayush/Documents/swarath_confidence_new/analysis/testing_india' 


	files = os.listdir(path)
	# files.remove('temp')


	# print files
	# files = [i[:-4] for  i in files if i[-6]!="n"]
	files = [i[:-4] for  i in files if i[-1]!="t"]
	# print files[:10]
	files = list(set(files))
	files.sort()

	print files

	# total_file= open("total_new.txt","w") 
	total_file= open("total.txt","w") 
	
 	
	sol=[]
	dot=[]
	fal=[]

	for n in files:
	# for n in [1793]:

		print n
		print "img no",n
		# plt.figure()
		img = cv2.imread(path+"/"+str(n)+".jpg",-1)

		ymax,xmax = img.shape[:2]
		

		# print img
		h = img.shape[0]
		w = img.shape[1]
		


		file = open(path+"/"+str(n)+"_ann"+".txt", "r") 
		# file = open(path+"/"+str(n)+".txt", "r") 

		org = img.copy()
		poly = img.copy()
		# plt.subplot(2,3,1)
		# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
		a = file.read()
		b = a.split('\n')


		print b


		l_b = 0
		for i in b:
			if i =="solid" or i=="dotted" or i=="false":
				break
			else:
				l_b +=1
		

		
		points = b[:l_b]
		lane_type = b[l_b:][:-1]

		print points
		print lane_type



		points_new =[]
		for x,y in zip(points,lane_type+lane_type):
			# if y =="solid":
			points_new.append(x)
		
		points = points_new

		 # for white
	

		lines = (len(points))/2

		print "lines",lines
		if lines >0 :

			print points
			for i in range(len(points)):
				points[i] = ast.literal_eval(points[i])

			print points
			print lane_type
			

			point1 = []
			point2 = []

			for i in range(lines):
			    point1.append(points[i])
			    point2.append(points[i+(len(points)/2)])


			print point1,point2


			
			
			for i,j,t,lan in zip(point1,point2,lane_type,range(len(point1))):
				print t
				i,j = process_point(i,j,xmax,ymax)

				if t=="solid":
					# sol+=1
					sol.append(str(n)+"_"+str(lan)+".jpg")
					t =0
				elif t=="dotted":
					# dot+=1
					dot.append(str(n)+"_"+str(lan)+".jpg")

					t=1
				elif t=="false" :
					# fal+=1 
					fal.append(str(n)+"_"+str(lan)+".jpg")
					
					t=2
				# i[0] -= 10
				# j[0] += 10
				offset = 15
				# offset = 25
				a = (i[0]-offset,i[1])
				b = (i[0]+offset,i[1])
				c = (j[0]+offset,j[1])
				d = (j[0]-offset,j[1])

				mask = np.zeros(img.shape, dtype=np.uint8)
				roi_corners = np.array([[a,b,c,d]], dtype=np.int32)
				# fill the ROI so it doesn't get wiped out when the mask is applied
				channel_count = img.shape[2]  # i.e. 3 or 4 depending on your img
				ignore_mask_color = (255,)*channel_count
				cv2.fillPoly(mask, roi_corners, ignore_mask_color)
				# from Masterfool: use cv2.fillConvexPoly if you know it's convex

				# apply the mask
				masked_img = cv2.bitwise_and(img, mask)


				print i,j

				if "dnd" in n:
					print "============================="
					k1 = 100
					k2 = 0
				else:
					k1 = 70
					k2 = 30

				z = [0,0]
				if i[1] < j[1] :
					
					z[0] = (k1*i[0] + k2*j[0])/(k1+k2)
					z[1] = (k1*i[1] + k2*j[1])/(k1+k2)

					print z
					# if i[0]<j[0]:
					if z[0]<j[0]:
						# crop_img = masked_img[i[1]:j[1], i[0]:j[0]]
						crop_img = masked_img[z[1]:j[1], z[0]:j[0]]
					elif z[0]>j[0]:
						# crop_img = masked_img[i[1]:j[1], j[0]:i[0]]
						crop_img = masked_img[z[1]:j[1],j[0]:z[0]]
					elif z[0] == j[0]:
						# crop_img = masked_img[i[1]:j[1], j[0]-offset:j[0]+offset]
						crop_img = masked_img[z[1]:j[1], j[0]-offset:j[0]+offset]
				elif i[1] > j[1]:
					z[0] = (k1*j[0] + k2*i[0])/(k1+k2)
					z[1] = (k1*j[1] + k2*i[1])/(k1+k2)

					print z
					if i[0]<z[0]:
						# crop_img = masked_img[j[1]:i[1], i[0]:j[0]]
						crop_img = masked_img[z[1]:i[1], i[0]:z[0]]
					elif i[0] > z[0]: #right lane 
						# crop_img = masked_img[j[1]:i[1], j[0]:i[0]]
						crop_img = masked_img[z[1]:i[1], z[0]:i[0]]
					elif i[0] == z[0]:
						# crop_img = masked_img[j[1]:i[1], j[0]-offset:j[0]+offset]
						crop_img = masked_img[z[1]:i[1], j[0]-offset:j[0]+offset]
				# elif i[0] == j[0]:
				# 	print "true"
				# 	if i[1]<j[1]:
				# 		crop_img = masked_img[i[1]:j[1], i[0]-offset:i[0]+offset]
				# 	else:
				# 		crop_img = masked_img[j[1]:i[1], j[0]-offset:j[0]+offset]


				print crop_img.shape

				# try :
				crop_img = cv2.resize(crop_img,(224,224))
				# plt.imshow((cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)))
				# ext_file.write("%s%d\n" %(str(n)+"_"+str(lan)+".jpg,",t)) 

				cv2.imwrite("/home/ayush/lane/ext_image/"+str(n)+"_"+str(lan)+".jpg", crop_img)
					# plt.show()
				# except:
					# print "======================================>><<<<<<<<<<<<<<<=========s"
					# pass
			# Gradients
		
	# print sol
	# print dot
	# print fal
	random.shuffle(sol)
	random.shuffle(dot)
	random.shuffle(fal)

	print len(sol)
	print len(dot)
	print len(fal)

	train_set_sol = sol[:int(0.7*len(sol))] 
	val_set_sol = sol[int(0.7*len(sol)):]
	train_set_dot = dot[:int(0.7*len(dot))] 
	val_set_dot = dot[int(0.7*len(dot)):] 
	train_set_fal = fal[:int(0.7*len(fal))] 
	val_set_fal = fal[int(0.7*len(fal)):]

	print len(val_set_sol)
	print len(val_set_dot)
	print len(val_set_fal)

	for i in train_set_sol:
		total_file.write("%s,%d\n" %(i,0)) 
	for i in val_set_sol:
		total_file.write("%s,%d\n" %(i,0)) 
	for i in train_set_dot:
		total_file.write("%s,%d\n" %(i,1)) 
	for i in val_set_dot:
		total_file.write("%s,%d\n" %(i,1)) 
	for i in train_set_fal:
		total_file.write("%s,%d\n" %(i,2)) 
	for i in val_set_fal:
		total_file.write("%s,%d\n" %(i,2)) 




prep_data()

# 1110
# 379
# 553
