from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dropout, concatenate, Conv2DTranspose, BatchNormalization, Activation, LeakyReLU
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.callbacks import ReduceLROnPlateau

def upsample_block(x, filters, kernel_size=(3, 3), padding='same', strides=1):
    x = Conv2DTranspose(filters, kernel_size, padding=padding, strides=strides)(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(alpha=0.1)(x)  # LeakyReLU activation
    return x

def multi_unet_model2(n_classes=4, IMG_HEIGHT=256, IMG_WIDTH=256, IMG_CHANNELS=1):
    inputs = Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))
    s = inputs

    # Contraction path
    c1 = Conv2D(16, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(s)  # Glorot uniform initializer
    c1 = BatchNormalization()(c1)
    c1 = Dropout(0.1)(c1)
    c1 = Conv2D(16, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c1)  # Glorot uniform initializer
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(32, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(p1)  # Glorot uniform initializer
    c2 = BatchNormalization()(c2)
    c2 = Dropout(0.1)(c2)
    c2 = Conv2D(32, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c2)  # Glorot uniform initializer
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(64, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(p2)  # Glorot uniform initializer
    c3 = BatchNormalization()(c3)
    c3 = Dropout(0.2)(c3)
    c3 = Conv2D(64, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c3)  # Glorot uniform initializer
    p3 = MaxPooling2D((2, 2))(c3)

    c4 = Conv2D(128, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(p3)  # Glorot uniform initializer
    c4 = BatchNormalization()(c4)
    c4 = Dropout(0.2)(c4)
    c4 = Conv2D(128, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c4)  # Glorot uniform initializer
    p4 = MaxPooling2D(pool_size=(2, 2))(c4)

    c5 = Conv2D(256, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(p4)  # Glorot uniform initializer
    c5 = BatchNormalization()(c5)
    c5 = Dropout(0.3)(c5)
    c5 = Conv2D(256, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c5)  # Glorot uniform initializer

    # Extra layer with 512 channels
    c6 = Conv2D(512, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c5)  # Glorot uniform initializer
    c6 = BatchNormalization()(c6)
    c6 = Dropout(0.3)(c6)
    c6 = Conv2D(512, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c6)  # Glorot uniform initializer

    # Expansive path
    u6 = upsample_block(c6, 256, strides=(2, 2))
    u6 = concatenate([u6, c4])
    c7 = Conv2D(256, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(u6)  # Glorot uniform initializer
    c7 = BatchNormalization()(c7)
    c7 = Dropout(0.2)(c7)
    c7 = Conv2D(256, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c7)  # Glorot uniform initializer

    u7 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c7)
    u7 = concatenate([u7, c3])
    c8 = Conv2D(128, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(u7)  # Glorot uniform initializer
    c8 = BatchNormalization()(c8)
    c8 = Dropout(0.2)(c8)
    c8 = Conv2D(128, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c8)  # Glorot uniform initializer

    u8 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c8)
    u8 = concatenate([u8, c2])
    c9 = Conv2D(64, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(u8)  # Glorot uniform initializer
    c9 = BatchNormalization()(c9)
    c9 = Dropout(0.1)(c9)
    c9 = Conv2D(64, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c9)  # Glorot uniform initializer

    u9 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c9)
    u9 = concatenate([u9, c1], axis=3)
    c10 = Conv2D(32, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(u9)  # Glorot uniform initializer
    c10 = BatchNormalization()(c10)
    c10 = Dropout(0.1)(c10)
    c10 = Conv2D(32, (3, 3), activation='relu', kernel_initializer=glorot_uniform(), padding='same')(c10)  # Glorot uniform initializer

    outputs = Conv2D(n_classes, (1, 1), activation='softmax')(c10)

    model = Model(inputs=[inputs], outputs=[outputs])



    return model 