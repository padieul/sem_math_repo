import tensorflow as tf
import keras_tuner as kt

import io
from pathlib import Path

# Models and Model Builder functions for multiclassification experiments

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#  LOGISTIC REGRESSION
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------
# 1. TOKENS
#-------------------------------------------------------------------------------------------------------------------

# returns model graph: FEATURES: TOKENS
#
def create_model1_LR(num_classes, emb_dim, dp1, dp2, tokens_encoder, tokens_size, add_inp_emb_dim=1):
    embedding_input_dim = tokens_size + add_inp_emb_dim

    tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    tokens_vectorized = tokens_encoder(tokens_model_input)

    embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                        output_dim=emb_dim,
                                        # user masking to handle the variable sequence lengths
                                        mask_zero=True)(tokens_vectorized)
    
    dropout1 = tf.keras.layers.Dropout(dp1)(embedded)
    globalmaxpooling = tf.keras.layers.GlobalMaxPooling1D()(dropout1)
    dropout2 = tf.keras.layers.Dropout(dp2)(globalmaxpooling)
    model_output = tf.keras.layers.Dense(num_classes)(dropout2)

    model = tf.keras.models.Model(inputs=tokens_model_input, outputs=model_output)
        
    return model



# returns model builder: FEATURES: TOKENS
#
def create_model_builder1_LR(num_classes, tokens_encoder, tokens_size, add_inp_emb_dim=1):

    def model_builder(hp):
        
        embedding_input_dim = tokens_size + add_inp_emb_dim 

        tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        tokens_vectorized = tokens_encoder(tokens_model_input)


        hp_emb_dims = hp.Int('emb_dims', min_value=32, max_value=128, step=32)
        embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                            output_dim=hp_emb_dims,
                                            # user masking to handle the variable sequence lengths
                                            mask_zero=True)(tokens_vectorized)
    
        hp_do1 = hp.Choice('dropout1', values=[0.1, 0.2, 0.3])
        dropout1 = tf.keras.layers.Dropout(hp_do1)(embedded)
        globalmaxpooling = tf.keras.layers.GlobalMaxPooling1D()(dropout1)

        hp_do2 = hp.Choice('dropout2', values=[0.1, 0.2, 0.3])
        dropout2 = tf.keras.layers.Dropout(hp_do2)(globalmaxpooling)
        model_output = tf.keras.layers.Dense(num_classes)(dropout2)

        model = tf.keras.models.Model(inputs=tokens_model_input, outputs=model_output)
        
        hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(hp_learning_rate),
              metrics=["accuracy", tf.keras.metrics.Recall()])
        return model
    
    return model_builder

#-------------------------------------------------------------------------------------------------------------------
# 2. TYPES
#-------------------------------------------------------------------------------------------------------------------

# returns model graph: FEATURES: TYPES
#
def create_model2_LR(num_classes, emb_dim, dp1, dp2, types_encoder, types_size, add_inp_emb_dim=1):
    embedding_input_dim = types_size + add_inp_emb_dim 

    types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    types_vectorized = types_encoder(types_model_input)

    embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                        output_dim=emb_dim,
                                        # user masking to handle the variable sequence lengths
                                        mask_zero=True)(types_vectorized)
    
    dropout1 = tf.keras.layers.Dropout(dp1)(embedded)
    globalmaxpooling = tf.keras.layers.GlobalMaxPooling1D()(dropout1)
    dropout2 = tf.keras.layers.Dropout(dp2)(globalmaxpooling)
    model_output = tf.keras.layers.Dense(num_classes)(dropout2)

    model = tf.keras.models.Model(inputs=types_model_input, outputs=model_output)
        
    return model



