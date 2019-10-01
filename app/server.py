import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from PIL import Image
from matplotlib.pyplot import imshow
import numpy as np

export_file_url = 'https://www.dropbox.com/s/qjs4v9dqgh1dpsu/export_lm_first-2.pkl?dl=1'
export_file_url_2 = 'https://www.dropbox.com/s/kj3dg0o0umd7pfp/export_lm.pkl?dl=1'
export_file_name = 'export_lm_first-2.pkl'
export_file_name_2 = 'export_lm.pkl'

temp_file_name = 'temp_mask.png'

classes = ['0', '1']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

async def setup_learner_2():
    await download_file(export_file_url_2, path / export_file_name_2)
    try:
        learn_2 = load_learner(path, export_file_name_2)
        return learn_2
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]

tasks_2 = [asyncio.ensure_future(setup_learner_2())]
learn_2 = loop.run_until_complete(asyncio.gather(*tasks_2))[0]
loop.close()

#loop_2 = asyncio.get_event_loop()
#tasks_2 = [asyncio.ensure_future(setup_learner_2())]
#learn_2 = loop_2.run_until_complete(asyncio.gather(*tasks_2))[0]
#loop_2.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    
    img.save('img_temp_test.png')
    imgItest = Image.open('img_temp_test.png');
    imgItest = imgItest.resize((64,128), Image.ANTIALIAS)
    imgItest.save('img_temp_test.png')

    img = open_image('img_temp_test.png')
    
    #prediction = learn.predict(img)[1]
    

    predsSeg = learn.predict(img)
    h = predsSeg[2][1].shape[0]
    top = h
    bottom = 0
    left = predsSeg[2][1].shape[1]
    right = 0
    for i in range(0,h):
      tensorI = predsSeg[2][1][i]
      w = tensorI.shape[0]
      for k in range(0,w):
        if tensorI[k] > 0.75:
          if i < top:
            top = i
          if i > bottom:
            bottom = i
          if k > right:
            right = k
          if k < left:
            left = k

    #bbox = ImageBBox.create(*img.size, [[top,left,bottom,right]], labels=[0], classes=['eye'])
    #img.show(y=bbox)
    imTemp = Image.open('img_temp_test.png')
    imTemp = imTemp.crop((left,top,right,bottom))
    imTemp = imTemp.resize((148,148))
    tempImgName = "temp.png"
    imTemp.save(tempImgName)
    
    img = open_image(tempImgName)
    predsSeg_2 = learn_2.predict(img)
    
    
    
    
    
    #prediction_2 = learn_2.predict(img)[0]
    #arr = np.asarray(prediction[0])
    
    #arr2 = np.asarray(prediction_2[0])
    #imgMask = Image.fromarray(arr,'L')
    #imgMask.save(path / temp_file_name)
    return JSONResponse({'result': str(path)})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
