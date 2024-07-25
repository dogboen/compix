import os
from zipfile import ZipFile
from pathlib import Path

os.chdir('./zipfix')

for broke in Path(os.getcwd()).iterdir():
    goodname = broke.name
    broke.rename(goodname + 'OLD')
    broke_zip = ZipFile(broke.name + 'OLD', 'r')
    print(f"Zipfixing {goodname}...")

    with ZipFile(goodname, 'w') as fix_zip:
        for file in broke_zip.filelist:
            if file.file_size > 10:
                filedata = broke_zip.read(file.filename)
                if file.filename.endswith('.xml'):
                    filedecode = filedata.decode()
                    filedata = filedecode.encode('utf-8')
                elif file.filename.endswith('.jpg'):
                    pagenum = file.filename.rsplit('page')[1]
                    file.filename = file.filename.replace(pagenum, pagenum.zfill(7))
                tpb_mess = file.filename.rsplit('/')
                if len(tpb_mess) > 1:
                    tpb_dir = file.filename.removesuffix(tpb_mess[-1:][0])
                    if not os.path.exists(tpb_dir):
                        os.makedirs(tpb_dir)
                f = open(file.filename, "wb+")
                f.write(filedata)
                f.close()
                fix_zip.write(f.name)
                os.remove(f.name)
    broke_zip.close()
    print("fixed")
    os.remove(broke_zip.filename)
    for root, dirs, files in os.walk('.', topdown=False):
        for dir in dirs:
            try:
                os.removedirs(os.path.join(root, dir))
            except OSError:
                pass
