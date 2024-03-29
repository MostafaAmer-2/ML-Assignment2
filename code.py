import numpy as np
import math
import matplotlib.pyplot as plt

def loadTrainingSet():
    images = np.empty([2400, 785])
    for i in range(1, 2401):
        img = plt.imread('./Train/' + str(i) + '.jpg')
        img2 = img.flatten()
        img3 = np.append(img2, 1)
        images[i-1] = img3

    return images

def configureInitialWeightMatrix():
    weights = np.zeros([10, 784])
    ones = np.ones([10, 1])
    return np.hstack((ones, weights))


def perceptron():
    images = loadTrainingSet()
    learning_rates = np.array([1.0, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001, 0.00000001, 0.000000001])

    for n in learning_rates:
        weights = configureInitialWeightMatrix()
        confusionMatrix = np.zeros((10, 10))
        for c in range(10):
            print("Training Class " + str(c))
            # handling targets
            startingTarget = 240 * c  # 1*0, 1*1, 1*2....etc
            target = np.full(2400, -1)
            target[startingTarget:startingTarget + 240] = 1

            for epoch in range(500):
                for img in range(0, 2400):
                    currentImage = images[img]
                    currentTarget = target[img]
                    calculatedTarget = 1 if (np.dot(weights[c], currentImage) >= 0) else -1
                    if (calculatedTarget != currentTarget):
                        weights[c] = weights[c] + (n * currentImage * currentTarget)

        for i in range(1, 201):
            testImg = plt.imread('./Test/' + str(i) + '.jpg')
            testImg = np.append(testImg.flatten(), 1)
            dot = np.dot(weights, testImg)
            index = np.argmax(dot)
            confusionMatrix[((i - 1) // 20)][index] = confusionMatrix[((i - 1) // 20)][index] + 1

        position_n, = np.where(learning_rates == n)
        print("Confusion Matrix - " + str(position_n[0]))
        print(confusionMatrix)
        plt.imshow(confusionMatrix)
        plt.savefig("./Confusion-"+str(position_n[0]) +".jpg")
        # plt.show()

def naive():
    images = loadTrainingSet()
    
    mews = np.zeros([10,784])
    standard_div = np.zeros([10,784])
    for c in range(10):
        mew_c = np.zeros(784)
        for i in range( c*240 , c*240+240):
            mew_c = mew_c + np.true_divide(images[i,:-1],255)
        mews[c] = np.true_divide(mew_c,240)

    for c in range(10):
        std_c = np.zeros(784)
        for i in range( c*240 , c*240+240):
            std_c = std_c + ( pow(np.true_divide(images[i,:-1],255) - mews[c],2) )
        standard_div[c] = np.true_divide( std_c,240 )

    return mews, standard_div
    
def naive_test(filepath, mews, standard_div):
    img = plt.imread(filepath)
    img2 = img.flatten()
    img3 = np.append(img2, 1)
    img3 = np.true_divide(img3[:-1],255)

    probs = np.ones(10)
    for c in range(10):
        for i in range(784):
            std_div = 0.1
            if(standard_div[c,i]>0.1):
                std_div = standard_div[c,i]
            gaussian = gaussian_eq(img3[i], mews[c,i], std_div)
            probs[c] = probs[c]*gaussian
    
    return np.argmax(probs)

    
def gaussian_eq(n, mew, std_div):
    return 1/math.sqrt(2*math.pi*std_div)*math.exp(- ( pow(n - mew,2) ) / ( 2*std_div ) )

def confusionMatrixGenerator(mews, std_div):
    confusionMatrix= np.zeros((10, 10))
    for i in range(1,201):
        testingResult = naive_test('./Test/'+str(i)+'.jpg', mews, std_div)
        confusionMatrix[((i-1)//20), testingResult] += 1

    print(confusionMatrix)
    plt.imshow(confusionMatrix)
    plt.savefig("./Confusion-Gauss.jpg")
    plt.show()

    return confusionMatrix

if __name__ == "__main__":

    # Question 1
    perceptron()

    # Question 2
    # mews, standard_div = naive()
    # confusionMatrixGenerator(mews, standard_div)

    weight = [1, 2, 1]
    weight = np.array(weight)








