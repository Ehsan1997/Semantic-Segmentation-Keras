import tensorflow as tf
from keras.layers import Layer
from keras import backend as K

class MaxPooling2DWithIndices(Layer):
    def __init__(self, pool_size, strides, padding='SAME', **kwargs):
        super(MaxPooling2DWithIndices, self).__init__(**kwargs)
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding
        return

    def call(self, x):
        pool_size = self.pool_size
        strides = self.strides
        if isinstance(pool_size, int): ps = [1, pool_size, pool_size, 1]
        else: ps = [1,pool_size[0],pool_size[1],1]
        if isinstance(strides,int): st = [1, strides, strides, 1]
        else: st = [1, strides[0], strides[1], 1]
        mpooled, indices = tf.nn.max_pool_with_argmax(x, ps, st, self.padding)
        return [mpooled, indices]

    def compute_output_shape(self, input_shape):
        if input_shape[1] == None and input_shape[2] == None:
            output_shape = input_shape
        else:
            if isinstance(self.pool_size, int):
                output_shape = (input_shape[0], input_shape[1]//self.pool_size, input_shape[2]//self.pool_size, input_shape[3])
            else: output_shape = (input_shape[0], input_shape[1]//self.pool_size[0], input_shape[2]//self.pool_size[1], input_shape[3])
        return [output_shape, output_shape]

class MaxUnpooling2DWithIndices(Layer):
    def __init__(self, **kwargs):
        super(MaxUnpooling2DWithIndices, self).__init__(**kwargs)
        return
        
    def call(self,x):
        argmax=K.cast(K.flatten(x[1]),'int32')
        max_value=K.flatten(x[0])
        with tf.variable_scope(self.name):
            input_shape=K.shape(x[0])
            batch_size=input_shape[0]
            image_size=input_shape[1]*input_shape[2]*input_shape[3]
            output_shape=[input_shape[0],input_shape[1]*2,input_shape[2]*2,input_shape[3]]
            indices_0=K.flatten(tf.matmul(K.reshape(tf.range(batch_size),(batch_size,1)),K.ones((1,image_size),dtype='int32')))
            indices_1=argmax%(image_size*4)//(output_shape[2]*output_shape[3])
            indices_2=argmax%(output_shape[2]*output_shape[3])//output_shape[3]
            indices_3=argmax%output_shape[3]
            indices=tf.stack([indices_0,indices_1,indices_2,indices_3])
            output=tf.scatter_nd(K.transpose(indices),max_value,output_shape)
            return output

    def compute_output_shape(self, input_shape):
        if input_shape[0][1] == None and input_shape[0][2] == None:
            return (input_shape[0][0], input_shape[0][1], input_shape[0][2], input_shape[0][3])
        else: return (input_shape[0][0], input_shape[0][1]*2, input_shape[0][2]*2, input_shape[0][3])
