'''
《TensorFlow官网教程》
第2章 MNIST
CNN+Softmax MINST手写数字识别
'''

# import mnist dataset:
from tensorflow.examples.tutorials.mnist import input_data
MNIST_data_folder = "F:\DATA\MNIST_data" #数据存放路径
mnist = input_data.read_data_sets("MNIST_data_folder",one_hot=True)

# BUILD THE GRAPH
# ===============================================
import tensorflow as tf

# 交互式Session
sess = tf.InteractiveSession()

# input & output:
x = tf.placeholder("float", shape=[None, 784])
y_ = tf.placeholder("float", shape=[None, 10])

# references interlization:
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# convolution and pooling operation
def conv2d(x,w):
    return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

# Convolution Layer 1:
# ----------------------------------------
W_conv1 = weight_variable([5,5,1,32])
b_conv1 = bias_variable([32])

# reshape x from 2d to 4d
x_image = tf.reshape(x,[-1,28,28,1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

# Convolution Lyaer 2:
# ----------------------------------------
W_conv2 = weight_variable([5,5,32,64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# fully connected layer:
# ---------------------------------------
W_fc1 = weight_variable([7*7*64, 1024])
b_fc1 = bias_variable([1024])
# 将最后池化层的输出展平，变成一个向量
h_pool2_flat = tf.reshape(h_pool2, [-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# Dropout:
# ----------------------------------------
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# Output: Softmax layer:
W_fc2 = weight_variable([1024,10])
b_fc2 = bias_variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# TRAIN THE MODEL
# ==============================================
# cost function: cross entry
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# Intalization the Variables:
sess.run(tf.global_variables_initializer())

for i in range(1000):
    batch = mnist.train.next_batch(100)
    if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_:batch[1],keep_prob:1.0})
        print("step %d , training accuracy %g"%(i,train_accuracy))
    train_step.run(feed_dict={x:batch[0], y_:batch[1],keep_prob:0.5})

# Evaluate the Model
# ================================================
print("test accuracy %g"%accuracy.eval(feed_dict={x:mnist.test.images, y_:mnist.test.labels,keep_prob:1.0}))