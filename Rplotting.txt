setwd('c:/nba/')
csvfiles<-"c:/nba/hotcolddata.csv"
MyData <- read.csv(file=csvfiles, header=TRUE, sep=",")
dfp<-data.frame(MyData$'percent.all',MyData$'percent.hot',MyData$'percent.cold')
dfp <- setNames(dfp, c("all","hot","cold"))
dfps <- stack(dfp)
dfps<-setNames(dfps, c("shot.successrate","shot.type"))

myColors<-c("green","blue","red")
m <- ggplot(dfps, aes(x=shot.successrate))
m <- m + geom_density(aes(fill=factor(shot.type)), size=0.01, alpha=.25) + 
  scale_fill_manual(values=myColors)+theme_classic(base_size = 10, base_family = "Helvetica")+labs(x = "shot success rate", y = "density")
tiff("plot1.tiff",width = 900, height = 900, res = 200)
m
dev.off()
##densityplot for shooting percentage
##dot plot range vs hot-diff and cold-diff
library(reshape)
dfp2<-data.frame(MyData$'range',MyData$'range.diff.hot',MyData$'range.diff.cold')
dfp2<-setNames(dfp2, c("range","hot","cold"))
dfpm <- melt(dfp2, id.vars = "range")
dfpm<-setNames(dfpm, c("range","shot.type","diff"))
myr <- lm(diff ~ shot.type*range, data = dfpm)
tiff("plot2.tiff",width = 900, height = 900, res = 200)
p<-ggplot(dfpm, aes(range, diff, colour = shot.type)) +
  geom_point() +
  scale_colour_manual(values = c("red", "blue"))+theme_classic(base_size = 10, base_family = "Helvetica")+labs(x = "average shot distance (feet)", y = "shot distance shift (feet)")+geom_smooth(method="lm", se=FALSE)
p
dev.off()
