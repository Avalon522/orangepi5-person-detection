import json,time,base64,os
from datetime import datetime
from urllib.request import Request,urlopen
import cv2
class Alarm:
    def __init__(self):
        self.threshold=.5
        self.root=os.environ.get('ALARM_SERVER_URL', 'http://127.0.0.1:8000')
        self.active=False
        self.streak=0
        self.empty_at=None
        self.frozen=None
        self.next_send=0
    def post(self,path,data,headers):
        with urlopen(Request(self.root+path,data=data,headers=headers,method='POST'),timeout=2) as r: r.read()
    def jpeg(self,image):
        ok,j=cv2.imencode('.jpg',image,[cv2.IMWRITE_JPEG_QUALITY,80])
        if not ok: raise RuntimeError('JPEG encoding failed')
        return j.tobytes()
    def update(self,detections,image=None):
        if image is None:return
        now=time.monotonic()
        scores=[float(s) for _,s in detections if s>=self.threshold]
        try:
            if scores:
                self.empty_at=None
                if not self.active:
                    if self.streak==0:self.first=(image.copy(),len(scores),max(scores),datetime.now().astimezone().isoformat(timespec='seconds'))
                    self.streak+=1
                    if self.streak>=3:
                        self.active=True
                        im,n,s,t=self.first
                        event=dict(device_id='orangepi5',person_count=n,max_confidence=s,event_time=t,test=False,image_base64=base64.b64encode(self.jpeg(im)).decode())
                        try:
                            self.post('/api/alert',json.dumps(event).encode(),{'Content-Type':'application/json'})
                            print('[ENTRY ALARM] first frame saved',flush=True)
                        except Exception as e:print('[ALARM FAILED]',e,flush=True)
            else:
                self.streak=0
                if self.empty_at is None:
                    self.empty_at=now
                if self.active and now-self.empty_at>=1:
                    self.active=False
                    print('[CLEAR] no person confirmed',flush=True)
            # Send every processed image, even when nobody is present.
            self.post('/api/frame',self.jpeg(image),{'X-Person-Count':str(len(scores))})
        except Exception as e:print('[LIVE FAILED]',e,flush=True)
