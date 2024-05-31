import uvicorn
from fastapi import FastAPI, File, UploadFile
from typing_extensions import Annotated
import pandas as pd
from io import BytesIO
from pyngrok import ngrok
from filter_data import filter_data,send_data
import threading
# from send_mqtt import send_mqtt
app = FastAPI(docs_url="/",reload=True)

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    print("Creating file", file,len(file))
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print('Creating',file)
    file_contents = await file.read()
    # data = pd.read_csv(pd.compat.StringIO(file_contents.decode('utf-8')))
    # data = file_contents.read().decode('utf-8').splitlines()
    # df = pd.read_csv(StringIO('\n'.join(data)))
    df = pd.read_excel(BytesIO(file_contents),sheet_name='Shop 1-(07-31.07.2022)')
    # name_col= data.iloc[4]
    # rows_to_drop = data.index[0:5]
    # # Xóa 4 hàng đầu tiên
    # data_cleaned = data.drop(rows_to_drop)
    # data_cleaned.columns = [name_col]
    df= filter_data(df)
    threading.Thread(target=send_data,args=([df]), daemon=True).start()
    
    return {"filename": file.filename}

if __name__ == "__main__":
    from pyngrok import ngrok, conf
    conf.get_default().auth_token = "2gg1a79zdywtdyOSpZWE5tksRMX_5d8SVyUsshp7tYxzyem92"
    public_url = ngrok.connect(8022)
    print("ngrok tunnel URL:", public_url)
    uvicorn.run('__main__:app', host="0.0.0.0", port=8022,reload=True)
