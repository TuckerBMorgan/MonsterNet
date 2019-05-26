# MonsterNet

![monsternet-preview](https://github.com/TuckerBMorgan/MonsterNet/blob/master/examplpe.png)

A personal project to learn Autoencoders 


I am interested in the use of Neural Networks to generate new things from an exsisting style
I choose the Pokemon images because they were all the same sizes, and yet still had a distinct style and I could find a good number of them


requirements:

	pip3 install tensorflow

	pip3 install bokeh

	git lfs pull (the grey_scale_larger model is too large for github)


run with:

	bokeh serve --show ./bokeh_server.py

Then adjust the weights and click the Generate Pokemon button to see what changes you have made