# returns model builder: FEATURES: TYPES
#
def create_model_builder2_LR(num_classes, types_encoder, types_size, add_inp_emb_dim=1):

    def model_builder(hp):
        embedding_input_dim = types_size + add_inp_emb_dim 

        types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        types_vectorized = types_encoder(types_model_input)

        hp_emb_dims = hp.Int('emb_dims', min_value=32, max_value=128, step=32)
        embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                            output_dim=hp_emb_dims,
                                            # user masking to handle the variable sequence lengths
                                            mask_zero=True)(types_vectorized)
    
        hp_do1 = hp.Choice('dropout1', values=[0.1, 0.2, 0.3])
        dropout1 = tf.keras.layers.Dropout(hp_do1)(embedded)
        globalmaxpooling = tf.keras.layers.GlobalMaxPooling1D()(dropout1)

        hp_do2 = hp.Choice('dropout2', values=[0.1, 0.2, 0.3])
        dropout2 = tf.keras.layers.Dropout(hp_do2)(globalmaxpooling)
        model_output = tf.keras.layers.Dense(num_classes)(dropout2)

        model = tf.keras.models.Model(inputs= types_model_input, outputs=model_output)
        
        hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(hp_learning_rate),
              metrics=["accuracy", tf.keras.metrics.Recall()])
        return model
    
    return model_builder

#-------------------------------------------------------------------------------------------------------------------
# 3. TOKENS + TYPES
#-------------------------------------------------------------------------------------------------------------------

# returns model graph: FEATURES: TOKENS, TYPES
#
def create_model3_LR(num_classes, emb_dim, dp1, dp2, tokens_encoder, types_encoder, tokens_size, types_size, add_inp_emb_dim=1):
    embedding_input_dim = tokens_size + types_size + add_inp_emb_dim

    tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    tokens_vectorized = tokens_encoder(tokens_model_input)

    types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    types_vectorized = types_encoder(types_model_input)

    merged = tf.keras.layers.Concatenate(axis=1)([tokens_vectorized, types_vectorized])
    embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                        output_dim=emb_dim,
                                        # user masking to handle the variable sequence lengths
                                        mask_zero=True)(merged)
    
    dropout1 = tf.keras.layers.Dropout(dp1)(embedded)
    globalmaxpooling = tf.keras.layers.GlobalMaxPooling1D()(dropout1)
    dropout2 = tf.keras.layers.Dropout(dp2)(globalmaxpooling)
    model_output = tf.keras.layers.Dense(num_classes)(dropout2)

    model = tf.keras.models.Model(inputs=[tokens_model_input, types_model_input], outputs=model_output)
        
    return model



# returns model builder: FEATURES: TOKENS, TYPES
#
def create_model_builder3_LR(num_classes, tokens_encoder, types_encoder, tokens_size, types_size, add_inp_emb_dim=1):

    def model_builder(hp):
        embedding_input_dim = tokens_size + types_size + add_inp_emb_dim + 3 # 3 size of sem_type_model_input

        tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        tokens_vectorized = tokens_encoder(tokens_model_input)

        types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        types_vectorized = types_encoder(types_model_input)

        merged = tf.keras.layers.Concatenate(axis=1)([tokens_vectorized, types_vectorized])

        hp_emb_dims = hp.Int('emb_dims', min_value=32, max_value=128, step=32)
        embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                            output_dim=hp_emb_dims,
                                            # user masking to handle the variable sequence lengths
                                            mask_zero=True)(merged)
    
        hp_do1 = hp.Choice('dropout1', values=[0.1, 0.2, 0.3])
        dropout1 = tf.keras.layers.Dropout(hp_do1)(embedded)
        globalmaxpooling = tf.keras.layers.GlobalMaxPooling1D()(dropout1)

        hp_do2 = hp.Choice('dropout2', values=[0.1, 0.2, 0.3])
        dropout2 = tf.keras.layers.Dropout(hp_do2)(globalmaxpooling)
        model_output = tf.keras.layers.Dense(num_classes)(dropout2)

        model = tf.keras.models.Model(inputs=[tokens_model_input, types_model_input], outputs=model_output)
        
        hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(hp_learning_rate),
              metrics=["accuracy", tf.keras.metrics.Recall()])
        return model
    
    return model_builder

#-------------------------------------------------------------------------------------------------------------------
# 4. TOKENS + TYPES + MATH_TYPES
#-------------------------------------------------------------------------------------------------------------------

