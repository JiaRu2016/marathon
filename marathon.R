
rm(list = ls())

require(rvest)
require(stringr)
require(plyr)

urlfile <- "urls_2000_3001.txt"
ab <- unlist(str_extract_all(urlfile, pattern = "\\d{4}"))
a <- ab[1]
b <- ab[2]
data <- read.table(file = urlfile, header = FALSE, sep="\t", 
                   col.names = c("ID", "url"), stringsAsFactors = F)
# 定义函数：
# x: url
# y: 成绩信息(三个)

GetInfo <- function(ID,url) {
  if (str_detect(string=url, pattern = "sorry")) {
    return(c("ID"=ID, "name"="***", "time"="None", "rank"="None", "url"=url))
  }
  page <- read_html(url)
  name <- 
    html_nodes(page, css = ".name") %>%
    html_text(trim = TRUE) %>%
    str_replace(pattern = "\r\n\t\t\t\r\n\t\t\t选手成功完赛", replacement = "")
  time <- 
    html_nodes(page, css = ".time") %>%
    html_text()
  rank <- 
    html_nodes(page, css = ".ranking") %>%
    html_text()
  
  return(c("ID"=ID, "name"=name, "time"=time, "rank"=rank, "url"=url))
}

# 写文件
infofile <- paste0("info_",a,"_",b,".txt")
file.create(infofile)

for (i in 1:nrow(data)) {
  info <- GetInfo(data[i,1],data[i,2])
  cat(info,sep = "\t", file = infofile, append=T)
  cat("\n",file = infofile, append=T)
  message(round(i/nrow(data)*100),"% completed ...")
}


#######################################
# 分析数据

data3 <- read.table(file = infofile, header = FALSE, sep="\t", 
                   col.names = c("ID", "name", "time", "rank", "url"), 
                   stringsAsFactors = F)
data3$rank <- as.numeric(data3$rank)
View(data3)

##################################
# 生成姓名集合
names <- read.table("nameset.txt",sep="a")
names <- as.character(names[,1])
names <- str_replace(names, pattern = "(.+)\t2(.+)", replacement = "\\1")
nameset <- names
# 
data_wise <- subset(data3, name %in% nameset)
View(data_wise)



