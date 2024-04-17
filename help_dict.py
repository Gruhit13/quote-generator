####################### Do sample helper text #######################
do_sample_text = """
Do you want the model to greedily select next token with the highest probability
or you want it to use the probability distribution to select next token.
For-example: for ouput of model = [0.4, 0.3, 0.15, 0.15] corresponding to words [The, cat, beautiful, nice].
If do sample is off then model will simply select the word that has the highest probability in our case
it is 'The'.

But if do sample is on then the selection of word will be done based on probability distribution so
words other than 'The' will also have chances to be takens as next word
"""
####################### END #######################

# <=======================================================================================================> 
max_token_length = """
The number of words at max you want the model to generate.
"""
####################### END #######################

# <=======================================================================================================> 
num_beams_text = """
During the text generation there are certain tokens that have higher probability which are later
in the sequence but as the succeeding word has low probability this later high prob words does not
get selected and hence num_beams is used like a hypothesis that keep track of cumulative probability.
Hence the text-sequence with highest cumulative probability among all the num_beams will be takens
as final generated sequence.
"""
####################### END #######################

# <=======================================================================================================> 
top_k_text = """
When sampling tokens with the least prabability value is probable to occur but actually is not needed,
hence this parameter configure hoe many top tokens to consider when choosing next token based on 
probability distribution.
"""
####################### END #######################

# <=======================================================================================================> 
top_p_text = """
It can be hard to configure what peculiar value of top-K will meet your need. Instead use cummulative
probability threshold to select the tokens in the pool of next-token selection. Tokens will be selected
till their cummulative probability mass is under the top_p value. 
"""
####################### END #######################

# <=======================================================================================================> 
temperature = """
A threshold to take tokens with probability higher than this temperature for predicting next-word.
"""

helper = {
    'do_sample': do_sample_text,
    'max_token_length': max_token_length,
    'num_beams': num_beams_text,
    'top_k': top_k_text,
    'top_p': top_p_text,
    'temperature': temperature
}