# returns model graph: ALL FEATURES: TOKENS, TYPES, MATH_TYPES
#
def create_model4_LR(num_classes, emb_dim, dp1, dp2, tokens_encoder, types_encoder, tokens_size, types_size, input_type, add_inp_emb_dim=1):
    embedding_input_dim = tokens_size + types_size + add_inp_emb_dim + 3 # 3 size of sem_type_model_input

    tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    tokens_vectorized = tokens_encoder(tokens_model_input)

    types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    types_vectorized = types_encoder(types_model_input)

    if input_type == "float":
        sem_type_model_input = tf.keras.layers.Input(dtype=tf.float32, shape=(3,))
    elif input_type == "int":
        sem_type_model_input = tf.keras.layers.Input(dtype=tf.int64, shape=(3,))

    merged = tf.keras.layers.Concatenate(axis=1)([tokens_vectorized, types_vectorized, sem_type_model_input])
    embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                        output_dim=emb_dim,
                                        # user masking to handle the variable sequence lengths
                                        mask_zero=True)(merged)
    
    dropout1 = tf.keras.layers.Dropout(dp1)(embedded)
    globalmaxpooling = tf.keras.layers.GlobalMaxPooling1D()(dropout1)
    dropout2 = tf.keras.layers.Dropout(dp2)(globalmaxpooling)
    model_output = tf.keras.layers.Dense(num_classes)(dropout2)

    model = tf.keras.models.Model(inputs=[tokens_model_input, types_model_input, sem_type_model_input], outputs=model_output)
        
    return model



# returns model builder: ALL FEATURES: TOKENS, TYPES, MATH_TYPES
#
def create_model_builder4_LR(num_classes, tokens_encoder, types_encoder, tokens_size, types_size, input_type, add_inp_emb_dim=1):

    def model_builder(hp):
        ...
        # model = create_model(encoder_count_tokens, encoder_count_types,tokens_input_len, "float", type_input_len)
        embedding_input_dim = tokens_size + types_size + add_inp_emb_dim + 3 # 3 size of sem_type_model_input

        tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        tokens_vectorized = tokens_encoder(tokens_model_input)

        types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        types_vectorized = types_encoder(types_model_input)

        if input_type == "float":
            sem_type_model_input = tf.keras.layers.Input(dtype=tf.float32, shape=(3,))
        elif input_type == "int":
            sem_type_model_input = tf.keras.layers.Input(dtype=tf.int64, shape=(3,))

        merged = tf.keras.layers.Concatenate(axis=1)([tokens_vectorized, types_vectorized, sem_type_model_input])

        hp_emb_dims = hp.Int('emb_dims', min_value=32, max_value=128, step=32)
        embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                            output_dim=hp_emb_dims,
                                            # user masking to handle the variable sequence lengths
                                            mask_zero=True)(merged)
    
        hp_do1 = hp.Choice('dropout1', values=[0.1, 0.2, 0.3])
        dropout1 = tf.keras.layers.Dropout(hp_do1)(embedded)
        globalmaxpooling = tf.keras.layers.GlobalMaxPooling1D()(dropout1)

        hp_do2 = hp.Choice('dropout2', values=[0.1, 0.2, 0.3])
        dropout2 = tf.keras.layers.Dropout(hp_do2)(globalmaxpooling)
        model_output = tf.keras.layers.Dense(num_classes)(dropout2)

        model = tf.keras.models.Model(inputs=[tokens_model_input, types_model_input, sem_type_model_input], outputs=model_output)
        
        hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(hp_learning_rate),
              metrics=["accuracy", tf.keras.metrics.Recall()])
        return model
    
    return model_builder


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#  RNN (Bidirectional LSTM)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------
# 1. TOKENS
#-------------------------------------------------------------------------------------------------------------------

# returns model graph: FEATURES: TOKENS
#
def create_model1_RNN(num_classes, emb_dim, lstm_units, dense_units, tokens_encoder, tokens_size, add_inp_emb_dim=1):
    embedding_input_dim = tokens_size + add_inp_emb_dim

    tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    tokens_vectorized = tokens_encoder(tokens_model_input)

    embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                        output_dim=emb_dim,
                                        # user masking to handle the variable sequence lengths
                                        mask_zero=True)(tokens_vectorized)
    
    bilstmed = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units))(embedded)
    densed1 = tf.keras.layers.Dense(dense_units, activation="relu")(bilstmed)
    model_output = tf.keras.layers.Dense(num_classes)(densed1)

    model = tf.keras.models.Model(inputs=tokens_model_input, outputs=model_output)
        
    return model



