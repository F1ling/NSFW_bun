from fastapi import FastAPI, UploadFile, HTTPException
from nudenet import NudeDetector  


# Create FastAPI application
app = FastAPI()
detector = NudeDetector()
bun_w = ['FEMALE_BREAST_EXPOSED', 'ANUS_EXPOSED', 'FEMALE_GENITALIA_EXPOSED']
bun_NSFW = {'class': True, 'score': True}


@app.post("/moderate") #Create endpoint
async def moder_pic(upload_f: UploadFile):
    #Check file type
    if upload_f.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, detail="Invalid file format. Only JPEG/PNG allowed")
    try:
        #Scaning NSFW content
        filename = upload_f.filename
        scan_pic = detector.detect(filename)
        check_NSFW = [{
        "class": t["class"] in scan_pic,
        "score": t["score"]>0.7} for t in scan_pic]
        #Results
        if bun_NSFW in check_NSFW:
            return {"status": "REJECTED", "reason": "NSFW content"}
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(500, detail=f"Processing error: {str(e)}")
 
