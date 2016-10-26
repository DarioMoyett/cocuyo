import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
import matplotlib.image as mpimg
import matplotlib.cm as cm
from   matplotlib.colorbar import ColorbarBase
from   matplotlib.colors import Normalize
from   matplotlib.pyplot import figure
from   scipy.interpolate import griddata
import pandas as pd
import numpy as np 
import math
import os 


# funcion para interpolar los datos 

def interpolaDatos(THETA,R,magnitude):
  
  THETAi  = np.linspace(min(THETA),max(THETA),num=720.0)
  
  Ri      = np.linspace(min(R),max(R),num=360.0)
  
  theta,r = np.meshgrid(THETAi,Ri,indexing='xy') 
  
  z = griddata((THETA,R),magnitude,(theta,r),method="linear")
  
  z = np.round(z,2)
  
  return((THETAi,Ri,z))


# funcion para promediar la medidas a azimuto 0 y 360

def fixMagnitude(magnitude):
  
  inx0    = np.arange(0,6)
  
  inx360  = np.arange(len(magnitude) - 6,len(magnitude))
  
  magnitude0    = magnitude[inx0]
  
  magnitude360  = magnitude[inx360]
  
  magnitudePromedio = (magnitude0 + magnitude360)/2
  
  magnitude[inx0]   = magnitudePromedio 
  
  magnitude[inx360] = magnitudePromedio    

  return(magnitude)

# funcion para seleccinar tabla de colores

def seleccionaColor(miColor):
  if (miColor == "azul"):
    micolor = cm.YlGnBu
  elif (miColor == "anaranjado"):
    micolor = cm.autumn
  elif (miColor == "gris"):
    micolor = cm.Greys 
  return(micolor)
  

# funcion para extraer columnas de data frame 

def extraeColumnas(df):
  
  azimuth   = np.array(df['azimuth'])
  elevation = np.array(df['elevation'])
  magnitude = np.array(df['magnitude'])
 
  return((azimuth,elevation,magnitude))


def polarPlot(df,outfile,
              miTitulo,
              miFecha,
              miColor="azul",
              puntosMuestreo = False,
              direccionReloj = False,
              mostrarContorno = False):
                
  # titulo = "Pitahaya"
  # fecha  = "8/Febrero/2016"

  # extraer columnas del dataframe
  
  azimuth,elevation,magnitude = extraeColumnas(df)
  
  # para seleccinar tabla de colores

  micolor = seleccionaColor(miColor)
  
  #fig = pyplot.figure()
  
  # para especificar el tamano del plot 
  
  fig = figure(figsize=(8.0,8.6))
  
  # para promediar la medidas a azimuto 0 y 360 

  magnitude = fixMagnitude(magnitude)
  
  # conversion de angulos a radianes 
  
  theta = np.radians(azimuth)
  phi   = np.radians(elevation)  
  
  # definicion de eje para barra de colores 
  
  cax = fig.add_axes([0.25, 0.03, 0.5, 0.03])
  
  # definicion de eje para grafica polar 
  
  ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], 
                  frameon=True,
                  polar=True,axisbg='#d5de9c',aspect='equal')

  if direccionReloj:  
    ax.set_theta_direction(-1)
    ax.set_theta_offset(math.pi/2.0)
  
  labels = np.unique(theta)
  
  ax.set_xticks(labels[:-1])
  ax.set_yticks(())
  
  rCard  = 1.4
  
  ax.set_xticklabels(['N', '$30^o$', '$60^o$', 'E', 
  '$120^o$', '$150^o$','S', '$210^o$', '$240^o$','W', '$300^o$','$330^o$'],
  ha='center') 
  
  # ax.text(0.0,rCard,"N",fontsize=14,weight='bold')
  # ax.text(math.pi/2,rCard,"E",fontsize=14,weight='bold')
  # ax.text(math.pi,rCard,"S",fontsize=14,weight='bold')
  # ax.text(3*math.pi/2,rCard,"W",fontsize=14,weight='bold')
  # 
  thetai,phii,z = interpolaDatos(theta,phi,magnitude)
  
  vmin = 18.0
  vmax = 22.0 
  
  ax.contourf(thetai,phii,z,10,linewidth=2,cmap=micolor,vmin=vmin,vmax=vmax)
  
  if direccionReloj:
    ang = 0.0
  else:
    ang = math.pi/2    
  
 
  ax.text(ang,1.5,miTitulo,fontsize=22,horizontalalignment='center')
  ax.text(ang,1.4,miFecha,fontsize=22,horizontalalignment='center')
  
  #ax.contourf(THETAi,Ri,z,10,linewidth=2,cmap=micolor)
  #pyplot.clabel(CS,fontsize=9,fmt='%1.2f',colors="k")  
  
  if mostrarContorno:
    ax.contour(thetai,phii,z,10,colors="k")
  
  # mostrar puntos de muestreo 
  
  if puntosMuestreo:
    ax.scatter(theta,phi)
  
  # especificar radio del mapa polar 
  
  ax.set_rmax(1.2)
  
  #vmin = min(magnitude)
  #vmax = max(magnitude)
  
  # rango de magnitudes en la tabla de colores 
  
  
  # # para mostrar las unidades al lado de la barra de colores 
  
  if direccionReloj:
    ax.text(np.radians(151),1.7,"$mag/arcsec^2$",
      weight="bold",
      fontsize=16)
  else:
    ax.text(np.radians(299),1.7,"$mag/arcsec^2$",
            weight="bold",
            fontsize=16)
        
      
  
  ColorbarBase(cax,orientation='horizontal',cmap=micolor,
               spacing='proportional',
               norm=Normalize(vmin=vmin, vmax=vmax))
  
  pyplot.savefig(outfile)
  
  pyplot.close()
  
  #return(fig)
  
  
  
  
polarPlot(datos,outfile,miTitulo,miFecha,miColor,puntosMuestreo,direccionReloj,mostrarContorno)