# returns model builder: FEATURES: TOKENS
#
def create_model_builder1_RNN(num_classes, tokens_encoder, tokens_size, add_inp_emb_dim=1):

    def model_builder(hp):
        
        embedding_input_dim = tokens_size + add_inp_emb_dim 

        tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        tokens_vectorized = tokens_encoder(tokens_model_input)


        hp_emb_dims = hp.Int('emb_dims', min_value=32, max_value=128, step=32)
        embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                            output_dim=hp_emb_dims,
                                            # user masking to handle the variable sequence lengths
                                            mask_zero=True)(tokens_vectorized)
    
        lstm_units = hp.Int('lstm_units', min_value=32, max_value=128, step=32)
        bilstmed = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units))(embedded)
        dense_units = hp.Int('dense_units', min_value=32, max_value=128, step=32)
        densed1 = tf.keras.layers.Dense(dense_units, activation="relu")(bilstmed)

        model_output = tf.keras.layers.Dense(num_classes)(densed1)

        model = tf.keras.models.Model(inputs=tokens_model_input, outputs=model_output)
        
        hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(hp_learning_rate),
              metrics=["accuracy", tf.keras.metrics.Recall()])
        return model
    
    return model_builder

#-------------------------------------------------------------------------------------------------------------------
# 2. TYPES
#-------------------------------------------------------------------------------------------------------------------

# returns model graph: FEATURES: TYPES
#
def create_model2_RNN(num_classes, emb_dim, lstm_units, dense_units, types_encoder, types_size, add_inp_emb_dim=1):
    embedding_input_dim = types_size + add_inp_emb_dim 

    types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    types_vectorized = types_encoder(types_model_input)

    embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                        output_dim=emb_dim,
                                        # user masking to handle the variable sequence lengths
                                        mask_zero=True)(types_vectorized)
    

    bilstmed = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units))(embedded)
    densed1 = tf.keras.layers.Dense(dense_units, activation="relu")(bilstmed)
    model_output = tf.keras.layers.Dense(num_classes)(densed1)

    model = tf.keras.models.Model(inputs=types_model_input, outputs=model_output)
        
    return model



# returns model builder: FEATURES: TYPES
#
def create_model_builder2_RNN(num_classes, types_encoder, types_size, add_inp_emb_dim=1):

    def model_builder(hp):
        embedding_input_dim = types_size + add_inp_emb_dim 

        types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        types_vectorized = types_encoder(types_model_input)

        hp_emb_dims = hp.Int('emb_dims', min_value=32, max_value=128, step=32)
        embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                            output_dim=hp_emb_dims,
                                            # user masking to handle the variable sequence lengths
                                            mask_zero=True)(types_vectorized)
    
        lstm_units = hp.Int('lstm_units', min_value=32, max_value=128, step=32)
        bilstmed = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units))(embedded)
        dense_units = hp.Int('dense_units', min_value=32, max_value=128, step=32)
        densed1 = tf.keras.layers.Dense(dense_units, activation="relu")(bilstmed)

        model_output = tf.keras.layers.Dense(num_classes)(densed1)

        model = tf.keras.models.Model(inputs= types_model_input, outputs=model_output)
        
        hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(hp_learning_rate),
              metrics=["accuracy", tf.keras.metrics.Recall()])
        return model
    
    return model_builder

#-------------------------------------------------------------------------------------------------------------------
# 3. TOKENS + TYPES
#-------------------------------------------------------------------------------------------------------------------

# returns model graph: FEATURES: TOKENS, TYPES
#
def create_model3_RNN(num_classes, emb_dim, lstm_units, dense_units, tokens_encoder, types_encoder, tokens_size, types_size, add_inp_emb_dim=1):
    embedding_input_dim = tokens_size + types_size + add_inp_emb_dim

    tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    tokens_vectorized = tokens_encoder(tokens_model_input)

    types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    types_vectorized = types_encoder(types_model_input)

    merged = tf.keras.layers.Concatenate(axis=1)([tokens_vectorized, types_vectorized])
    embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                        output_dim=emb_dim,
                                        # user masking to handle the variable sequence lengths
                                        mask_zero=True)(merged)
    
    bilstmed = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units))(embedded)
    densed1 = tf.keras.layers.Dense(dense_units, activation="relu")(bilstmed)
    model_output = tf.keras.layers.Dense(num_classes)(densed1)

    model = tf.keras.models.Model(inputs=[tokens_model_input, types_model_input], outputs=model_output)
        
    return model



