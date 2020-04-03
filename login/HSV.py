import cv2
class HSV():
    def hsv(self,r, g, b):
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df/mx
        v = mx
        return h,s,v

    def hsvSpace(self,h,s,v):
        h=int(h)
        if h >= 316 or h <= 20:
            H = 0
        elif 20 <= h <= 40:
            H = 1
        elif 41 <= h <= 75:
            H = 2
        elif 76 <= h <= 155:
            H = 3
        elif 156 <= h <= 190:
            H = 4
        elif 191 <= h <= 270:
            H = 5
        elif 271 <= h <= 295:
            H = 6
        elif 295 <= h <= 315:
            H = 7
        if 0 <= s < 0.2:
            S = 0
        elif 0.2 <= s < 0.7:
            S = 1
        elif 0.7 <= s <= 1:
            S = 2
        if 0 <= v < 0.2:
            V = 0
        elif 0.2 <= v < 0.7:
            V = 1
        elif 0.7 <= v <= 1:
            V = 2
        return H,S,V

    def hsvFeature(self,image):
        b,g,r=cv2.split(image)
        feature=[]
        for i in range(len(b)):
            for j in range(len(b[0])):
                temp_r=r[i][j]
                temp_g=g[i][j]
                temp_b=b[i][j]
                h,s,v=self.hsv(temp_r,temp_g,temp_b)
                H,S,V=self.hsvSpace(h,s,v)
                l=9*H+3*S+V
                feature.append(l)
        hist=[0]*72
        for i in feature:
            hist[i]+=1
        return hist

    def hsvFeaturePro(self,image):
        h1_list=[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190]
        h2_list=[200,205,210,215,220,225,230,235,240,245,250,255,260,265,270,275,280,285,290,295]
        h3_list=[300,310,320,330,340,350]
        s_list=[0.173,0.423,0.673,0.923]
        v_list=[0,0.25,0.5,0.75]
        b, g, r = cv2.split(image)
        feature = []
        for i in range(len(b)):
            for j in range(len(b[0])):
                temp_r = r[i][j]
                temp_g = g[i][j]
                temp_b = b[i][j]
                h,s,v= self.hsv(temp_r, temp_g, temp_b)
                H,S,V=self.hsvSpace(h,s,v)
                if 0<=H<200:
                    d=360
                    for index,value in enumerate(h1_list):
                        if abs(H-value)<d:
                            d=abs(H-value)
                            class_H=index
                elif 200<=H<300:
                    d=360
                    for index,value in enumerate(h2_list):
                        if abs(H-value)<d:
                            d=abs(H-value)
                            class_H=index+20
                elif 300<=H<360:
                    d = 360
                    for index, value in enumerate(h3_list):
                        if abs(H - value) < d:
                            d = abs(H - value)
                            class_H = index + 40
                d=1
                for index, value in enumerate(s_list):
                    if abs(H - value) < d:
                        d = abs(H - value)
                        class_S = index
                d = 1
                for index, value in enumerate(v_list):
                    if abs(H - value) < d:
                        d = abs(H - value)
                        class_V = index
                l=4*H+3*S+V
                feature.append(l)
        hist = [0] * 193
        for i in feature:
            hist[i] += 1
        return hist
    def getFeatures(self,image):
        image_1 = image[0:50, 0:50]
        image_2 = image[50:100, 0:50]
        image_3 = image[0:50, 50:100]
        image_4 = image[50:100, 50:100]

        hist_1 = self.hsvFeature(image_1)
        hist_2 = self.hsvFeature(image_2)
        hist_3 = self.hsvFeature(image_3)
        hist_4 = self.hsvFeature(image_4)

        hist = []
        hist.extend(hist_1)
        hist.extend(hist_2)
        hist.extend(hist_3)
        hist.extend(hist_4)
        return hist



