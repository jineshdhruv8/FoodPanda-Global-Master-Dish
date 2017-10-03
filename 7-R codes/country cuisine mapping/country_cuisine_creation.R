
library(stringr)
library(stringdist)
library(data.table)

#### trim function
trim <- function(x) return(tolower(str_trim(gsub("^ *|(?<= ) | *$", "", x, perl=T))))

#country_id <- 39

#### cuisine modification function

cuisine_modification_fn <- function(cuisne_mapping,country_subcui_subcat_file,country_id){

country_cuisine_mapping <- cuisne_mapping[which(cuisne_mapping$country_id==country_id),]
#unique(country_cuisine_mapping$cuisine)

country_cuisine_mapping$cuisine<-factor(country_cuisine_mapping$cuisine)
#unique(country_subcui_subcat_file$vendor_id)

column_names <- colnames(country_cuisine_mapping)

vendor_dish <- data.frame(tapply(X=country_subcui_subcat_file$vendor_id,INDEX=as.factor(country_subcui_subcat_file$vendor_id),FUN=length))
vendor_dish <- cbind(row.names(vendor_dish),vendor_dish)
names(vendor_dish)[1:2] <- paste(c("vendor_id","dishes"))

cuisine_analysis <- merge(country_cuisine_mapping,vendor_dish,by="vendor_id",all.x=TRUE)
cuisine_analysis$dishes[which(is.na(cuisine_analysis$dishes))]<-0

cuisine_modification_output <- data.frame(data.table(cuisine_analysis)[,list(count=length(vendor_id),sum_dishes=sum(dishes)),by="cuisine"])

write.csv(cuisine_modification_output,file='manual_modification.csv',row.names=FALSE)

}

cuisne_mapping <- read.csv("vendor_to_cuisine_all_countries.csv")
#colnames(cuisne_mapping)
#cuisne_mapping <- read.csv(file.choose(),header=TRUE)

if(ncol(cuisne_mapping)>6){
  cuisne_mapping <- cuisne_mapping[,c(1:4,6:7)]
  names(cuisne_mapping)[1:6]<- paste(c("country_id","country","vendor","vendor_id","cuisine","cuisine_id"))
}


file.remove("manual_modification.csv")

country_subcui_subcat_file <- read.csv(file.choose(),header=TRUE)

print("enter country_id")

cuisine_modification_fn(cuisne_mapping,country_subcui_subcat_file,28)


#############
## cuisine file creation
#############


cuisine_creation_fn <- function(country,country_id){

manual_modification <- read.csv("manual_modification.csv")
names(manual_modification)[ncol(manual_modification)]<- paste("cuisine_modification")
manual_modification <- manual_modification[,c("cuisine","cuisine_modification")]

#colnames(manual_modification)

country_cuisine_mapping <- cuisne_mapping[which(cuisne_mapping$country_id==country_id),]
#colnames(country_cuisine_mapping)

cuisine_creation <- merge(country_cuisine_mapping,manual_modification,by="cuisine")

#head(cuisine_creation)

cuisine_creation <- cuisine_creation[which(cuisine_creation$cuisine_modification!=""),]
cuisine_creation <- cuisine_creation[,c("vendor_id","cuisine_modification")]
cuisine_creation <-unique(cuisine_creation[,c("vendor_id","cuisine_modification")])

cuisine_creation$vendor_id<-factor(cuisine_creation$vendor_id)

cuisine_count <- data.frame(tapply(X=cuisine_creation$vendor_id,INDEX=as.factor(cuisine_creation$vendor_id),FUN=length))
cuisine_count <- cbind(row.names(cuisine_count),cuisine_count)
names(cuisine_count)[1:2] <- paste(c("vendor_id","count"))

cuisine_creation <- merge(cuisine_creation,cuisine_count,by="vendor_id")

cuisine_creation$final_cuisine <- ifelse(cuisine_creation$count > 1,paste("multi_",as.character(cuisine_creation$cuisine_modification),sep=""),as.character(cuisine_creation$cuisine_modification))

#colnames(cuisine_creation)

cuisine_creation <- cuisine_creation[,c("vendor_id","final_cuisine")]
names(cuisine_creation)[ncol(cuisine_creation)]<- paste("cuisine")


write.csv(cuisine_creation,file=paste(country,"_cuisine.csv",sep=""),row.names=FALSE)

}

check <-cuisne_mapping[which(cuisne_mapping$country_id==28),]

cuisine_creation_fn("Ukraine",28)


#### for translation

country_cuisine_mapping <- cuisne_mapping[which(cuisne_mapping$country_id==40),]
write.csv(country_cuisine_mapping,file="Serbia_translation.csv",row.names=FALSE)