# returns model builder: FEATURES: TOKENS, TYPES
#
def create_model_builder3_RNN(num_classes, tokens_encoder, types_encoder, tokens_size, types_size, add_inp_emb_dim=1):

    def model_builder(hp):
        embedding_input_dim = tokens_size + types_size + add_inp_emb_dim + 3 # 3 size of sem_type_model_input

        tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        tokens_vectorized = tokens_encoder(tokens_model_input)

        types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        types_vectorized = types_encoder(types_model_input)

        merged = tf.keras.layers.Concatenate(axis=1)([tokens_vectorized, types_vectorized])

        hp_emb_dims = hp.Int('emb_dims', min_value=32, max_value=128, step=32)
        embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                            output_dim=hp_emb_dims,
                                            # user masking to handle the variable sequence lengths
                                            mask_zero=True)(merged)
    
        lstm_units = hp.Int('lstm_units', min_value=32, max_value=128, step=32)
        bilstmed = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units))(embedded)
        dense_units = hp.Int('dense_units', min_value=32, max_value=128, step=32)
        densed1 = tf.keras.layers.Dense(dense_units, activation="relu")(bilstmed)

        model_output = tf.keras.layers.Dense(num_classes)(densed1)

        model = tf.keras.models.Model(inputs=[tokens_model_input, types_model_input], outputs=model_output)
        
        hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(hp_learning_rate),
              metrics=["accuracy", tf.keras.metrics.Recall()])
        return model
    
    return model_builder

#-------------------------------------------------------------------------------------------------------------------
# 4. TOKENS + TYPES + MATH_TYPES
#-------------------------------------------------------------------------------------------------------------------

# returns model graph: ALL FEATURES: TOKENS, TYPES, MATH_TYPES
#
def create_model4_RNN(num_classes, emb_dim, lstm_units, dense_units, tokens_encoder, types_encoder, tokens_size, types_size, input_type, add_inp_emb_dim=1):
    embedding_input_dim = tokens_size + types_size + add_inp_emb_dim + 3 # 3 size of sem_type_model_input

    tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    tokens_vectorized = tokens_encoder(tokens_model_input)

    types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
    types_vectorized = types_encoder(types_model_input)

    if input_type == "float":
        sem_type_model_input = tf.keras.layers.Input(dtype=tf.float32, shape=(3,))
    elif input_type == "int":
        sem_type_model_input = tf.keras.layers.Input(dtype=tf.int64, shape=(3,))

    merged = tf.keras.layers.Concatenate(axis=1)([tokens_vectorized, types_vectorized, sem_type_model_input])
    embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                        output_dim=emb_dim,
                                        # user masking to handle the variable sequence lengths
                                        mask_zero=True)(merged)
    
    bilstmed = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units))(embedded)
    densed1 = tf.keras.layers.Dense(dense_units, activation="relu")(bilstmed)
    model_output = tf.keras.layers.Dense(num_classes)(densed1)

    model = tf.keras.models.Model(inputs=[tokens_model_input, types_model_input, sem_type_model_input], outputs=model_output)
        
    return model



