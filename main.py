from fastapi import FastAPI, UploadFile
from nudenet import NudeDetector  


app = FastAPI()
detector = NudeDetector()
bun_w = ['FEMALE_BREAST_EXPOSED', 'ANUS_EXPOSED', 'FEMALE_GENITALIA_EXPOSED']
bun_NSFW = {'class': True, 'score': True}


@app.post("/moderate")
async def moder_pic(upload_f: UploadFile):
    filename = upload_f.filename
    scan_pic = detector.detect(filename)
    check_NSFW = [{
    "class": t["class"] in scan_pic,
    "score": t["score"]>0.7} for t in scan_pic]
    if bun_NSFW in check_NSFW:
        return {"BUN": "NSFW"}
    return {"ok": "Safe"}
 
