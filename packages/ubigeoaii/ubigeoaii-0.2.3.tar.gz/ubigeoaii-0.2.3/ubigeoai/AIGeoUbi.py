



def GeoUbicacion(path_raster, path_model, confidence, output_name, img_div):
    import rasterio
    import geopandas as gpd
    import numpy as np
    from matplotlib import pyplot as plt 
    from rasterio.windows import Window 
    import os 
    import pandas as pd 
    from skimage.io import imsave
    import glob
    from shapely.geometry import Polygon
    from shutil import rmtree 




    if not os.path.isdir('Resultados'):
        os.mkdir('Resultados')
        
    if not os.path.isdir('Predict'):
        os.mkdir('Predict')

    if not os.path.isdir('Predict_jpg'):
        os.mkdir('Predict_jpg')
    
    if not os.path.isdir('runs'):
        os.mkdir('runs')
    rmtree("Predict")
    rmtree("Predict_jpg")
    rmtree("Resultados")
    rmtree("runs")
    path_img = path_raster
    src_img = rasterio.open(path_img)
    img = src_img.read()
    print(img.shape)
    img = img.transpose([1,2,0])
    plt.figure(figsize=[16,16])
    plt.imshow(img)
    plt.axis('off')
    
    #Dvividir el ortomosaico en imagenes mas pequeñas (img_div X img_div pixeles)
    if not os.path.isdir('Resultados'):
        os.mkdir('Resultados')
        
    if not os.path.isdir('Predict'):
        os.mkdir('Predict')
    
    qtd = 0
    out_meta = src_img.meta.copy()
    for n in range((src_img.meta['width']//img_div)):
        for m in range((src_img.meta['height']//img_div)):
            x = (n*img_div)
            y = (m*img_div)
            window = Window(x,y,img_div,img_div)
            win_transform = src_img.window_transform(window)
            arr_win = src_img.read(window=window)
            arr_win = arr_win[0:3,:,:]
            if (arr_win.max() != 0) and (arr_win.shape[1] == img_div) and (arr_win.shape[2] == img_div):
                qtd = qtd + 1
                path_exp = 'Predict/img_' + str(qtd) + '.tif'
                out_meta.update({"driver": "GTiff","height": img_div,"width": img_div, "transform":win_transform})
                with rasterio.open(path_exp, 'w', **out_meta) as dst:
                    for i, layer in enumerate(arr_win, start=1):
                        dst.write_band(i, layer.reshape(-1, layer.shape[-1]))
                del arr_win
    print(qtd)
    
    
    if not os.path.isdir('Predict_jpg'):
        os.mkdir('Predict_jpg')
        
    path_data_pred = 'Predict_jpg'
    imgs_to_pred = os.listdir('Predict')
    
    for images in imgs_to_pred:
        src = rasterio.open('Predict/' + images)
        raster = src.read()
        raster = raster.transpose([1,2,0])
        raster = raster[:,:,0:3]
        imsave(os.path.join(path_data_pred,images.split('.')[0] + '.jpg'), raster)
        
    
    from ultralytics import YOLO
    model = YOLO(path_model)
    model.predict('Predict_jpg', save=True,save_txt=True, show_conf=False, show_labels=False, imgsz=640, conf=confidence)
    from IPython.display import Image, display
    for images in glob.glob('runs/obb/predict/*.jpg')[316:320]:
        display(Image(filename=images))
    
    
    ls_poly = []
    ls_class = []
    
    imgs_to_pred = [f for f in os.listdir('runs/obb/predict/labels/') if f.endswith('.txt')]
    for images in imgs_to_pred:
        filename = images.split('.')[0]
        src = rasterio.open('Predict/' + filename + '.tif')
        path = f'runs/obb/predict/labels/'+filename+'.txt'
        cols = ['class', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4']
        df = pd.read_csv(path, sep=" ", header=None)
        df.columns = cols
        df['x1'] = np.round(df['x1'] * img_div)
        df['y1'] = np.round(df['y1'] * img_div)
        df['x2'] = np.round(df['x2'] * img_div)
        df['y2'] = np.round(df['y2'] * img_div)
        df['x3'] = np.round(df['x3'] * img_div)
        df['y3'] = np.round(df['y3'] * img_div)
        df['x4'] = np.round(df['x4'] * img_div)
        df['y4'] = np.round(df['y4'] * img_div)

        for i,row in df.iterrows():
            xs1, ys1 = rasterio.transform.xy(src.transform, row['y1'], row['x1'])
            xs2, ys2 = rasterio.transform.xy(src.transform, row['y2'], row['x2'])
            xs3, ys3 = rasterio.transform.xy(src.transform, row['y3'], row['x3'])
            xs4, ys4 = rasterio.transform.xy(src.transform, row['y4'], row['x4'])

            ls_poly.append(Polygon([[xs1, ys1], [xs2,ys2], [xs3, ys3], [xs4,ys4]]))
            ls_class.append(row['class'])
            
    
    gdf = gpd.GeoDataFrame(ls_class, geometry=ls_poly, crs=src.crs)
    gdf.rename(columns={0:'class'}, inplace=True)
    print(gdf)
    gdf.to_file('Resultados/' + output_name)
    gdf.to_file('Resultados/' + output_name)






#Descarga de archivos de precipitacion

def DescargaChirps(route = str, fechain = int, fechafin = int):
    import requests
    import os
    chirps_files = []
    for year in range(fechain, fechafin):
        if fechain > fechafin:
            print('Error: el primer año ingresado es mayor que el segundo')
            exit()
        for month in range(1, 13):
            file_name = f"chirps-v2.0.{year}.{month:02d}.tif.gz"
            url = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/{file_name}"
            chirps_files.append(url)
    for file_url in chirps_files:
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(route, os.path.basename(file_url))
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        print("")
                    else:
                        print(f"Hubo un problema al descargar el archivo {os.path.basename(file_url)}. Código de estado: {response.status_code}")



def CortarMultiRaster(carpeta_in = str, shapefileroute = str, carpeta_out = str):
    import rasterio
    import rasterio.mask
    import fiona
    import os
    def buscarRASTER(carpeta):
        lista = []
        lista2 = []
        print(lista2)
        for ruta, NombreCarpeta, fileNames in os.walk(carpeta):
            for archivo in fileNames:
                if(archivo.endswith('.tif')):
                    lista2.append(archivo)
                    lista.append(os.path.join(ruta, archivo))
        return lista
    lista_raster = buscarRASTER(carpeta_in)
    print(lista_raster)
    with fiona.open(shapefileroute, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]
    for shp in lista_raster:
        shp = shp.replace("\\", "/")
        print(shp)
        with rasterio.open(shp) as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            out_meta = src.meta
        out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})
        with rasterio.open(shp, "w", **out_meta) as dest:
            dest.write(out_image)
       
            
            
            
                        

  




  
