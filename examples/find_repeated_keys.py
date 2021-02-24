import uparma

jsons = {
    ("general", "parameters"): "parameters.json",
    ("general", "styles"): "styles.json",
}
up = uparma.UParma(refresh_jsons=True , parameter_data=jsons)

data = up.parameter2id_list
frequencies = {}

style_list = []
for style in data:
    style_freq = {}
    for key in data[style]:
        try:
            style_freq[len(data[style][key])] += 1
        except KeyError:
            style_freq[len(data[style][key])] = 1

        if len(data[style][key]) > 1:
            print(f"{style}: {key}, ids={data[style][key]}")

    frequencies[style] = style_freq.copy()
    if max(style_freq.keys()) > 1:
        style_list.append((style, style_freq))

print()
for style, style_freq in style_list:
    print(f"{style}: {style_freq}")

global_frequencies = {}
for style in frequencies:
    for f in frequencies[style]:
        try:
            global_frequencies[f] += frequencies[style][f]
        except KeyError:
            global_frequencies[f] = frequencies[style][f]

print("\nGlobal Frequencies")
print(global_frequencies)
