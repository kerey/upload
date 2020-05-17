#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import

import sys

from os.path import basename
from pix2code.model.classes.Sampler import *
from pix2code.model.classes.model.pix2code import *

def test(input_path):

    trained_weights_path = 'pix2code/bin'
    trained_model_name = 'pix2code'
    output_path = 'pix2code/code'
    search_method = 'greedy'

    meta_dataset = np.load("{}/meta_dataset.npy".format(trained_weights_path))

    input_shape = meta_dataset[0]
    output_size = meta_dataset[1]

    model = pix2code(input_shape, output_size, trained_weights_path)
    model.load(trained_model_name)

    sampler = Sampler(trained_weights_path, input_shape, output_size, CONTEXT_LENGTH)

    file_name = basename(input_path)[:basename(input_path).find(".")]
    evaluation_img = Utils.get_preprocessed_img(input_path, IMAGE_SIZE)


    if search_method == 'greedy':
        result, _ = sampler.predict_greedy(model, np.array([evaluation_img]))
        print("Result greedy: {}".format(result))
    else:
        beam_width = int(search_method)
        print("Search with beam width: {}".format(beam_width))
        result, _ = sampler.predict_beam_search(model, np.array([evaluation_img]), beam_width=beam_width)
        print("Result beam: {}".format(result))

    with open("{}/{}.gui".format(output_path, file_name), 'w') as out_f:
        out_f.write(result.replace(START_TOKEN, "").replace(END_TOKEN, ""))
        return output_path + '/' + file_name + '.gui'

if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = None

    return_val = test(arg)
