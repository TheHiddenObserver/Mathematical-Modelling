# t检验
t_test<-function(x,mu0,ha='two-sided',alpha){
  n<-length(x)
  mu<-mean(x)
  s<-sd(x)
  result=list()
  if(ha=="two-sided"){
    cr<-paste(-Inf,mu0-qt(1-alpha/2,n-1)*s/sqrt(n),'&',mu0+qt(1-alpha/2,n-1)*s/sqrt(n),Inf)
    ci<-paste(mu-qt(1-alpha/2,n-1)*s/sqrt(n),mu+qt(1-alpha/2,n-1)*s/sqrt(n))
    test<-(mu-mu0)/(s/sqrt(n))
    p_value<-(1-pt(abs(test),n-1))*2
  }
  if(ha=="greater"){
    cr<-paste(mu0+qt(1-alpha,n-1)*s/sqrt(n),Inf)
    ci<-paste(mu-qt(1-alpha,n-1)*s/sqrt(n),Inf)
    test<-(mu-mu0)/(s/sqrt(n))
    p_value<-(1-pt(test,n-1))
  }
  if(ha=="less"){
    cr<-paste(-Inf,mu0-qt(1-alpha,n-1)*s/sqrt(n))
    ci<-paste(-Inf,mu+qt(1-alpha,n-1)*s/sqrt(n))
    test<-(mu-mu0)/(s/sqrt(n))
    p_value<-pt(test,n-1)
  }
  result$mean<-mu
  result$critical_region<-cr
  result$confidence_interval<-ci
  result$statistic<-test
  result$p_value<-p_value
  return(result)
}

# 测试数据
x<-rnorm(100,mean=15,sd=5)
t_test(x,10,ha="greater",0.05)
t.test(x,y=NULL,mu=10,"greater",conf.level = 0.95)

# 两样本t检验
twosample_t_test<-function(x,y,varequal = FALSE,h1='two-sided',alpha=0.05)
{
  sx<-sd(x)
  sy<-sd(y)
  n<-length(x)
  m<-length(y)
  mux<-mean(x)
  muy<-mean(y)
  sp=sqrt(((n-1)*var(x)+(m-1)*var(y))/(n+m-2))
  result=list()
  if(varequal==FALSE)
  {
    df<-(sx^2/n+sy^2/m)^2/((sx^2/n)^2/(n-1)+(sy^2/m)^2/(m-1))
    demo<-sqrt(sx^2/n+sy^2/m)
  }
  else
  {
    df<-n+m-2
    demo<-sp*sqrt(1/n+1/m)
  }
  test<-(mux-muy)/demo
  if(h1=="two-sided"){
    cr<-paste(-Inf,-qt(1-alpha/2,df)*demo,'&',qt(1-alpha/2,df)*demo,Inf)
    ci<-paste(mux-muy-qt(1-alpha/2,df)*demo,mux-muy+qt(1-alpha/2,df)*demo)
    p_value<-(1-pt(abs(test),df))*2
  }
  if(h1=="greater"){
    cr<-paste(qt(1-alpha,df)*demo,Inf)
    ci<-paste(mux-muy-qt(1-alpha,df)*demo,Inf)
    p_value<-(1-pt(test,df))
  }
  if(h1=="less"){
    cr<-paste(-Inf,-qt(1-alpha,df)*demo)
    ci<-paste(-Inf,mux-muy+qt(1-alpha,df)*demo)
    p_value<-pt(test,df)
  }
  result$meanx<-mux
  result$meany<-muy
  result$df<-df
  result$critical_region<-cr
  result$confidence_interval<-ci
  result$statistic<-test
  result$p_value<-p_value
  return(result)
}

# 测试数据
x<-rnorm(100,20,5)
y<-rnorm(50,15,5)
twosample_t_test(x,y,varequal = TRUE)

# 与R语言自带的函数比较
t.test(x,y,var.equal = TRUE)

# 独立性检验
independence_test<-function(x,alpha=0.05)
{
  r<-nrow(x)
  c<-ncol(x)
  n<-sum(x)
  df=(r-1)*(c-1)
  result<-list()
  rsum<-as.matrix(rowSums(x))
  csum<-as.matrix(colSums(x))
  exp<-rsum%*%t(csum)/n
  test<-sum((x-exp)^2/exp)
  cr<-paste(qchisq(1-alpha,df),Inf)
  p_value<-(1-pchisq(test,df))
  result$df<-df
  result$statistic<-test
  result$critical_region<-cr
  result$p_value<-p_value
  return(result)
}

# 测试数据
x<-matrix(c(1481,1111,78,81,375,425,399,268),ncol = 2,byrow = TRUE)
independence_test(x)

# 与自带的函数比较
chisq.test(x)
