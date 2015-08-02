# This code reads the text files of the prediction errors into R
# and the code outputs a .csv that is read to be connected with the 
# SQL-django interface

# Parts of this code that is commented out was also used for analysis

# This code is mostly original with guidance from the following sources:
# http://en.wikipedia.org/wiki/Kernel_density_estimation (provides R code for KDE)
# http://stackoverflow.com/questions/11538532/change-stringsasfactors-settings-for-data-frame
# https://blog.udemy.com/r-tutorial/
# http://www.inside-r.org/r-doc/base/file.remove
# http://www.statmethods.net/advgraphs/axes.html

# First run the command: install.packages("KernSmooth")
# Source: http://cran.r-project.org/web/packages/KernSmooth/index.html
# Select a CRAN mirror, and allow it to download
library(KernSmooth)

# Navigate to correct directory. Re-enter the R environment to re-run code
setwd("Output")

routes = c("6","55","171","172")
stops = cbind(c("2815","1659","5037","14483","1421","1427","4872","5033","1651","5206"), 
  c("10565","15193","10589","10603","10615","14122","10502","10511","10536","10548"), 
  c("5919","10567","14033","14019","15433","16036","10563","1520","NA","NA"), 
  c("1523","15817","14033","14019","15433","14040","14039","16124","NA","NA"))

# Initialize column values
Bus <- -999
Stops <- -999
Type <- "First"
Time <- -999
Prediction.Lower <- -999
Prediction.Upper <- -999

# Loop through .txt files in Output and calculate our predictions
for (time in seq(0,30)){
  for (j in seq(1,4)){
	for (i in seq(1,10)){
	  for (type in c("Bus","Official")){
	    filename <- paste(time,"_",routes[j],"_",stops[i,j],"_",type,".txt",sep="")
	    if (file.exists(filename)){
	      data <- as.numeric(read.table(filename, sep = ","))
	      Bus <- c(Bus,routes[j])
	      Stops <- c(Stops, stops[i,j])
	      Type <- c(Type, type)
	      Time <- c(Time, time)
	      # All of these cases had observations of all 0 -- not eligible for KDE        
	      if ((time == 0) && (((j == 3) && ((i == 8) || (i == 2) || (i == 3)) | ((j == 1) && (i == 7))))) {
	    	prediction <- 0
	    	Prediction.Lower <- c(Prediction.Lower, prediction) 
	    	Prediction.Upper <- c(Prediction.Upper, prediction) 
	      } 
	      else {
	    	kde <- bkde(x=data) 
	    	sd <- sd(unlist(kde))
	    	m <- mean(unlist(kde))
	    	prediction.lower <- m-0.5*sd
	    	prediction.upper <- m+0.5*sd
	    	Prediction.Lower <- c(Prediction.Lower, prediction.lower)
	    	Prediction.Upper <- c(Prediction.Upper, prediction.upper)
	    	#plot(kde, xlab = "Time", ylab = "Density", pch = 16, main = filename)
	      }
          #hist(data, main = filename)
          #dev.copy(png,paste(filename,".png",sep=""))
          #dev.off()
        }
	  }
    }
  }
} 
prediction_data <- data.frame(cbind(Bus, Stops, Type, Time, Prediction.Lower, Prediction.Upper),stringsAsFactors = FALSE)
write.table(prediction_data,file="Predictions.csv",sep="|", quote =FALSE, row.names = FALSE)


# Analysis and Construction of Histograms
#route = 0
#stop = 0
#num_obs = 0
#num_correct = 0
#for (j in seq(1,4)){
#  for (i in seq(1,10)){
#    filename <- paste("AVG",routes[j],"_",stops[i,j],".txt",sep="")
#    if (file.exists(filename)){
#      data <- as.numeric(read.table(filename, sep = ","))
      
#      num_obs <- c(num_obs, length(data))
#      num_correct <- c(num_correct, length(data[data == 0]))
#      route = c(route, routes[j])
#      stop = c(stop, stops[i,j])
#      hist(data, main = filename, sub = paste("n = ",length(data),sep=""), xlab = "Error")
#      dev.copy(png, paste(filename,".png",sep=""))
#      dev.off()
      #kde <- bkde(x = data)
      #plot(kde, xlab = "Error", ylab = "Density", pch = 16, main = filename)
      #dev.copy(png, paste("KDE",filename,".png",sep=""))
      #dev.off()
#    }
#  }
#}
#percent <- num_correct/num_obs
#outcome <- data.frame(cbind(route,stop,percent))