# returns model builder: ALL FEATURES: TOKENS, TYPES, MATH_TYPES
#
def create_model_builder4_RNN(num_classes, tokens_encoder, types_encoder, tokens_size, types_size, input_type, add_inp_emb_dim=1):

    def model_builder(hp):
        ...
        # model = create_model(encoder_count_tokens, encoder_count_types,tokens_input_len, "float", type_input_len)
        embedding_input_dim = tokens_size + types_size + add_inp_emb_dim + 3 # 3 size of sem_type_model_input

        tokens_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        tokens_vectorized = tokens_encoder(tokens_model_input)

        types_model_input = tf.keras.layers.Input(dtype=tf.string, shape=(1,))
        types_vectorized = types_encoder(types_model_input)

        if input_type == "float":
            sem_type_model_input = tf.keras.layers.Input(dtype=tf.float32, shape=(3,))
        elif input_type == "int":
            sem_type_model_input = tf.keras.layers.Input(dtype=tf.int64, shape=(3,))

        merged = tf.keras.layers.Concatenate(axis=1)([tokens_vectorized, types_vectorized, sem_type_model_input])

        hp_emb_dims = hp.Int('emb_dims', min_value=32, max_value=128, step=32)
        embedded = tf.keras.layers.Embedding(input_dim= embedding_input_dim,
                                            output_dim=hp_emb_dims,
                                            # user masking to handle the variable sequence lengths
                                            mask_zero=True)(merged)
    

        lstm_units = hp.Int('lstm_units', min_value=32, max_value=128, step=32)
        bilstmed = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(lstm_units))(embedded)
        dense_units = hp.Int('dense_units', min_value=32, max_value=128, step=32)
        densed1 = tf.keras.layers.Dense(dense_units, activation="relu")(bilstmed)
        model_output = tf.keras.layers.Dense(num_classes)(densed1)

        model = tf.keras.models.Model(inputs=[tokens_model_input, types_model_input, sem_type_model_input], outputs=model_output)
        
        hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(hp_learning_rate),
              metrics=["accuracy", tf.keras.metrics.Recall()])
        return model
    
    return model_builder


def save_vec_vals(model1, encoder_int_tokens, encoder_int_types, tokens_input_len, type_input_len, suffix):
    suffix = "some"

    print("tokens len: ", tokens_input_len)
    print("types len: ", type_input_len)
    try:
        weights = model1.get_layer('embedding').get_weights()[0]
        vocab1 = encoder_int_tokens.get_vocabulary()
        vocab2 = encoder_int_types.get_vocabulary()
        out_v = io.open('vectors1.tsv', 'w', encoding='utf-8')
        out_m = io.open('metadata1.tsv', 'w', encoding='utf-8')
    
        first_index = 0
        for index, word in enumerate(vocab1):
            if index == 0:
                continue  # skip 0, it's padding.
            vec = weights[index]
            out_v.write('\t'.join([str(x) for x in vec]) + "\n")
            out_m.write(word + "\n")
            first_index = index
        first_index = tokens_input_len
        print(first_index)
        # tokens_input_len, type_input_len

        second_index = 0
        for index, word in enumerate(vocab2):
            if index == 0:
                continue  # skip 0, it's padding.
            second_index = index + first_index
            vec = weights[second_index]
            out_v.write('\t'.join([str(x) for x in vec]) + "\n")
            out_m.write(word + "\n")

        second_index = tokens_input_len + type_input_len
        print(second_index)

        #set , scal , func ,
        for index, word in [(0, "SET"), (1, "SCAL"), (2, "FUNC")]:
            vec = weights[second_index + index]
            out_v.write('\t'.join([str(x) for x in vec]) + "\n")
            out_m.write(word + "\n")
    
        out_v.close()
        out_m.close()

    except Exception as e:
        print(e)


# save token embeddings
#
def save_token_embeddings(model, encoder_int_tokens, embedding_layer_name, class_task_str, emb_dim_str):

    vec_path = Path("embedding_vecs_multi/") / (class_task_str + "_" + emb_dim_str + "_" + "vectors.tsv")
    meta_path = Path("embedding_vecs_multi/") / (class_task_str + "_" + emb_dim_str + "_" + "metadata.tsv")

    out_v = io.open(vec_path, 'w', encoding='utf-8')
    out_m = io.open(meta_path, 'w', encoding='utf-8')
    weights = model.get_layer(embedding_layer_name).get_weights()[0]
    vocab = encoder_int_tokens.get_vocabulary()

    for index, word in enumerate(vocab):
        if index == 0:
            continue  # skip 0, it's padding.
        vec = weights[index]
        out_v.write('\t'.join([str(x) for x in vec]) + "\n")
        out_m.write(word + "\n")
    out_v.close()
    out_m.close()




def prediction_to_labels(arg):

    ...