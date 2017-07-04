#!/usr/bin/env python
#coding:utf-8

import numpy as np
from matplotlib import pyplot as plt

#よくわかってない.エラーを修正する奴?
def errorGrad(model,data):
    a=model[0]
    b=model[1]
    x=data[:,0]
    y=data[:,1]
    ga=(2*(a*x+b-y)*x).sum()
    gb=(2*(a*x+b-y)).sum()
    return np.array([ga,gb])

#最小二乗法での係数算出
def leastSquare(data):
    tau = 100
    bestfit = None
    besterr = float('inf')
    model = np.zeros(2)
    while tau >= 0.0001:
        for _ in range(10):
            grad = errorGrad(model, data)
            grad /= np.linalg.norm(grad)
            grad *= -1
            model += grad*tau
        tau*=0.1
    return model

#結果を用いた直線を出力
def applyResult(model,x):
    a=model[0]
    b=model[1]
    return a*x+b

#エラー取得?
def getError(model,p):
    x=p[0]
    y=p[1]
    return np.abs(applyResult(model,x)-y)

def getParamWithSamples(samples):
    p0=samples[0]
    p1=samples[1]
    dp = p1-p0
    a=dp[1]/dp[0]
    b=p0[1]-a*p0[0]
    return a,b

#RANSACでの係数算出
def RANSAC(data,choice=2,loop_max=100,threshold=2.0,d=800):
    good_models=[]
    good_model_errors=[]
    iterations=0
    while iterations<loop_max:
        sample = data[np.random.choice(len(data),choice,False)]
        param = getParamWithSamples(sample)
        inliers = []
        for p in data:
            if(p==sample).all(1).any():
                continue
            if getError(param,p)>threshold:
                continue
            else:
                inliers.append(p)

        if len(inliers)>d:
            current_error = np.array([getError(param,p)for p in data]).mean()
            good_models.append(param)
            good_model_errors.append(current_error)

        iterations += 1

    best_index = np.argmin(good_model_errors)
    return good_models[best_index]

#メイン関数
def main():
    print "y=ax+b"
    print "a:"
    _a=input()
    print "b:"
    _b=input()

    points=np.array([[x, _a*x + _b + .1*np.random.randn() + (np.random.randint(100)==0)*np.random.rand()*1000 ]for x in np.arange(0,10,0.01)])
    plt.plot(points[:,0],points[:,1],linestyle=":",color="g")
    
    a,b = leastSquare(points)
    least = np.array([(x,applyResult((a,b),x))for x in points[:,0]])
    plt.plot(least[:,0],least[:,1],linestyle="-",color="y")
    
    a,b = RANSAC(points)
    ransac = np.array([(x,applyResult((a,b),x))for x in points[:,0]])
    plt.plot(ransac[:,0],ransac[:,1],linestyle="-",color="b")

    true = np.array([[x,_a*x+_b]for x in points[:,0]])
    plt.plot(true[:,0],true[:,1],linestyle="--",color="r")
    
    plt.ylim(0,10)
    plt.show()

if __name__=="__main__":
    main()
