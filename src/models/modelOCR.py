import tensorflow as tf

# Model Params
# Height, Width, Channels (for grayscale: 1)
# Input for Synth90K: (32 X 100 X RGB)
input_shape = (32, 100, 3)

# Numbers of unique characters (e.g. letters, digits + special characters)
vocab_size = 80
embedding_dim = 256
units = 512

# Funkcja Attention
class Attention(tf.keras.layers.Layer):
    def __init__(self, units):
        super(Attention, self).__init__()
        self.W1 = tf.keras.layers.Dense(units)
        self.W2 = tf.keras.layers.Dense(units)
        self.V = tf.keras.layers.Dense(1)

    def call(self, features, hidden_state):
        # features shape: (batch_size, num_pixels, embedding_dim)
        # hidden_state shape: (batch_size, units)
        hidden_with_time_axis = tf.expand_dims(hidden_state, 1)
        attention_weights = self.V(
            tf.nn.tanh(self.W1(features) + self.W2(hidden_with_time_axis))
        )
        attention_weights = tf.nn.softmax(attention_weights, axis=1)
        context_vector = attention_weights * features
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights

# Encoder: CNN feature extraction
def build_encoder(input_shape):
    inputs = tf.keras.layers.Input(shape=input_shape)
    
    x = tf.keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same")(inputs)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)
    
    x = tf.keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)
    
    x = tf.keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same")(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)
    
    shape_before_flatten = tf.keras.backend.int_shape(x)
    
    # Reshape to (batch, sequence_length, embedding_dim)
    x = tf.keras.layers.Reshape((shape_before_flatten[1] * shape_before_flatten[2], shape_before_flatten[3]))(x)
    x = tf.keras.layers.Dense(embedding_dim)(x)

    return tf.keras.Model(inputs, x, name="Encoder")

# Decoder with Attention
def build_decoder(vocab_size, embedding_dim, units):
    encoder_output = tf.keras.layers.Input(shape=(None, embedding_dim))
    decoder_hidden_state = tf.keras.layers.Input(shape=(units,))
    decoder_input = tf.keras.layers.Input(shape=(None,))

    embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)(decoder_input)

    # GRU
    x, state = tf.keras.layers.GRU(units, return_sequences=True, return_state=True)(
        embedding, initial_state=decoder_hidden_state
    )

    # Attention Please!
    attention = Attention(units)
    context_vector, _ = attention(encoder_output, state)
    
    # Reshape context vector to match x's time steps
    context_vector = tf.keras.layers.Lambda(
        lambda ctx: tf.expand_dims(ctx, 1),
        output_shape=(1, embedding_dim)
    )(context_vector)
    
    context_vector = tf.keras.layers.Lambda(
        lambda ctx: tf.tile(ctx, [1, tf.shape(x)[1], 1]),
        output_shape=(None, embedding_dim)
    )(context_vector)

    context_vector = tf.keras.layers.Dense(units)(context_vector)
    concat = tf.keras.layers.Concatenate(axis=-1)([context_vector, x])
    outputs = tf.keras.layers.Dense(vocab_size, activation="softmax")(concat)

    return tf.keras.Model(
        inputs=[encoder_output, decoder_hidden_state, decoder_input],
        outputs=outputs,
        name="Decoder"
    )

# Build Model
def build_attention_ocr(input_shape, vocab_size, embedding_dim, units):
    encoder = build_encoder(input_shape)
    decoder = build_decoder(vocab_size, embedding_dim, units)

    # I/O
    encoder_inputs = tf.keras.layers.Input(shape=input_shape)
    decoder_inputs = tf.keras.layers.Input(shape=(None,))
    hidden_state_inputs = tf.keras.layers.Input(shape=(units,))

    encoder_output = encoder(encoder_inputs)
    decoder_output = decoder([encoder_output, hidden_state_inputs, decoder_inputs])

    return tf.keras.Model(inputs=[encoder_inputs, hidden_state_inputs, decoder_inputs], outputs=decoder_output, name="AttentionOCR")

# Compile Model
attention_ocr_model = build_attention_ocr(input_shape, vocab_size, embedding_dim, units)

attention_ocr_model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss="sparse_categorical_crossentropy"
)

attention_ocr_model.summary()