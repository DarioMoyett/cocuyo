library(shiny)
library(rPython)
library(png)


shinyServer(function(input, output,session) {
  
  observe({
    
    query <- parseQueryString(session$clientData$url_search)
    print(query)

   
  construyeTable <- function(inFile)
  {
    if (is.null(inFile) & (!input$usarEjemplo))
      return(NULL)
    
    if(input$usarEjemplo)
    {
      datos <<- read.table("ejemplo.dat",col.names=c("azimuth","elevation","magnitude"))
      
    }else
    {
      datos <<- read.table(inFile$datapath,
                         col.names=c("azimuth","elevation","magnitude"))
    }
    
    return(datos)
  }
     
  construyePolar <- function(inFile)
  {
    if (is.null(inFile) & (!input$usarEjemplo))
      return(NULL)
    
    if(input$usarEjemplo)
    {
      datos <<- read.table("ejemplo.dat",col.names=c("azimuth","elevation","magnitude"))
      outfile ="ejemplo.png"
      titulo = "Pitahaya"
      fecha  = "8/Febrero/2016"
      
    }else
    {
      datos <<- read.table(inFile$datapath,
                           col.names=c("azimuth","elevation","magnitude"))
      outfile = paste0(unlist(strsplit(inFile$datapath,".",fixed=TRUE))[1],".png")
      titulo = input$titulo
      fecha  = input$fecha
    }
    
    
    python.assign("datos",datos)
    python.assign("outfile",outfile)
    python.assign("miTitulo",titulo)
    python.assign("miFecha",fecha)
    python.assign("miColor",input$select)
    python.assign("puntosMuestreo",input$muestreo)
    python.assign("direccionReloj",input$reloj)
    python.assign("mostrarContorno",input$contorno)
    
    python.load("polarPlot.py")
    
    img <- readPNG(outfile)
    
    list(src = outfile,
         contentType = 'image/png',
         width = 500,
         height = 531,
         alt = "This is alternate text")

  }
  

  output$plot1<- renderImage({construyePolar(input$file1)})  
  
  output$info <- renderText({HTML("<BR>Esta aplicaci&oacute;n permite construir un gr&aacute;fico polar 
    a partir de datos de magnitudes visibles colectados utilizando el instrumento 
    SQM. Los datos consisten de tres columnas: azimut, elevaci&oacute;n, y la magnitud 
    en cada punto.")})
  
  output$table = renderDataTable({construyeTable(input$file1)})

  })
  
})