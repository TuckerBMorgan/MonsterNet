
from random import random
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential

from bokeh.layouts import column, row
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models import Slider, Select

number_of_pokemon = 251
current_pokemon_to_display = 50
start_string = "Spr_2g_"
data_ex = ".npy"
N = 56
img = np.empty((N,N), dtype=np.uint8)
view = img.view(dtype=np.uint8).reshape((N, N))

def load_initial_data():
    pokemon_train = []

    for i in range(number_of_pokemon):
        #the + 1 is because we dont have a Spr_1b_000.png
        image_string = "./grey_scale/" + start_string + str(i + 1).zfill(3) + data_ex
        pokemon_train.append(np.load(image_string))
     #   print("Loaded image", image_string)
    pokemon_train = np.array(pokemon_train)
#    pokemon_train = pokemon_train.reshape((len(pokemon_train), 56, 56, 1))
    pokemon_train = pokemon_train.reshape((len(pokemon_train), np.prod(pokemon_train.shape[1:])))
    return pokemon_train

def load_finished_model(model_name):
    return load_model(model_name)

def predict_pokemon(network, input_data):
    return network.predict(input_data)

def special_case_run_split_network(network, input):
	first_half_of_network = Sequential()
	first_half_of_network.add(network.layers[0])
	first_half_of_network.add(network.layers[1])
	first_half_of_network.add(network.layers[2])
	first_half_of_network.add(network.layers[3])
	first_half_output = first_half_of_network.predict(input)

	second_half_of_network = Sequential()
	second_half_of_network.add(network.layers[4])
	second_half_of_network.add(network.layers[5])
	second_half_of_network.add(network.layers[6])
	second_half_out = second_half_of_network.predict(first_half_output)
	return (first_half_output, second_half_out)
	
def run_split_network(network, single_input):
    first_half_of_network = Sequential()
    first_half_of_network.add(network.layers[0])
    first_half_of_network.add(network.layers[1])
    first_half_of_network.add(network.layers[2])
    first_half_of_network.add(network.layers[3])

    second_half_of_network = Sequential()
    second_half_of_network.add(network.layers[4])
    second_half_of_network.add(network.layers[5])
    second_half_of_network.add(network.layers[6])
    second_half_out = second_half_of_network.predict(single_input)
    return second_half_out

number_options = []
for i in range(251):
	number_options.append(str(i + 1))

# create a plot and style its properties
p = figure(x_range=(0, 10), y_range=(0, 10), toolbar_location=None)
p.outline_line_color = None
p.grid.grid_line_color = None

input_data = load_initial_data()
pokemon_model = load_finished_model("grey_scale_larger")
(first_half_output, second_half_out) = special_case_run_split_network(pokemon_model, input_data)
default = second_half_out[145].reshape(56, 56)

sliders = []
for i in range(32):
    slid = Slider(start=0.0, end=150, value = 0, step = .1, title=str(i))
    sliders.append(slid)

def select_button(attr, old, new):
	global pokemon_model
	new_as_int = int(new)
	setup_field(pokemon_model, new_as_int)

def set_view(new_image):
	for i in range(N):
		for j in range(N):
			view[i, j] = int( new_image[(N - 1) - i,(N - 1) - j] * 255)
	p.image(image=[img], x=0, y=0, dw=10, dh=10)

def setup_field(network, pokemon_number):
	(first_half_output, second_half_out) = special_case_run_split_network(network, input_data)
	default = second_half_out[pokemon_number - 1].reshape(56, 56)
	set_view(default)
	p.image(image=[img], x=0, y=0, dw=10, dh=10)
	for i in range(32):
		sliders[i].value = first_half_output[pokemon_number - 1][i]

setup_field(pokemon_model, 1)
other_col = column(sliders)

def rerun_button():
	slider_values = [0.0] * 32
	for i in range(32):
		slider_values[i] = sliders[i].value
	output = run_split_network(pokemon_model, np.array([np.array(slider_values)]))
	set_view(output[0].reshape(56, 56))


button_for_rerun = Button(label = "Generate Pokemon", button_type="success")
button_for_rerun.on_click(rerun_button)
# put the button and plot in a layout and add to the document
select  = Select(title = "Pokemon Number", value = "0", options=number_options)
select.on_change("value", select_button)
curdoc().add_root(row(column(p, select, button_for_rerun), other_col))