
#####################
### cuisine classification
#####################

### for those masterdishes which are served by a single serving resturant or single as well as mutltiple serveing resturant


library(stringr)
library(stringdist)

#### trim function
trim <- function(x) return(tolower(str_trim(gsub("^ *|(?<= ) | *$", "", x, perl=T))))

cuisine_fn <- function(rest_cuisine,country_id){

data <- read.csv(paste("C:/Users/Rohit/Desktop/codes/wine and juice cleaning/wine_juice_output_",country_id,".csv",sep=""),header=TRUE)
#colnames(data)
names(data)[2]<-paste("vendor_id")


column_names_data<-colnames(data)

data_orignal <- data

#colnames(rest_cuisine)
rest_cuisine <- unique(rest_cuisine[,c("vendor_id","cuisine")])


data<- merge(data,rest_cuisine,by="vendor_id")

data$Masterdish<-factor(data$Masterdish)

data$flag <- as.numeric(grepl(pattern="\\bmulti_",x=data$cuisine))

data$parent <-gsub(pattern="\\bmulti_",
                           replacement="",x=data$cuisine)

data$cuisine_identifer<-ifelse(data$flag==1,"",data$parent)

data$multi_cuisine_identifier <-ifelse(data$flag==0,"",data$parent)

md_present_sngl_cuisine_rest_fn <- function(x){
  x<-x[which(x!="")]
  len<-length(unique(x))
  if(len==1){output<-unique(x)
  }else{
    output<-""
  }  
}

md_present_sngl_cuisine_rest<-data.frame(tapply(X=data$cuisine_identifer,INDEX=as.factor(data$Masterdish),FUN=md_present_sngl_cuisine_rest_fn))

md_present_sngl_cuisine_rest <- cbind(row.names(md_present_sngl_cuisine_rest),md_present_sngl_cuisine_rest)

names(md_present_sngl_cuisine_rest)[1:2]<-paste(c("Masterdish","multi_cuisine_identifier"))

count_mutli_cuisine_fn <- function(x){
  x<-x[which(x==1)]
  len <- length(x)
  if(len==0){
    flag=1
  }else{
    flag=0
  }
}

mutli_serving_flg<-data.frame(tapply(X=data$flag,INDEX=as.factor(data$Masterdish),FUN=count_mutli_cuisine_fn))

mutli_serving_flg <- cbind(row.names(mutli_serving_flg),mutli_serving_flg)

names(mutli_serving_flg)[1:2]<-paste(c("Masterdish","flag"))

final <- merge(md_present_sngl_cuisine_rest,mutli_serving_flg,by="Masterdish")

dishes1<- final[which(final$flag==1),c("Masterdish","multi_cuisine_identifier")]

final2<- final[which(final$flag==0),c("Masterdish","multi_cuisine_identifier")]

data1<-data[which(data$multi_cuisine_identifier!=""),]


dishes2<-merge(data1,final2,by=c("Masterdish","multi_cuisine_identifier"))

dishes2<-dishes2[,c("Masterdish","multi_cuisine_identifier")]

dishes2<- unique(dishes2[,c("Masterdish","multi_cuisine_identifier")])

dishes <- rbind(dishes1,dishes2)

names(dishes)[2]<-paste("cuisine_classification_2")

data<-data_orignal

data2<-merge(data,dishes,by="Masterdish",all.x=TRUE)


##########
## Cuisine classification 3
#########

##### resturant serving single cuisine then all the masterdish of that resturant is classified as cuisine of that resturtant

single_serving_rest <- data.frame(tapply(X=rest_cuisine$vendor_id,INDEX=rest_cuisine$vendor_id,FUN=length))

single_serving_rest <- cbind(row.names(single_serving_rest),single_serving_rest)
names(single_serving_rest)[1:2]<-paste(c("vendor_id","length"))

single_serving_rest <- single_serving_rest[which(single_serving_rest$length==1),]

single_serving_rest <- merge(rest_cuisine,single_serving_rest,by="vendor_id")

names(single_serving_rest)[2]<-paste("cuisine3")

single_serving_rest <- single_serving_rest[which(single_serving_rest$cuisine3!="dessert"),]

single_serving_rest <- single_serving_rest[,c("vendor_id","cuisine3")]

data3<-merge(data2,single_serving_rest,by="vendor_id",all.x=TRUE)

#colnames(data3)


data3$cuisine_classification_2[which(is.na(data3$cuisine_classification_2))] <- ""


levels(data3$cuisine3)<-c(levels(data3$cuisine3),"")

data3$cuisine3[which(is.na(data3$cuisine3))]<-""

data3$cuisine_upto_3 <- ifelse(data3$Cuisine=="" & data3$cuisine_classification_2=="",as.character(data3$cuisine3),ifelse(data3$Cuisine=="" & data3$cuisine_classification_2!="",as.character(data3$cuisine_classification_2),as.character(data3$Cuisine)))
data3$cuisine_flag <- ifelse(data3$Cuisine=="" & data3$cuisine_classification_2=="",3,ifelse(data3$Cuisine=="" & data3$cuisine_classification_2!="",2,1))

#################
### cuisine classification 4
################
data3_orignal <- data3

data3 <- data3[which(data3$cuisine_upto_3!="alcoholic beverages"),]
data3 <- data3[which(data3$cuisine_upto_3!="non-alcoholic beverages"),]
data3 <- data3[which(data3$cuisine_upto_3!="dessert"),]

#### on the basis of max cuisine served by a resturant all other dishes are tagged as that cuisine
data3$vendor_id<-factor(data3$vendor_id)
#head(data3)
#colnames(data3)

cuisine4_temp<- data.frame(tapply(X=data3$cuisine_upto_3,INDEX=data3$vendor_id,FUN=length))
cuisine4_temp<-cbind(row.names(cuisine4_temp),cuisine4_temp)
names(cuisine4_temp)[1:2]<-paste(c("vendor_id","count"))

cuisine4<-data.frame(tapply(X=data3$cuisine_upto_3,INDEX=list(data3$vendor_id,data3$cuisine_upto_3),FUN=length))

column_names<-colnames(cuisine4)

if("V1" %in% column_names){
  flag=TRUE
}else{
  flag=FALSE
}

if(flag==TRUE){
  lower=3
}else{
  lower=2
}


column_names<-column_names[which(column_names!="V1")]

cuisine4<-cbind(row.names(cuisine4),cuisine4)
number_of_column <- ncol(cuisine4)
names(cuisine4)[1]<-paste(c("vendor_id"))

if(flag==TRUE){cuisine4 <- cuisine4[,c("vendor_id","V1",column_names)];
               names(cuisine4)[1:2]<-paste(c("vendor_id","blanks"));
}

cuisine4[is.na(cuisine4)]<-0

cuisine4 <- merge(cuisine4,cuisine4_temp,by="vendor_id")

if(flag==TRUE){
  cuisine4$count_without_blanks<-cuisine4$count-cuisine4$blanks
}else{
  cuisine4$count_without_blanks <- cuisine4$count
}


cuisine4$max <- apply(X=cuisine4[,lower:number_of_column],MARGIN=1,FUN=max)

cuisine4$cuisine4 <-names(cuisine4)[apply(X=cuisine4[,lower:number_of_column],MARGIN= 1, function(x) match(max(x),x))+(lower-1)]

cuisine4$percentage_filter <- cuisine4$max/cuisine4$count_without_blanks

cuisine4$count_max_occurance <- apply(X=cuisine4[,lower:number_of_column],1,FUN=function(x) length(which(x==max(x))))

cuisine4$cuisine4_final<-ifelse((cuisine4$count_without_blanks>=5 & cuisine4$percentage_filter>=0.5 & cuisine4$count_max_occurance==1),as.character(cuisine4$cuisine4),"")

cuisine4 <- cuisine4[,c("vendor_id","cuisine4_final")]
names(cuisine4)[2]<-paste("cuisine4")

data4<- merge(data3_orignal,cuisine4,by="vendor_id",all.x=TRUE)

data4$final_cuisine <- ifelse(data4$cuisine_upto_3=="",as.character(data4$cuisine4),as.character(data4$cuisine_upto_3))
data4$cuisine_flag <- ifelse(data4$cuisine_upto_3=="",4,data4$cuisine_flag)
data4$cuisine_flag <- ifelse(data4$final_cuisine=="","",data4$cuisine_flag)


data4 <- data4[order(data4$Count),]

data4 <- data4[,!(names(data4) %in% c("Cuisine"))]

names(data4)[which(names(data4)=="final_cuisine")] <- paste("Cuisine")

column_names_data_nw <- c(column_names_data[1:which(column_names_data=="Cuisine")],"cuisine_flag",column_names_data[(which(column_names_data=="Cuisine")+1):length(column_names_data)])

data4 <- data4[,(names(data4) %in% column_names_data_nw)]

data4<-data4[,column_names_data_nw]

data4$Cuisine <- ifelse(data4$Cuisine=="dessert" & data4$Subcategory!="dessert","",as.character(data4$Cuisine))

write.csv(data4,file=paste("masterdish_final_",country_id,".csv",sep=""),row.names=FALSE)
}
################

rest_cuisine <- read.csv(file.choose(),header=TRUE)

cuisine_fn(rest_cuisine,"ua")
