library(shiny)
library(shinythemes)

shinyUI(fluidPage(theme = shinytheme("readable"),
  tags$br(),
  sidebarLayout(
    sidebarPanel(

      HTML("<H1><font face ='Verdama' color = 'blue'> Cocuyo </font>  Visualizaci&oacute;n de  Datos de Brillo Nocturno</H1>"),
      
      HTML("<p align='justify'>Aplicaci&oacute;n en linea para visualizar datos colectados 
      utilizando el protocolo XYZ. Un proyecto del Grupo de Trabajo de
      Contaminaci&oacute;n Lum&iacute;nica de Puerto Rico.<p>"), 
      
      checkboxInput("usarEjemplo",label = "Utilizar archivo de ejemplo",value=TRUE), 
      
      tags$hr(),
      
      conditionalPanel(condition = "input.usarEjemplo == false",
      fileInput('file1', 'Seleccionar archivo')),
      
      conditionalPanel(condition = "input.usarEjemplo == false",
                       textInput('titulo', 'Titulo')),
      
      conditionalPanel(condition = "input.usarEjemplo == false",
                       textInput('fecha', 'Fecha')),
      
      checkboxInput("muestreo", label = "Mostrar puntos de muestreo", value = FALSE),
      
      checkboxInput("contorno", label = HTML("Mostrar l&iacute;neas  de contorno"), value = FALSE),
      
      checkboxInput("reloj", label = HTML("Gr&aacute;fico en direcci&oacute;n de manecillas del reloj"), value = FALSE),
      
      tags$hr(),
      
      selectInput("select", label = "Tabla de colores", 
                  choices = list("Azul" = "azul", "Anaranjado" = "anaranjado",
                                 "Gris" = "gris"), selected = "azul"), 
      
      tags$hr()
    ),
    mainPanel(
      
              tabsetPanel(
              tabPanel("Info",htmlOutput("info")), 
              tabPanel("Tabla", dataTableOutput("table")), 
              tabPanel(HTML("Gr&aacute;fico Polar"), plotOutput("plot1"))
             )
    )
  )
))
