


library(stringr)
library(stringdist)
library(data.table)

#### trim function
trim <- function(x) return(tolower(str_trim(gsub("^ *|(?<= ) | *$", "", x, perl=T))))


compression_collation1_fn <- function(country_id){

#compression_output <- read.csv(file.choose(),header=TRUE)
compression_output <- read.csv(paste(country_id,"_compress_output.csv",sep=""),header=TRUE)

#colnames(compression_output)
names(compression_output)[1:ncol(compression_output)]<-paste(c("Masterdish","cuisine_compressed","cuisine_ratio","subcuisine_compressed",
                                                               "subcuisine_ratio","subcategory_compressed","subcategory_ratio"))

compression_output <- compression_output[which(compression_output$Masterdish!=""),]

masterdish <- read.csv(paste('C:/Users/Rohit/Desktop/codes/compression file/masterdish_files/masterdish_final_',country_id,'.csv',sep=""),header=TRUE)

column_names <- colnames(masterdish)

merged <- merge(masterdish,compression_output,by="Masterdish",all.x=TRUE)

#### cuisine

merged$new_cuisine <- ifelse(merged$Cuisine=="" & merged$cuisine_compressed!="",as.character(merged$cuisine_compressed),as.character(merged$Cuisine))
merged$new_flag <- ifelse(merged$Cuisine=="" & merged$cuisine_compressed!="",5,merged$cuisine_flag)

merged <- merged[,!(names(merged) %in% c("Cuisine","cuisine_flag","cuisine_compressed","cuisine_ratio"))]
names(merged)[which(names(merged)=="new_cuisine")] <- paste("Cuisine")
names(merged)[which(names(merged)=="new_flag")] <- paste("cuisine_flag")

merged$cuisine_flag[which(is.na(merged$cuisine_flag))] <- ""

###### subcuisine

merged$new_subcuisine <- ifelse(merged$Subcuisine=="" & merged$subcuisine_compressed!="",as.character(merged$subcuisine_compressed),as.character(merged$Subcuisine))
merged$new_flag <- ifelse(merged$Subcuisine=="" & merged$subcuisine_compressed!="",2,ifelse(merged$Subcuisine=="" & merged$subcuisine_compressed=="","",1))

merged <- merged[,!(names(merged) %in% c("Subcuisine","subcuisine_compressed","subcuisine_ratio"))]
names(merged)[which(names(merged)=="new_subcuisine")] <- paste("Subcuisine")
names(merged)[which(names(merged)=="new_flag")] <- paste("subcuisine_flag")

column_names_nw <- c(column_names[1:which(column_names=="Subcuisine")],"subcuisine_flag",column_names[(which(column_names=="Subcuisine")+1):length(column_names)],"subcategory_flag")

##### subcategory

merged$new_subcategory <- ifelse(merged$Subcategory=="" & merged$subcategory_compressed!="",as.character(merged$subcategory_compressed),as.character(merged$Subcategory))
merged$new_flag <- ifelse(merged$Subcategory=="" & merged$subcategory_compressed!="",2,ifelse(merged$Subcategory=="" & merged$subcategory_compressed=="","",1))

merged <- merged[,!(names(merged) %in% c("Subcategory","subcategory_compressed","subcategory_ratio"))]
names(merged)[which(names(merged)=="new_subcategory")] <- paste("Subcategory")
names(merged)[which(names(merged)=="new_flag")] <- paste("subcategory_flag")

merged$Cuisine[which(is.na(merged$Cuisine))] <- ""
merged$Subcuisine[which(is.na(merged$Subcuisine))] <- ""
merged$Subcategory[which(is.na(merged$Subcategory))] <- ""
merged$subcuisine_flag[which(is.na(merged$subcuisine_flag))] <- ""
merged$subcategory_flag[which(is.na(merged$subcategory_flag))] <- ""

merged <- merged[,column_names_nw]

merged <- merged[order(merged$Count),]

write.csv(merged,file=paste('C:/Users/Rohit/Desktop/codes/compression file/final_files/final_output_',country_id,'.csv',sep=""),row.names=FALSE)

}

input_country_ids<- read.csv(file.choose(),header=TRUE)

for(i in 1:nrow(input_country_ids)){
  print(i)
  compression_collation1_fn(as.character(input_country_ids[i,1]))
}
